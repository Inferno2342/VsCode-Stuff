import requests
from dotenv import load_dotenv
import os
from dataclasses import dataclass

load_dotenv()
api_key = os.getenv('API_KEY')

@dataclass
class WeatherData:
    main: str
    description: str
    icon: str
    temperature: float

def get_lat_lon(city_name, state_code, country_code, api_key):
    resp = requests.get(
        f'http://api.openweathermap.org/geo/1.0/direct?q={city_name},{state_code},{country_code}&limit=1&appid={api_key}'
    )
    resp.raise_for_status()
    data = resp.json()
    if not data:
        raise ValueError('Location not found')
    lat = data[0].get('lat')
    lon = data[0].get('lon')
    return lat, lon

def get_current_weather(lat, lon, api_key):
    resp = requests.get(
        f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric'
    )
    resp.raise_for_status()
    response = resp.json()
    weather = response.get('weather', [{}])[0]
    data = WeatherData(
        main=weather.get('main'),
        description=weather.get('description'),
        icon=weather.get('icon'),
        temperature=response.get('main', {}).get('temp')
    )
    return data

def main(city_name, state_name, country_name):
    lat, lon = get_lat_lon(city_name, state_name, country_name, api_key)
    weather_data = get_current_weather(lat, lon, api_key)
    return weather_data

if __name__ == '__main__':
    lat, lon = get_lat_lon('Los Angeles', 'CA', 'US', api_key)
    print(get_current_weather(lat, lon, api_key))