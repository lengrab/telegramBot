from telebot import types
from bot_commands.bot_callbacks import Callbacks


class WeatherKeyboards:
    @classmethod
    def get_base_keyboard(cls):
        inline_keyboard = types.InlineKeyboardMarkup(row_width=2)
        item_btn_1 = types.InlineKeyboardButton('Узнать погоду', callback_data=Callbacks.GET_WEATHER)
        item_btn_2 = types.InlineKeyboardButton('Сменить домашний город', callback_data=Callbacks.CHANGE_CITY)
        item_btn_3 = types.InlineKeyboardButton('About_author', callback_data=Callbacks.ABOUT_AUTHOR)
        inline_keyboard.row(item_btn_1, item_btn_2)
        inline_keyboard.row(item_btn_3)
        return inline_keyboard

    @classmethod
    def get_back_keyboard(cls):
        inline_keyboard = types.InlineKeyboardMarkup()
        item_btn_1 = types.InlineKeyboardButton('Назад', callback_data=Callbacks.BACK)
        inline_keyboard.row(item_btn_1)
        return inline_keyboard
