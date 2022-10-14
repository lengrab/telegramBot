import telebot
from telebot import types

TOKEN = "5440142515:AAFJKnKnBiL3Ap0FYP_hdx9mB4gH2F-f5WI"

bot = telebot.TeleBot(TOKEN)

markup = types.ReplyKeyboardMarkup(row_width=2)
item_btn_1 = types.KeyboardButton('Start')
item_btn_2 = types.KeyboardButton('Help')
item_btn_3 = types.KeyboardButton('About_author')
markup.add(item_btn_1, item_btn_2, item_btn_3)

inline_keyboard = types.InlineKeyboardMarkup(row_width=2)
item_btn_1 = types.InlineKeyboardButton('Start', callback_data='/start')
item_btn_2 = types.InlineKeyboardButton('Help', callback_data='/help')
item_btn_3 = types.InlineKeyboardButton('About_author', callback_data='/about_author')
inline_keyboard.row(item_btn_1,item_btn_2)
inline_keyboard.row(item_btn_3)
# inline_keyboard.add(item_btn_1, item_btn_2, item_btn_3)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    # bot.delete_message(message.chat.id, message.id)
    bot.send_message(message.chat.id, "Привет! Я умею следующие действия:", reply_markup=inline_keyboard)

@bot.callback_query_handler(func=lambda call: True)
def handle(call):
    # bot.send_message(call.message.chat.id, 'Data: {}'.format(str(call.data)))
    if call.data == '/about_author':
        bot.send_message(call.message.chat.id, 'Hi! My name is Leonid. I\'m author this channel.')
    if call.data == '/help':
        bot.send_message(call.message.chat.id, 'How can I help you?')
    bot.answer_callback_query(call.id)



# @bot.message_handler(commands=['help'])
# def send_welcome(message):
#     bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.send_message(message.chat.id, "text", reply_markup=inline_keyboard)


@bot.message_handler(commands=['about_author'])
def send_about(message):
    bot.send_message(message.chat.id, 'Hi! My name is Leonid. I\'m author this channel.')


# @bot.message_handler(func=lambda message: True)
# def echo_all(message):
#  	bot.reply_to(message, message.text)

# @bot.message_handler(func=lambda message: True)
# def echo_all(message):
#  	bot.send_message(message.chat.id, message.text)

bot.infinity_polling()
input()
