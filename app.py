from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

# get your api key from https://openweathermap.org/api
API_KEY = os.getenv('WEATHER_API_KEY', 'apikey')
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = {}
    if request.method == 'POST':
        city = request.form['city']
        weather_data = get_weather(city)
    return render_template('index.html', weather=weather_data)

def get_weather(city):
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'  
    }
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        
        weather_info = {
            'city': data['name'],
            'country': data['sys']['country'],
            'temp': round(data['main']['temp']),
            'feels_like': round(data['main']['feels_like']),
            'description': data['weather'][0]['description'].title(),
            'icon': data['weather'][0]['icon'],
            'humidity': data['main']['humidity'],
            'wind': round(data['wind']['speed']),
        }
        return weather_info
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None

if __name__ == '__main__':
    app.run(debug=True)
