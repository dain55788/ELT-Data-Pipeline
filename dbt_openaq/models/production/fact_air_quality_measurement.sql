{#
    this sql creates a fact table called fact_air_quality_measurement in the production schema
#}

{{ config(materialized = 'table') }}

WITH air_quality_measurement_staging AS (
    SELECT 
        {{ dbt_utils.surrogate_key(['s.sensor_id', 's.parameter_id', 'lo.location_id', 'lo.owner_id','lo.instrument_id', 'lo.provider_id']) }} as measurement_key,
        ds.sensor_key,
        dp.parameter_key,
        dl.location_key,
        do.owner_key,
        di.instrument_key,
        dv.provider_key,
        s.measurement_value,
        s.summary_min,
        s.summary_max,
        s.summary_avg,
        s.coverage_observed_count,
        dd.date_key,
        dt.time_key,
        s.measurement_datetime_utc,
        
    FROM staging.stg_measurement_by_sensors as s
    JOIN staging.stg_sensors_by_locations as lo ON s.sensor_id = lo.sensor_id
    JOIN production.dim_sensor AS ds ON s.sensor_id = ds.sensor_id
    JOIN production.dim_parameter AS dp ON lo.parameter_id = dp.parameter_id
    JOIN production.dim_location AS dl ON lo.location_id = dl.location_id
    JOIN production.dim_owner AS do ON lo.owner_id = do.owner_id
    JOIN production.dim_provider AS dv ON lo.provider_id = dv.provider_id
    JOIN production.dim_instrument AS di ON lo.instrument_id = di.instrument_id
    JOIN production.dim_date AS dd ON DATE(s.measurement_datetime_utc) = dd.date_actual
    JOIN production.dim_time AS dt ON EXTRACT(HOUR FROM s.measurement_datetime_utc) = dt.hour
)

SELECT * FROM air_quality_measurement_staging