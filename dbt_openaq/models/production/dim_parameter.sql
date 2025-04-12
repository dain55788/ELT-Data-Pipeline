{#
    this sql creates a dim_parameter table in the production schema
#}

{{ config(materialized = 'table') }}

WITH parameter_staging AS (
    SELECT DISTINCT 
        parameter_id, 
        parameter_name, 
        parameter_units, 
        parameter_display_name
    FROM staging.stg_measurement_by_sensors
    WHERE parameter_id IS NOT NULL
)

SELECT
    {{ dbt_utils.surrogate_key(['parameter_id']) }} as parameter_key,
    parameter_id,
    parameter_name,
    parameter_units,
    parameter_display_name
FROM parameter_staging
WHERE parameter_id IS NOT NULL
ORDER BY parameter_id ASC