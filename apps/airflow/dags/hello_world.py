from datetime import datetime
from airflow.decorators import dag, task


@dag(
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["example"],
)
def hello_world():

    @task
    def say_hello():
        print("Hello, Airflow 👋")

    say_hello()


dag = hello_world()
