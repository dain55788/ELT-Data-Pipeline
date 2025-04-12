{#
    this sql creates a dim_owner table in the production schema
#}

{{ config(materialized = 'table') }}

WITH owner_staging AS (
    SELECT DISTINCT 
        owner_id,
        owner_name
    FROM staging.stg_sensors_by_locations
    WHERE owner_id IS NOT NULL
)

SELECT
    {{ dbt_utils.surrogate_key(['owner_id']) }} as owner_key,
    owner_id,
    owner_name
FROM owner_staging
WHERE owner_id IS NOT NULL
ORDER BY owner_id ASC 