WITH raw_flights AS (
    SELECT * FROM {{ source('public', 'staging_flights') }}
)
SELECT
    icao24,
    TRIM(callsign) AS callsign,
    origin_country,
    longitude,
    latitude,
    baro_altitude,
    velocity,
    fetched_at
FROM raw_flights
WHERE longitude IS NOT NULL AND latitude IS NOT NULL
