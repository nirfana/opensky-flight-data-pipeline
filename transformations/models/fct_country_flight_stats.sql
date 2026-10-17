SELECT
    origin_country,
    COUNT(DISTINCT icao24) AS total_active_aircraft,
    ROUND(AVG(velocity), 2) AS avg_velocity,
    MAX(fetched_at) AS last_updated
FROM {{ ref('stg_flights') }}
GROUP BY origin_country
ORDER BY total_active_aircraft DESC
