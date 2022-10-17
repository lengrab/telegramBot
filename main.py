import logging
import time

import flask
import telebot

API_TOKEN = ''
WEBHOOK_PORT = 8444
WEBHOOK_HOST = '127.0.0.1'
WEBHOOK_URL = 'https://3eec-77-93-112-174.eu.ngrok.io'

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)
bot = telebot.TeleBot(API_TOKEN)
app = flask.Flask(__name__)
time.sleep(0.1)


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message,
                 ("Hi there, I am EchoBot.\n"
                  "I am here to echo your kind words back to you."))


@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    bot.reply_to(message, message.text)


# Process webhook calls
@app.route('/' + API_TOKEN, methods=['POST', 'GET'])
def webhook():
    logger.debug("gas")
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
app.run(host=WEBHOOK_HOST,
        port=WEBHOOK_PORT)
