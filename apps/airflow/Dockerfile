FROM apache/airflow:3.1.0

USER root
RUN apt-get update && apt-get install -y --no-install-recommends build-essential && \
    rm -rf /var/lib/apt/lists/*

USER airflow

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Optional: install dbt in a separate venv to avoid dependency conflicts
RUN python -m venv /opt/airflow/dbt_venv && \
    /opt/airflow/dbt_venv/bin/pip install --no-cache-dir dbt-postgres

# Copy DAGs into the image
COPY dags/ /opt/airflow/dags/
COPY transformation/ /opt/airflow/transformation/
