from __future__ import annotations

import os
import random
import signal
import string
import time
from collections import deque
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Deque

import psycopg
from faker import Faker
from psycopg.types.json import Jsonb


@dataclass(frozen=True)
class WriterConfig:
    database_url: str
    users_interval_s: float
    orders_interval_s: float
    events_interval_s: float
    users_batch_size: int
    orders_batch_size: int
    events_batch_size: int
    retry_delay_s: float


def _env_float(name: str, default: float) -> float:
    raw = os.getenv(name)
    return float(raw) if raw else default


def _env_int(name: str, default: int) -> int:
    raw = os.getenv(name)
    return int(raw) if raw else default


def load_config() -> WriterConfig:
    return WriterConfig(
        database_url=os.getenv(
            "DATABASE_URL",
            "postgresql://postgres:postgres@postgres:5432/postgres",
        ),
        users_interval_s=_env_float("USERS_INTERVAL_S", 1.5),
        orders_interval_s=_env_float("ORDERS_INTERVAL_S", 1.0),
        events_interval_s=_env_float("EVENTS_INTERVAL_S", 0.5),
        users_batch_size=_env_int("USERS_BATCH_SIZE", 3),
        orders_batch_size=_env_int("ORDERS_BATCH_SIZE", 5),
        events_batch_size=_env_int("EVENTS_BATCH_SIZE", 12),
        retry_delay_s=_env_float("RETRY_DELAY_S", 3.0),
    )


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def random_order_number() -> str:
    return "ORD-" + "".join(
        random.choices(string.ascii_uppercase + string.digits, k=10)
    )


def create_schema(conn: psycopg.Connection) -> None:
    with conn.cursor() as cur:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id BIGSERIAL PRIMARY KEY,
                email TEXT NOT NULL UNIQUE,
                full_name TEXT NOT NULL,
                city TEXT NOT NULL,
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
            )
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS orders (
                id BIGSERIAL PRIMARY KEY,
                user_id BIGINT NOT NULL REFERENCES users(id),
                order_number TEXT NOT NULL UNIQUE,
                status TEXT NOT NULL,
                amount_cents INTEGER NOT NULL,
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
            )
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS events (
                id BIGSERIAL PRIMARY KEY,
                user_id BIGINT REFERENCES users(id),
                order_id BIGINT REFERENCES orders(id),
                event_type TEXT NOT NULL,
                payload JSONB NOT NULL,
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
            )
            """
        )
    conn.commit()


def insert_users(conn: psycopg.Connection, fake: Faker, count: int) -> list[int]:
    created_ids: list[int] = []
    with conn.cursor() as cur, conn.transaction():
        for _ in range(count):
            email = fake.unique.email()
            cur.execute(
                """
                INSERT INTO users (email, full_name, city)
                VALUES (%s, %s, %s)
                RETURNING id
                """,
                (email, fake.name(), fake.city()),
            )
            created_ids.append(cur.fetchone()[0])
    fake.unique.clear()
    return created_ids


def insert_orders(
    conn: psycopg.Connection, fake: Faker, user_ids: list[int], count: int
) -> list[int]:
    created_ids: list[int] = []
    statuses = ["pending", "paid", "shipped", "refunded"]
    with conn.cursor() as cur, conn.transaction():
        for _ in range(count):
            user_id = random.choice(user_ids)
            cur.execute(
                """
                INSERT INTO orders (user_id, order_number, status, amount_cents)
                VALUES (%s, %s, %s, %s)
                RETURNING id
                """,
                (
                    user_id,
                    random_order_number(),
                    random.choice(statuses),
                    random.randint(1000, 50000),
                ),
            )
            created_ids.append(cur.fetchone()[0])
    return created_ids


def insert_events(
    conn: psycopg.Connection,
    fake: Faker,
    user_ids: list[int],
    order_ids: list[int],
    count: int,
) -> None:
    event_types = [
        "page_view",
        "signup",
        "checkout_started",
        "checkout_completed",
        "support_ticket",
    ]
    with conn.cursor() as cur, conn.transaction():
        for _ in range(count):
            user_id = (
                random.choice(user_ids) if user_ids and random.random() < 0.9 else None
            )
            order_id = (
                random.choice(order_ids)
                if order_ids and random.random() < 0.7
                else None
            )
            cur.execute(
                """
                INSERT INTO events (user_id, order_id, event_type, payload)
                VALUES (%s, %s, %s, %s)
                """,
                (
                    user_id,
                    order_id,
                    random.choice(event_types),
                    Jsonb(
                        {
                            "path": fake.uri_path(),
                            "user_agent": fake.user_agent(),
                            "ip_address": fake.ipv4_public(),
                            "source": random.choice(["web", "mobile", "api"]),
                        }
                    ),
                ),
            )


def log_run(table: str, count: int) -> None:
    print(f"[{now_utc().isoformat()}] inserted {count} rows into {table}")


def connect_with_retry(config: WriterConfig) -> psycopg.Connection:
    while True:
        try:
            conn = psycopg.connect(config.database_url)
            conn.autocommit = False
            return conn
        except psycopg.OperationalError as exc:
            print(
                f"database connection failed: {exc}; retrying in {config.retry_delay_s}s"
            )
            time.sleep(config.retry_delay_s)


def run() -> None:
    config = load_config()
    fake = Faker()
    stop = False

    def handle_stop(signum: int, frame) -> None:  # noqa: ARG001
        nonlocal stop
        stop = True

    signal.signal(signal.SIGINT, handle_stop)
    signal.signal(signal.SIGTERM, handle_stop)

    user_ids: Deque[int] = deque(maxlen=5000)
    order_ids: Deque[int] = deque(maxlen=5000)

    conn = connect_with_retry(config)
    try:
        create_schema(conn)
        seed_users = insert_users(conn, fake, max(config.users_batch_size, 1))
        user_ids.extend(seed_users)
        log_run("users", len(seed_users))

        next_users = time.monotonic() + config.users_interval_s
        next_orders = time.monotonic() + config.orders_interval_s
        next_events = time.monotonic() + config.events_interval_s

        while not stop:
            now = time.monotonic()
            did_work = False

            if now >= next_users:
                created = insert_users(conn, fake, config.users_batch_size)
                user_ids.extend(created)
                log_run("users", len(created))
                next_users = now + config.users_interval_s
                did_work = True

            if now >= next_orders and user_ids:
                created = insert_orders(
                    conn, fake, list(user_ids), config.orders_batch_size
                )
                order_ids.extend(created)
                log_run("orders", len(created))
                next_orders = now + config.orders_interval_s
                did_work = True

            if now >= next_events and user_ids:
                insert_events(
                    conn,
                    fake,
                    list(user_ids),
                    list(order_ids),
                    config.events_batch_size,
                )
                log_run("events", config.events_batch_size)
                next_events = now + config.events_interval_s
                did_work = True

            if not did_work:
                time.sleep(0.1)
    finally:
        conn.close()


if __name__ == "__main__":
    run()
