import sqlite3

def get_latest_weather():
    conn = sqlite3.connect("weather.db")
    cur = conn.cursor()
    cur.execute("""
        SELECT location, date, temp_max, precipitation, windspeed
        FROM weather
        ORDER BY fetched_at DESC
        LIMIT 3
    """)
    rows = cur.fetchall()
    conn.close()
    return rows

def build_table_rows(weather_data):
    rows = ""
    for row in weather_data:
        location, date, temp, rain, wind = row
        rows += f"""
        <tr>
            <td>{location}</td>
            <td>{temp}</td>
            <td>{rain}</td>
            <td>{wind}</td>
        </tr>"""
    return rows

def update_html():
    # Read the poem
    try:
        with open("poem.txt", "r", encoding="utf-8") as f:
            poem = f.read().strip()
    except FileNotFoundError:
        poem = "Poem could not be generated."

    # Read weather data
    weather_data = get_latest_weather()
    table_rows = build_table_rows(weather_data)

    # Read the HTML file
    with open("docs/index.html", "r", encoding="utf-8") as f:
        html = f.read()

    # Replace poem section
    html = html.split("<!-- POEM_START -->")[0] + \
           "<!-- POEM_START -->\n" + poem + "\n" + \
           "<!-- POEM_END -->" + html.split("<!-- POEM_END -->")[1]

    # Replace table section
    html = html.split("<!-- TABLE_START -->")[0] + \
           "<!-- TABLE_START -->" + table_rows + "\n<!-- TABLE_END -->" + \
           html.split("<!-- TABLE_END -->")[1]

    # Write back
    with open("docs/index.html", "w", encoding="utf-8") as f:
        f.write(html)

    print("✅ index.html updated successfully!")

if __name__ == "__main__":
    update_html()