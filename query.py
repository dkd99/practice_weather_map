import sqlite3

def query_weather_data():
    conn = sqlite3.connect('weather_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM weather')
    rows = cursor.fetchall()
    conn.close()
    for row in rows:
        print(f"Datetime: {row[0]}, Temperature: {row[1]}, Description: {row[2]}")
        
query_weather_data()