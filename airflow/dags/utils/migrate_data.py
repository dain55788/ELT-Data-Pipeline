from datetime import datetime
import json

from scripts.postgresql_client import PostgresSQLClient
from psycopg2.extras import execute_values

import os
from dotenv import load_dotenv

import sys
sys.path.append('/opt/airflow/scripts')
sys.path.append('../../scripts')

# LOAD ENVIRONMENT VARIABLES
load_dotenv()

# FILE PATH
location_file_path = os.getenv("LOCATION_FILE_PATH")
sensor_file_path = os.getenv("SENSOR_FILE_PATH")


# INSERT LOCATION DATA TO DATABASE
def load_sensors_by_locations():
    with open(location_file_path, 'r') as f:
        data = json.load(f)

    locations = data['results']

    records = []
    for location in locations:
        instrument = location['instruments'][0] if location['instruments'] else {}
        record = (
            location['id'],
            location['name'],
            location['country']['code'],
            location['country']['name'],
            location['timezone'],
            location['coordinates']['latitude'],
            location['coordinates']['longitude'],
            location.get('owner', {}).get('id'),
            location.get('owner', {}).get('name'),
            location['provider']['id'],
            location['provider']['name'],
            location.get('isMobile', False),
            location.get('isMonitor', False),
            instrument.get('id'),
            instrument.get('name'),
            location['datetimeFirst']['utc'],
            location['datetimeLast']['utc'],
            datetime.utcnow()  # load_timestamp
        )
        records.append(record)

    # CONNECT TO THE DATABASE
    conn = PostgresSQLClient(
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST", "host.docker.internal")
    )

    # SQL INSERT STATEMENT
    insert_location_data = """
            INSERT INTO staging.stg_sensors_by_locations (
                location_id, location_name, country_code, country_name, timezone, 
                latitude, longitude, owner_id, owner_name, provider_id, provider_name,
                is_mobile, is_monitor, instrument_id, instrument_name,
                datetime_first_utc, datetime_last_utc, load_timestamp
            ) VALUES %s
        """

    # Chèn dữ liệu bằng execute_values để tối ưu hiệu suất
    try:
        conn.execute_query(insert_location_data)
        print(f"Inserted {len(records)} records into stg_sensors_by_locations")
    except Exception as e:
        print(f"Fail to insert to database because of error: {e}")


# INSERT MEASUREMENT BY SENSORS DATA TO DATABASE
def load_measurements_by_sensors():
    with open(sensor_file_path, 'r') as f:
        data = json.load(f)

    records = []

    for sensor in data:
        record = (
            sensor['id'],
            sensor['name'],
            sensor['parameter']['id'],
            sensor['parameter']['name'],
            sensor['parameter']['units'],
            sensor['parameter']['displayName'],
            sensor['latest']['datetime']['utc'],
            sensor['latest']['value'],
            sensor['latest']['coordinates']['latitude'],
            sensor['latest']['coordinates']['longitude'],
            sensor['summary']['min'],
            sensor['summary']['max'],
            sensor['summary']['avg'],
            sensor['summary']['sd'],
            sensor['coverage']['observedCount'],
            datetime.utcnow()
        )
        records.append(record)

        #  CONNECT TO POSTGRES DATABASE
        conn = PostgresSQLClient(
            database=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            host=os.getenv("POSTGRES_HOST", "host.docker.internal")
        )

        cur = conn.cursor()

        # SQL INSERT STATEMENT:
        insert_sensor_data = """
                INSERT INTO staging.stg_measurement_by_sensors (
                    sensor_id, sensor_name, parameter_id, parameter_name, parameter_units,
                    parameter_display_name, measurement_datetime_utc, measurement_value,
                    latitude, longitude, summary_min, summary_max, summary_avg, summary_sd,
                    coverage_observed_count, load_timestamp
                ) VALUES %s
            """

        # EXECUTE INSERT QUERY USING execute_values
        try:
            execute_values(cur, insert_sensor_data, records)
            conn.commit()
            print(f"Inserted {len(records)} records into stg_measurement_by_sensors")
        except Exception as e:
            print(f"Fail to insert sensor data to database because of error: {e}")
            conn.rollback()
        finally:
            cur.close()
            conn.close()
