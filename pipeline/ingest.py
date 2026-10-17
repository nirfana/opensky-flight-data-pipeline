import requests
import psycopg2
from datetime import datetime

# 1. Fetch live aircraft positions (Bounding Box check: Europe/US coordinates)
# OpenSky returns raw state vectors as JSON arrays
url = "https://opensky-network.org/api/states/all?lamin=45.83&lomin=5.99&lamax=47.82&lomax=10.52"
response = requests.get(url).json()

flight_states = response.get("states", [])

# 2. Connect to local Postgres Warehouse container
conn = psycopg2.connect(
    host="localhost",
    database="analytics",
    user="de_user",
    password="de_password",
    port=5432
)
cursor = conn.cursor()

# 3. Create raw staging table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS staging_flights (
        icao24 VARCHAR(50),
        callsign VARCHAR(50),
        origin_country VARCHAR(100),
        longitude NUMERIC,
        latitude NUMERIC,
        baro_altitude NUMERIC,
        velocity NUMERIC,
        fetched_at TIMESTAMP
    );
""")

# 4. Insert fetched flight vectors
timestamp = datetime.utcnow()
inserted_count = 0

if flight_states:
    for state in flight_states:
        # OpenSky array indices: 0: icao24, 1: callsign, 2: origin_country, 5: longitude, 6: latitude, 7: baro_altitude, 9: velocity
        icao24 = state[0]
        callsign = state[1].strip() if state[1] else None
        origin_country = state[2]
        longitude = state[5]
        latitude = state[6]
        baro_altitude = state[7]
        velocity = state[9]

        cursor.execute("""
            INSERT INTO staging_flights 
            (icao24, callsign, origin_country, longitude, latitude, baro_altitude, velocity, fetched_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """, (icao24, callsign, origin_country, longitude, latitude, baro_altitude, velocity, timestamp))
        inserted_count += 1

conn.commit()
cursor.close()
conn.close()

print(f"Successfully ingested {inserted_count} flight records at {timestamp}.")