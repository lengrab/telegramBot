import json
import requests

from model.open_weather import City as City
from model.open_weather import WeatherResponse as Weather

from functools import lru_cache

URL = 'http://api.openweathermap.org/'

URL_GEO_POSTFIX = 'geo/1.0/direct?'
URL_WEATHER_POSTFIX = 'data/2.5/weather?'

FROM_KELVIN = 273.15


class WeatherService:
    def __init__(self, token):
        self.token = token

    def get_about_weather(self, city: str):
        weather = self.get_weather(city)
        city = self.get_location(city)

        temp = round(weather.main.temp - FROM_KELVIN, 2)
        pressure = weather.main.pressure
        wind_speed = round(weather.wind.speed, 2)

        return f"Погода в городе {city[0].local_names['ru']}:\n🌡  Температура: {temp} °C\n📟  Давление: {pressure} Па\n💨  Скорость ветра: {wind_speed} м/c."

    @lru_cache(maxsize=100)
    def get_weather(self, city: str):
        cities = self.get_location(city)

        print(cities)

        if len(cities) < 1:
            return

        url = f'{URL}{URL_WEATHER_POSTFIX}lat={cities[0].lat}&lon={cities[0].lon}&appid={self.token}'
        request = requests.get(url)

        if request.status_code == 200:
            return Weather.from_json(json.loads(request.text))
        else:
            return None

    @lru_cache(maxsize=100)
    def get_location(self, city: str):
        url = f'{URL}{URL_GEO_POSTFIX}q={city}&appid={self.token}'
        request = requests.get(url)

        if request.status_code == 200:
            cities = []
            for city in json.loads(request.text):
                cities.append(City.from_json(city))
            return cities
        else:
            return None
