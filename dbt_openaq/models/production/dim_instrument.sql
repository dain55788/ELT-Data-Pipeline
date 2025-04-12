{#
    this sql creates a dim_instrument table in the production schema
#}

{{ config(materialized = 'table') }}

WITH instrument_staging AS (
    SELECT DISTINCT 
        instrument_id,
        instrument_name
    FROM staging.stg_sensors_by_locations
    WHERE instrument_id IS NOT NULL
)

SELECT
    {{ dbt_utils.surrogate_key(['instrument_id']) }} as instrument_key,
    instrument_id,
    instrument_name
FROM instrument_staging
WHERE instrument_id IS NOT NULL
ORDER BY instrument_id ASC 