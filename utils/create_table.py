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
    create_table_staging_stations = """
        CREATE TABLE IF NOT EXISTS staging.stations (
            station_id INTEGER PRIMARY KEY,
            name VARCHAR(255),
            locality VARCHAR(100),
            timezone VARCHAR(50),
            country_id INTEGER,
            country_code VARCHAR(2),
            country_name VARCHAR(100),
            owner_id INTEGER,
            owner_name VARCHAR(255),
            provider_id INTEGER,
            provider_name VARCHAR(255),
            is_mobile BOOLEAN,
            is_monitor BOOLEAN,
            latitude FLOAT,
            longitude FLOAT,
            datetime_first_utc TIMESTAMP,
            datetime_first_local TIMESTAMP WITH TIME ZONE,
            datetime_last_utc TIMESTAMP,
            datetime_last_local TIMESTAMP WITH TIME ZONE,
            created_at TIMESTAMP DEFAULT NOW(),
        );
    """

    # Staging table - sensors
    create_table_staging_sensors = """
        CREATE TABLE IF NOT EXISTS staging.sensors (
            sensor_id INTEGER PRIMARY KEY,
            station_id INTEGER,
            name VARCHAR(100),
            parameter_id INTEGER,
            parameter_name VARCHAR(50),
            parameter_units VARCHAR(20),
            parameter_display_name VARCHAR(100),
            datetime_first_utc TIMESTAMP,
            datetime_first_local TIMESTAMP WITH TIME ZONE,
            datetime_last_utc TIMESTAMP,
            datetime_last_local TIMESTAMP WITH TIME ZONE,
            created_at TIMESTAMP DEFAULT NOW(),
            FOREIGN KEY (station_id) REFERENCES staging.stations(station_id)
    );
    """

    # Staging table - Measurements
    create_table_staging_measurements = """
        CREATE TABLE IF NOT EXISTS staging.measurements (
            measurement_id SERIAL PRIMARY KEY,
            sensor_id INTEGER,
            datetime_utc TIMESTAMP,
            datetime_local TIMESTAMP WITH TIME ZONE,
            value FLOAT,
            latitude FLOAT,
            longitude FLOAT,
            min_value FLOAT,
            max_value FLOAT,
            avg_value FLOAT,
            created_at TIMESTAMP DEFAULT NOW(),
            FOREIGN KEY (sensor_id) REFERENCES staging.sensors(sensor_id)
    );
    """


if __name__ == "__main__":
    main()