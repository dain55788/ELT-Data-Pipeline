from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from utils.airquality_collector import fetch_air_quality_locations, fetch_air_quality_sensors, transform_json_format

# DEFAULT DAG ARGUMENTS
default_args = {
    "owner": "dainynguyen",
    "email_on_failure": False,
    "email_on_retry": False,
    "email": "admin@localhost.com",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
    'catchup_by_default': False
}

# TASK DEFINITION
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
        python_callable=fetch_air_quality_locations(),
    )

    fetch_sensors_data = PythonOperator(
        task_id="fetch_openaq_data",
        python_callable=fetch_air_quality_sensors(),
    )

    sensor_file_transformation = PythonOperator(
        task_id="fetch_openaq_data",
        python_callable=transform_json_format(),
    )

    end_pipeline = EmptyOperator(
        task_id="end_pipeline"
    )


# TASK DEPENDENCIES
start_pipeline >> fetch_locations_data >> fetch_sensors_data >> sensor_file_transformation >> end_pipeline
