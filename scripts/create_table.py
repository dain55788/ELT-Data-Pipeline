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
            location_name VARCHAR,
            country_code VARCHAR,
            country_name VARCHAR,
            timezone VARCHAR,
            latitude FLOAT,
            longitude FLOAT,
            owner_id INT,
            owner_name VARCHAR,
            provider_id INT,
            provider_name VARCHAR,
            is_mobile BOOLEAN,
            is_monitor BOOLEAN,
            instrument_id INT,
            instrument_name VARCHAR,
            datetime_first_utc TIMESTAMP,
            datetime_last_utc TIMESTAMP,
            load_timestamp TIMESTAMP
        );
    """

    # Staging table - sensors
    create_table_staging_sensors = """
        CREATE TABLE staging.stg_measurement_by_sensors (
            sensor_id INT,
            sensor_name VARCHAR,
            parameter_id INT,
            parameter_name VARCHAR,
            parameter_units VARCHAR,
            parameter_display_name VARCHAR(50),
            measurement_datetime_utc TIMESTAMP,
            measurement_value FLOAT,
            latitude FLOAT,
            longitude FLOAT,
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
