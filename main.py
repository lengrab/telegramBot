import importlib
import logging
import flask
import telebot
from telebot.types import CallbackQuery, Message

import config
from model.bot_callbacks import Callbacks
from services.weatherService import WeatherService
from sessinon import Session
from states.state import State, BaseState, AboutAuthorState, ChangeCityState, WeatherInfoState

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)
bot = telebot.TeleBot(config.API_TOKEN)
app = flask.Flask(__name__)
weather_service = WeatherService(config.OPENWEATHER_TOKEN)


class User:
    def __init__(self, id, city, state: State):
        self.id = id
        self.city = city
        self.state = state.name
        self.cached_message = None


session = Session(bot, weather_service)
session.load()


def create_state_for_user(context: Session, id: int):
    args = ()
    kw = {"contex": session}
    module = importlib.import_module('states.state')
    klass = getattr(module, context.users[id].state)
    state = klass(*args, **kw)
    return state


@bot.message_handler(commands=['start'])
def send_welcome(message: Message):
    user_id = message.from_user.id

    if user_id not in session.users:
        session.users[user_id] = User(user_id, 'Москва', BaseState(session))

    state = create_state_for_user(session, user_id)
    state.handle(message)
    bot.delete_message(chat_id=message.chat.id, message_id=message.id)


@bot.message_handler(func=lambda message: True)
def handle_message(message: Message):
    state = create_state_for_user(session, message.from_user.id)
    state.handle(message)
    bot.delete_message(chat_id=message.chat.id, message_id=message.id)


@bot.callback_query_handler(func=lambda call: True)
def handle(call: CallbackQuery):
    state = BaseState(session)

    if call.data == Callbacks.GET_WEATHER:
        state = WeatherInfoState(session)

    elif call.data == Callbacks.CHANGE_CITY:
        state = ChangeCityState(session)
        session.users[call.from_user.id].state = state

    elif call.data == Callbacks.ABOUT_AUTHOR:
        state = AboutAuthorState(session)

    elif call.data == Callbacks.BACK:
        state = BaseState(session)

    state.handle(call)
    bot.answer_callback_query(call.id)


@app.route('/' + config.API_TOKEN, methods=['POST'])
def webhook():
    logger.debug(flask.request.get_data())

    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        session.save()
        return '200'
    else:
        flask.abort(403)


bot.remove_webhook()
bot.set_webhook(config.WEBHOOK_URL + "/" + config.API_TOKEN)
app.run(host=config.WEBHOOK_HOST, port=config.WEBHOOK_PORT)
