import os
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from dotenv import load_dotenv
from utils.airquality_collector import fetch_air_quality_locations, fetch_air_quality_sensors, transform_json_format

# FILE PATH
location_file_path = os.getenv("LOCATION_FILE_PATH")
sensor_file_path = os.getenv("SENSOR_FILE_PATH")

# Load environment variables
load_dotenv()
OPENAQ_API_KEY = os.getenv("OPENAQ_API_KEY")

# Default arguments for the DAG
default_args = {
    "owner": "dainynguyen",
    "email_on_failure": False,
    "email_on_retry": False,
    "email": "admin@localhost.com",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
    'catchup_by_default': False
}

# Task dependencies
with DAG(
        "airquality_pipeline",
        start_date=datetime(2025, 4, 7),
        schedule="1 * * * *",  # run at the first minute of every hour
        default_args=default_args,
        catchup=False) as dag:  # for preventing backfilling
    start_pipeline = EmptyOperator(
        task_id="start_pipeline"
    )

    fetch_locations_data = PythonOperator(
        task_id="fetch_openaq_data",
        python_callable=fetch_air_quality_locations(OPENAQ_API_KEY, location_file_path),
    )

    fetch_sensors_data = PythonOperator(
        task_id="fetch_openaq_data",
        python_callable=fetch_air_quality_sensors(OPENAQ_API_KEY, location_file_path, sensor_file_path),
    )

    sensor_file_transformation = PythonOperator(
        task_id="fetch_openaq_data",
        python_callable=transform_json_format(sensor_file_path),
    )

    end_pipeline = EmptyOperator(
        task_id="end_pipeline"
    )


# Data Dependencies
start_pipeline >> fetch_locations_data >> fetch_sensors_data >> sensor_file_transformation >> end_pipeline
