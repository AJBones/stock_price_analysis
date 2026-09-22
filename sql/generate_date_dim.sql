SET SESSION cte_max_recursion_depth = 100000;
INSERT INTO dim_date (
    date_id,
    calendar_date,
    year,
    quarter,
    month,
    day_of_week,
    is_trading_day
)
WITH RECURSIVE date_series AS (
    SELECT DATE('1990-04-01') AS dt

    UNION ALL

    SELECT DATE_ADD(dt, INTERVAL 1 DAY)
    FROM date_series
    WHERE dt < DATE('2040-03-31')
)
SELECT
    CAST(DATE_FORMAT(dt,'%Y%m%d') AS UNSIGNED) AS date_id,
    dt AS calendar_date,
    YEAR(dt) AS year,
    QUARTER(dt) AS quarter,
    MONTH(dt) AS month,
    WEEKDAY(dt) AS day_of_week,
    CASE WHEN WEEKDAY(dt) NOT IN (5, 6) THEN TRUE
    WHEN WEEKDAY(dt) IN (5, 6) THEN FALSE ELSE NULL END AS is_trading_day
FROM date_series
;