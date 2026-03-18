import requests
import sqlite3
from datetime import datetime, timedelta

# Locations
LOCATIONS = [
    {"name": "Faisalabad", "lat": 31.4504, "lon": 73.1350},
    {"name": "Islamabad",  "lat": 33.6844, "lon": 73.0479},
    {"name": "Aalborg",    "lat": 57.0488, "lon": 9.9217},
]

# Weather variables to fetch
VARIABLES = "temperature_2m_max,precipitation_sum,windspeed_10m_max,cloudcover_mean,relativehumidity_2m_max"

def fetch_weather(location):
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": location["lat"],
        "longitude": location["lon"],
        "daily": VARIABLES,
        "timezone": "auto",
        "start_date": tomorrow,
        "end_date": tomorrow,
    }
    response = requests.get(url, params=params)
    data = response.json()
    daily = data["daily"]
    return {
        "location": location["name"],
        "date": daily["time"][0],
        "temp_max": daily["temperature_2m_max"][0],
        "precipitation": daily["precipitation_sum"][0],
        "windspeed": daily["windspeed_10m_max"][0],
        "cloudcover": daily["cloudcover_mean"][0],
        "humidity": daily["relativehumidity_2m_max"][0],
    }

def save_to_db(records):
    conn = sqlite3.connect("weather.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS weather (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            location TEXT,
            date TEXT,
            temp_max REAL,
            precipitation REAL,
            windspeed REAL,
            cloudcover REAL,
            humidity REAL,
            fetched_at TEXT
        )
    """)
    for r in records:
        cur.execute("""
            INSERT INTO weather (location, date, temp_max, precipitation, windspeed, cloudcover, humidity, fetched_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            r["location"], r["date"], r["temp_max"], r["precipitation"],
            r["windspeed"], r["cloudcover"], r["humidity"],
            datetime.now().isoformat()
        ))
    conn.commit()
    conn.close()
    print("✅ Weather data saved to database.")

if __name__ == "__main__":
    records = []
    for loc in LOCATIONS:
        print(f"Fetching weather for {loc['name']}...")
        record = fetch_weather(loc)
        records.append(record)
        print(f"  {record}")
    save_to_db(records)