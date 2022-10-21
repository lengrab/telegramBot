import os
import pickle
import telebot

from services.weatherService import WeatherService


class Session:
    def __init__(self, bot: telebot, weather_service: WeatherService):
        self.users = {}
        self.bot = bot
        self.weather_service = weather_service

    def save(self):
        with open('../data.pkl', 'wb') as outfile:
            pickle.dump(self.users, outfile)

    def load(self):
        if not os.path.exists('../data.pkl'):
            return None

        with open('../data.pkl', 'rb') as json_file:
            self.users = pickle.load(json_file)

        if self.users is None:
            self.users = {}
