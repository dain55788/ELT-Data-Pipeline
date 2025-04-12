{#
    this sql creates a dim_location table in the production schema
#}

{{ config(materialized = 'table') }}

WITH location_staging AS (
    SELECT DISTINCT 
        location_id,
        location_name,
        country_code,
        country_name,
        timezone,
        latitude,
        longitude,
        is_mobile,
        is_monitor
    FROM staging.stg_sensors_by_locations
    WHERE location_id IS NOT NULL
)

SELECT
    {{ dbt_utils.surrogate_key(['location_id']) }} as location_key,
    location_id,
    location_name,
    country_code,
    country_name,
    timezone,
    latitude,
    longitude,
    is_mobile,
    is_monitor
FROM location_staging
WHERE location_id IS NOT NULL
ORDER BY location_id ASC 