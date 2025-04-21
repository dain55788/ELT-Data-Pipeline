from datetime import timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.utils.dates import days_ago

from utils.migrate_data import load_measurements_by_sensors

# DAG DEFINITION
default_args = {
    "owner": "dainynguyen",
    "email_on_failure": False,
    "email_on_retry": False,
    "email": "admin@localhost.com",
    "retries": 1,
    "retry_delay": timedelta(seconds=10),
    'catchup_by_default': False
}

# TASKS DEFINITION
with DAG(
        "data_migration_pipeline",
        start_date=days_ago(0),
        schedule="2 * * * *",  # run at the second minute of every hour
        default_args=default_args,
        # catchup=False
        ) as dag:  # for preventing backfilling

    start_pipeline = EmptyOperator(
        task_id="start_pipeline"
    )

    insert_measurement_sensors_data = PythonOperator(
        task_id="measurement_data_insert",
        python_callable=load_measurements_by_sensors
    )

    end_pipeline = EmptyOperator(
        task_id="end_pipeline"
    )

# TASK DEPENDENCIES
start_pipeline >> insert_measurement_sensors_data >> end_pipeline
