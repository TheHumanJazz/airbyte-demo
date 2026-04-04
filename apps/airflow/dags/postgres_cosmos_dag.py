import os
from datetime import datetime

from cosmos import DbtDag, ProjectConfig, ProfileConfig, ExecutionConfig
from cosmos.profiles import PostgresUserPasswordProfileMapping

airflow_home = os.environ["AIRFLOW_HOME"]

profile_config = ProfileConfig(
    profile_name="default",
    target_name="dev",
    profile_mapping=PostgresUserPasswordProfileMapping(
        conn_id="my_postgres",
        profile_args={"schema": "public"},
    ),
)

execution_config = ExecutionConfig(
    dbt_executable_path=f"{airflow_home}/dbt_venv/bin/dbt",
)

postgres_cosmos_dag = DbtDag(
    dag_id="postgres_cosmos_dag",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
    project_config=ProjectConfig(
        dbt_project_path=f"{airflow_home}/transformation",
    ),
    profile_config=profile_config,
    execution_config=execution_config,
    tags=["cosmos", "dbt", "postgres"],
)
