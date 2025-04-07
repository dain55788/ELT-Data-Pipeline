import os
from dotenv import load_dotenv
from postgresql_client import PostgresSQLClient
load_dotenv(".env")


def main():
    # create connection
    pc = PostgresSQLClient(
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
    )

    # Staging table - stations
    create_table_staging_location = """
        CREATE TABLE staging.stg_sensors_by_locations (
            location_id INT,
            location_name VARCHAR(50),
            country_code VARCHAR(2),
            country_name VARCHAR(50),
            timezone VARCHAR(50),
            latitude FLOAT,
            longitude FLOAT,
            provider_id INT,
            provider_name VARCHAR(50),
            is_mobile BOOLEAN,
            is_monitor BOOLEAN,
            parameter_id INT,
            parameter_name VARCHAR(50),
            parameter_units VARCHAR(20),
            parameter_display_name VARCHAR(50),
            datetime_first_utc TIMESTAMP,
            datetime_last_utc TIMESTAMP,
            load_timestamp TIMESTAMP
        );
    """

    # Staging table - sensors
    create_table_staging_sensors = """
        CREATE TABLE staging.stg_measurement_by_sensors (
            sensor_id INT,
            sensor_name VARCHAR(50),
            parameter_id INT,
            parameter_name VARCHAR(50),
            parameter_units VARCHAR(20),
            parameter_display_name VARCHAR(50),
            measurement_datetime_utc TIMESTAMP,
            measurement_value FLOAT,
            latitude FLOAT,
            longitude FLOAT,
            datetime_first_utc TIMESTAMP,
            datetime_last_utc TIMESTAMP,
            summary_min FLOAT,
            summary_max FLOAT,
            summary_avg FLOAT,
            summary_sd FLOAT,
            coverage_observed_count INT,
            load_timestamp TIMESTAMP
        );
    """

    try:
        pc.execute_query(create_table_staging_location)
        pc.execute_query(create_table_staging_sensors)
    except Exception as e:
        print(f"Failed to create table with error: {e}")


if __name__ == "__main__":
    main()