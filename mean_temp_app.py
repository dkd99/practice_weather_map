from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import requests

app = Flask(__name__)

API_KEY = 'e170cf5a92b4797f093bb94ca1fbbdf3'

def get_weather(city, units='metric', api_key=API_KEY):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units={units}"
    r = requests.get(url)
    return r.json()

def init_db():
    conn = sqlite3.connect('mean_weather.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mean_weather (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT,
            datetime TEXT,
            temperature REAL,
            description TEXT,
            UNIQUE(city, datetime)
        )
    ''')
    conn.commit()
    conn.close()

def save_weather_to_db(city, weather_data):
    conn = sqlite3.connect('mean_weather.db')
    cursor = conn.cursor()
    for dicty in weather_data['list']:
        cursor.execute('''
            INSERT OR REPLACE INTO mean_weather (city, datetime, temperature, description) 
            VALUES (?, ?, ?, ?)
        ''', (city, dicty['dt_txt'], dicty['main']['temp'], dicty['weather'][0]['description']))
    conn.commit()
    conn.close()

def get_mean_temperatures():
    conn = sqlite3.connect('mean_weather.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT city, AVG(temperature) as mean_temp
        FROM mean_weather
        GROUP BY city
    ''')
    data = cursor.fetchall()
    conn.close()
    return data

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        city = request.form['city']
        weather_data = get_weather(city)
        save_weather_to_db(city, weather_data)
        return redirect(url_for('index'))
    
    mean_temperatures = get_mean_temperatures()
    return render_template('mean.html', mean_temperatures=mean_temperatures)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
