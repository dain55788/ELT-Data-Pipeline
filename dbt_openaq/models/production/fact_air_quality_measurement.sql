{#
    this sql creates a fact table called fact_air_quality_measurement in the production schema
#}

{{ config(materialized = 'table') }}

WITH air_quality_measurement_staging AS (
    SELECT 
        {{ dbt_utils.surrogate_key(['s.sensor_id', 's.parameter_id', 's.measurement_datetime_utc']) }} as measurement_key,
        ds.sensor_key,
        dp.parameter_key,
        dl.location_key,
        down.owner_key,
        di.instrument_key,
        dv.provider_key,
        s.measurement_value,
        s.summary_min,
        s.summary_max,
        s.summary_avg,
        s.summary_sd,
        s.coverage_observed_count,
        dd.date_key,
        dt.time_key,
        s.measurement_datetime_utc,
        s.latitude,
        s.longitude
    FROM staging.stg_measurement_by_sensors AS s
    CROSS JOIN staging.stg_sensors_by_locations AS lo
    JOIN production.dim_sensor AS ds ON s.sensor_id = ds.sensor_id
    JOIN production.dim_parameter AS dp ON s.parameter_id = dp.parameter_id
    JOIN production.dim_location AS dl ON lo.location_id = dl.location_id
    JOIN production.dim_owner AS down ON lo.owner_id = down.owner_id
    JOIN production.dim_provider AS dv ON lo.provider_id = dv.provider_id
    JOIN production.dim_instrument AS di ON lo.instrument_id = di.instrument_id
    JOIN production.dim_date AS dd ON DATE(s.measurement_datetime_utc) = dd.date_actual
    JOIN production.dim_time AS dt ON EXTRACT(HOUR FROM s.measurement_datetime_utc) = dt.hour
    WHERE ABS(s.latitude - lo.latitude) < 0.0001 
      AND ABS(s.longitude - lo.longitude) < 0.0001
)

SELECT 
    measurement_key,
    sensor_key,
    parameter_key,
    location_key,
    owner_key,
    instrument_key,
    provider_key,
    measurement_value,
    summary_min,
    summary_max,
    summary_avg,
    summary_sd,
    coverage_observed_count,
    date_key,
    time_key,
    measurement_datetime_utc,
    latitude,
    longitude
FROM air_quality_measurement_staging