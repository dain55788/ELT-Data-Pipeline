{#
    this sql creates a dim_provider table in the production schema
#}

{{ config(materialized = 'table') }}

WITH provider_staging AS (
    SELECT DISTINCT 
        provider_id,
        provider_name
    FROM staging.stg_sensors_by_locations
    WHERE provider_id IS NOT NULL
)

SELECT
    {{ dbt_utils.surrogate_key(['provider_id']) }} as provider_key,
    provider_id,
    provider_name
FROM provider_staging
WHERE provider_id IS NOT NULL
ORDER BY provider_id ASC 