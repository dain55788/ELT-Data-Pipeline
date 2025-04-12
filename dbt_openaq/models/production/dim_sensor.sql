{#
    this sql creates a dim_sensor table in the production schema
#}

{{ config(materialized = 'table') }}

WITH sensor_staging AS (
    SELECT DISTINCT sensor_id, sensor_name
    FROM staging.stg_measurement_by_sensors
    WHERE sensor_id IS NOT NULL
)

SELECT
    {{ dbt_utils.surrogate_key(['sensor_id']) }} as sensor_key,
    sensor_id,
    sensor_name
FROM sensor_staging
WHERE sensor_id IS NOT NULL
ORDER BY sensor_id ASC