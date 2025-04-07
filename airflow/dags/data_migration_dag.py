from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from dotenv import load_dotenv
from airquality_pipeline_dag import default_args
import os
from datetime import datetime

# FILE PATH
location_file_path = os.getenv("LOCATION_FILE_PATH")
sensor_file_path = os.getenv("SENSOR_FILE_PATH")

# DAG DEFINITION
default_args = default_args

# TASKS DEFINITION
with DAG(
        "airquality_pipeline",
        start_date=datetime(2025, 4, 7),
        schedule="2 * * * *",  # run at the second minute of every hour
        default_args=default_args,
        catchup=False) as dag:  # for preventing backfilling

    start_pipeline = EmptyOperator(
        task_id="start_pipeline"
    )

    end_pipeline = EmptyOperator(
        task_id="end_pipeline"
    )
