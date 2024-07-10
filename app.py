from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def query_weather_data(city):
    conn = sqlite3.connect('weather_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM weather ')
    rows = cursor.fetchall()
    conn.close()
    return rows

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        city = request.form['city']
        weather_data = query_weather_data(city)
        return render_template('index.html', weather_data=weather_data, city=city)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)