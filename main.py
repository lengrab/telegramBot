import logging
from telebot import types
import flask
import telebot

API_TOKEN = '5647507123:AAEP5rpQ2w2Ap6Ij4zG09V6lL8HYuxjISjc'
WEBHOOK_PORT = 8444
WEBHOOK_HOST = '127.0.0.1'
WEBHOOK_URL = 'https://fb39-94-25-224-16.eu.ngrok.io'

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)
bot = telebot.TeleBot(API_TOKEN)
app = flask.Flask(__name__)

inline_keyboard = types.InlineKeyboardMarkup(row_width=2)
item_btn_1 = types.InlineKeyboardButton('Start', callback_data='/start')
item_btn_2 = types.InlineKeyboardButton('Help', callback_data='/help')
item_btn_3 = types.InlineKeyboardButton('About_author', callback_data='/about_author')
inline_keyboard.row(item_btn_1, item_btn_2)
inline_keyboard.row(item_btn_3)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Привет! Я умею следующие действия:", reply_markup=inline_keyboard)


@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message,
                 ("Hi there, I am EchoBot.\n"
                  "I am here to echo your kind words back to you."))


@bot.callback_query_handler(func=lambda call: True)
def handle(call):
    # bot.send_message(call.message.chat.id, 'Data: {}'.format(str(call.data)))
    if call.data == '/about_author':
        bot.send_message(call.message.chat.id, 'Hi! My name is Leonid. I\'m author this channel.')
    if call.data == '/help':
        bot.send_message(call.message.chat.id, 'How can I help you?')
    bot.answer_callback_query(call.id)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    bot.reply_to(message, message.text)


# Process webhook calls
@app.route('/' + API_TOKEN, methods=['POST'])
def webhook():
    logger.debug(flask.request.get_data())
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')

        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return '200'
    else:
        flask.abort(403)


bot.remove_webhook()
bot.set_webhook(WEBHOOK_URL + "/" + API_TOKEN)
app.run(host=WEBHOOK_HOST, port=WEBHOOK_PORT)
