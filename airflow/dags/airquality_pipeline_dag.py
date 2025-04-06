import os
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from dotenv import load_dotenv
from utils.airquality_collector import fetch_api_openaq

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
        start_date=datetime(2025, 4, 6),
        schedule="0 6 * * *",  # 6AM daily
        default_args=default_args,
        catchup=False) as dag:  # for preventing backfilling
    start_pipeline = EmptyOperator(
        task_id="start_pipeline"
    )

    fetch_data = PythonOperator(
        task_id="fetch_openaq_data",
        python_callable=fetch_api_openaq(OPENAQ_API_KEY),
    )

    end_pipeline = EmptyOperator(
        task_id="end_pipeline"
    )


start_pipeline >> fetch_data >> end_pipeline

