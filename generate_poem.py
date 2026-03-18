import os
import sqlite3
from groq import Groq

def get_latest_weather():
    conn = sqlite3.connect("weather.db")
    cur = conn.cursor()
    cur.execute("""
        SELECT location, date, temp_max, precipitation, windspeed, cloudcover, humidity
        FROM weather
        ORDER BY fetched_at DESC
        LIMIT 3
    """)
    rows = cur.fetchall()
    conn.close()
    return rows

def build_prompt(weather_data):
    lines = []
    for row in weather_data:
        location, date, temp, rain, wind, cloud, humidity = row
        lines.append(
            f"{location} on {date}: max temp {temp}°C, "
            f"precipitation {rain}mm, wind {wind}km/h, "
            f"cloud cover {cloud}%, humidity {humidity}%"
        )
    weather_summary = "\n".join(lines)

    prompt = f"""
Here is tomorrow's weather forecast for three cities:

{weather_summary}

Please write a short creative poem that:
- Compares the weather in these three cities
- Describes the differences vividly
- Suggests which city would be the nicest to be in tomorrow
- Is written in TWO languages: English first, then Urdu

Keep it fun and creative!
"""
    return prompt

def generate_poem():
    api_key = os.environ.get("GROQ_API_KEY")
    client = Groq(api_key=api_key)

    weather_data = get_latest_weather()
    if not weather_data:
        print("No weather data found. Run fetch.py first.")
        return ""

    prompt = build_prompt(weather_data)

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}]
    )

    poem = response.choices[0].message.content
    print("✅ Poem generated!")
    print(poem)
    return poem

if __name__ == "__main__":
    generate_poem()