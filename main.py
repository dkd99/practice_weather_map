import sqlite3
import requests
import schedule
import time
import threading

def get_weather(city, units='metric', api_key='e170cf5a92b4797f093bb94ca1fbbdf3'):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units={units}"
    r = requests.get(url)
    content = r.json()
    return content

def init_db():
    conn = sqlite3.connect('weather_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS weather (
            datetime TEXT PRIMARY KEY,
            city TEXT NOT NULL,
            temperature REAL,
            description TEXT
        )
    ''')
    conn.commit()
    conn.close()
    
def save_weather_to_db(weather_data,city):
    conn = sqlite3.connect('weather_data.db')
    cursor = conn.cursor()
    for dicty in weather_data['list']:
        cursor.execute('''
            INSERT INTO weather (datetime,city, temperature, description)
            VALUES (?,?, ?, ?)
            ON CONFLICT(datetime) DO UPDATE SET
                temperature=excluded.temperature,
                description=excluded.description
        ''', (dicty['dt_txt'],city, dicty['main']['temp'], dicty['weather'][0]['description']))
    conn.commit()
    conn.close()
    
def fetch_and_save_weather(city):
    weather_data = get_weather(city)
    save_weather_to_db(weather_data,city)
    
def schedule_daily_update(city, update_time):
    schedule.every().day.at(update_time).do(fetch_and_save_weather, city=city)

    def run_schedule():
        while True:
            schedule.run_pending()
            time.sleep(1)

    scheduler_thread = threading.Thread(target=run_schedule)
    scheduler_thread.daemon = True
    scheduler_thread.start()
    
def run_scheduler(city, update_time):
    scheduler_thread = threading.Thread(target=schedule_daily_update, args=(city, update_time))
    scheduler_thread.daemon = True
    scheduler_thread.start()
    
if __name__ == "__main__":
    city_name = 'kanpur'  # Replace with your city
    update_time = '23:56'  # Set the time to update daily

    init_db()
    fetch_and_save_weather(city_name)  # Initial fetch and save
    schedule_daily_update(city_name, update_time)