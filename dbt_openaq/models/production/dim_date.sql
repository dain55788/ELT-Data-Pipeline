{#
    this sql creates a dim_date table (from 2025 to 2026)  in the production schema
#}

{{ config(materialized = 'table') }}

WITH date_spine AS (
    {{ dbt_utils.date_spine(
        datepart="day",
        start_date="cast('2024-01-01' as date)",
        end_date="cast(dateadd(year, 1, current_date) as date)"
    ) }}
),

date_dimension AS (
    SELECT
        date_day as date_actual,
        {{ dbt_utils.surrogate_key(['date_day']) }} as date_key,
        
        EXTRACT(YEAR FROM date_day) as year,
        EXTRACT(MONTH FROM date_day) as month,
        EXTRACT(DAY FROM date_day) as day_of_month,
        EXTRACT(QUARTER FROM date_day) as quarter,
        EXTRACT(DOW FROM date_day) as day_of_week,
        EXTRACT(DOY FROM date_day) as day_of_year,
        EXTRACT(WEEK FROM date_day) as week_of_year,
        
        TO_CHAR(date_day, 'YYYY-MM-DD') as date_string,
        TO_CHAR(date_day, 'YYYY-MM') as year_month,
        TO_CHAR(date_day, 'YYYY-Q') as year_quarter,
        TO_CHAR(date_day, 'Month') as month_name,
        TO_CHAR(date_day, 'Mon') as month_name_short,
        TO_CHAR(date_day, 'Day') as day_name,
        TO_CHAR(date_day, 'Dy') as day_name_short,
        
        CASE 
            WHEN EXTRACT(MONTH FROM date_day) >= 4 THEN EXTRACT(YEAR FROM date_day)
            ELSE EXTRACT(YEAR FROM date_day) - 1
        END as fiscal_year,
        
        CASE 
            WHEN EXTRACT(MONTH FROM date_day) >= 4 THEN EXTRACT(MONTH FROM date_day) - 3
            ELSE EXTRACT(MONTH FROM date_day) + 9
        END as fiscal_month,
        
        CASE 
            WHEN EXTRACT(MONTH FROM date_day) IN (4, 5, 6) THEN 1
            WHEN EXTRACT(MONTH FROM date_day) IN (7, 8, 9) THEN 2
            WHEN EXTRACT(MONTH FROM date_day) IN (10, 11, 12) THEN 3
            WHEN EXTRACT(MONTH FROM date_day) IN (1, 2, 3) THEN 4
        END as fiscal_quarter,
        
        CASE 
            WHEN EXTRACT(DOW FROM date_day) IN (0, 6) THEN TRUE
            ELSE FALSE
        END as is_weekend,
        
        DATE_TRUNC('week', date_day)::DATE as week_start_date,
        (DATE_TRUNC('week', date_day) + INTERVAL '6 days')::DATE as week_end_date,
        
        DATE_TRUNC('month', date_day)::DATE as month_start_date,
        (DATE_TRUNC('month', date_day) + INTERVAL '1 month - 1 day')::DATE as month_end_date,
        
        CASE
            WHEN EXTRACT(MONTH FROM date_day) IN (12, 1, 2) THEN 'Winter'
            WHEN EXTRACT(MONTH FROM date_day) IN (3, 4, 5) THEN 'Spring'
            WHEN EXTRACT(MONTH FROM date_day) IN (6, 7, 8) THEN 'Summer'
            WHEN EXTRACT(MONTH FROM date_day) IN (9, 10, 11) THEN 'Fall'
        END as season,
        
        CASE WHEN date_day = CURRENT_DATE THEN TRUE ELSE FALSE END as is_today,
        CASE WHEN date_day = CURRENT_DATE - INTERVAL '1 day' THEN TRUE ELSE FALSE END as is_yesterday,
        CASE WHEN date_day = CURRENT_DATE + INTERVAL '1 day' THEN TRUE ELSE FALSE END as is_tomorrow,
        CASE WHEN EXTRACT(YEAR FROM date_day) = EXTRACT(YEAR FROM CURRENT_DATE) THEN TRUE ELSE FALSE END as is_current_year,
        CASE WHEN EXTRACT(MONTH FROM date_day) = EXTRACT(MONTH FROM CURRENT_DATE) 
             AND EXTRACT(YEAR FROM date_day) = EXTRACT(YEAR FROM CURRENT_DATE) 
             THEN TRUE ELSE FALSE END as is_current_month
    FROM date_spine
)

SELECT * FROM date_dimension
ORDER BY date_actual 