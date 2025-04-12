{#
    this sql creates a dim_time table in the production schema
#}

{{ config(materialized = 'table') }}

WITH time_hours AS (
    SELECT generate_series(0, 23, 1) AS hour
),

time_dimension AS (
    SELECT
        hour,
        {{ dbt_utils.surrogate_key(['hour']) }} as time_key,
        
        -- Time formats
        TO_CHAR((TIMESTAMP '1970-01-01 00:00:00' + hour * INTERVAL '1 hour'), 'HH24:00:00') as time_of_day,
        
        CASE
            WHEN hour BETWEEN 0 AND 5 THEN 'Night'
            WHEN hour BETWEEN 6 AND 11 THEN 'Morning'
            WHEN hour BETWEEN 12 AND 17 THEN 'Afternoon'
            ELSE 'Evening'
        END as day_period,
        
        CASE
            WHEN hour < 12 THEN 'AM'
            ELSE 'PM'
        END as am_pm
    FROM time_hours
)

SELECT * 
FROM time_dimension
ORDER BY hour 