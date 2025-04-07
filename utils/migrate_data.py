import json
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
import psycopg2
from psycopg2.extras import execute_values
from utils.postgresql_client import PostgresSQLClient
import os
from dotenv import load_dotenv

# LOAD ENVIRONMENT VARIABLES
load_dotenv()

# FILE PATH
location_file_path = os.getenv("LOCATION_FILE_PATH")
sensor_file_path = os.getenv("SENSOR_FILE_PATH")


# INSERT LOCATION DATA TO DATABASE
def load_sensors_by_locations(**kwargs):

    with open(location_file_path, 'r') as f:
        data = json.load(f)

    locations = data['results']

    records = []
    for location in locations:
        for sensor in location['sensors']:
            record = (
                location['id'],
                location['name'],
                location['country']['code'],
                location['country']['name'],
                location['timezone'],
                location['coordinates']['latitude'],
                location['coordinates']['longitude'],
                location['provider']['id'],
                location['provider']['name'],
                location['isMobile'],
                location['isMonitor'],
                location['datetimeFirst']['utc'],
                location['datetimeLast']['utc'],
                datetime.utcnow()  # load_timestamp
            )
            records.append(record)

    # Kết nối đến cơ sở dữ liệu
    conn = PostgresSQLClient(
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
    )
    cur = conn.cursor()

    # Câu lệnh SQL để chèn dữ liệu
    insert_query = """
        INSERT INTO staging.stg_sensors_by_locations (
            location_id, location_name, country_code, country_name, timezone, latitude, longitude,
            provider_id, provider_name, is_mobile, is_monitor, sensor_id, sensor_name,
            parameter_id, parameter_name, parameter_units, parameter_display_name,
            datetime_first_utc, datetime_last_utc, load_timestamp
        ) VALUES %s
    """

    # Chèn dữ liệu bằng execute_values để tối ưu hiệu suất
    execute_values(cur, insert_query, records)
    conn.commit()

    # Đóng kết nối
    cur.close()
    conn.close()
    print(f"Inserted {len(records)} records into stg_sensors_by_locations")
