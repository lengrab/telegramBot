from telebot.types import Message, CallbackQuery
from services.weather_keyboard import WeatherKeyboards
from sessinon import Session


class State:
    def __init__(self, contex: Session):
        self.name = self.__class__.__name__
        self.contex = contex

    def handle(self, event):
        pass


class AboutAuthorState(State):
    def handle(self, event):
        if isinstance(event, CallbackQuery):
            self.contex.users[event.from_user.id].state = self.name
            call = event
            self.contex.bot.send_message(call.message.chat.id,
                                         "Привет! Я @leonidgrabovskij941 - автор погодного бота.",
                                         reply_markup=WeatherKeyboards.get_back_keyboard())
            self.contex.bot.delete_message(chat_id=event.message.chat.id, message_id=event.message.message_id)


class BaseState(State):
    def handle(self, event):
        if isinstance(event, Message):
            chat_id = event.chat.id
            message_id = event.message_id
        elif isinstance(event, CallbackQuery):
            chat_id = event.message.chat.id
            message_id = event.message.message_id

        self.contex.users[event.from_user.id].state = self.name
        self.contex.bot.send_message(chat_id,
                                     "Привет! Я погодный бот и я умею выполнять следующие действия:",
                                     reply_markup=WeatherKeyboards.get_base_keyboard())
        self.contex.bot.delete_message(chat_id=chat_id, message_id=message_id)


class ChangeCityState(State):
    def handle(self, event):
        self.contex.users[event.from_user.id].state = self.name

        if isinstance(event, CallbackQuery):
            self.contex.users[event.from_user.id].cached_message = self.contex.bot.send_message(event.message.chat.id,
                                                                                                "Укажи свой домашний город:")
            self.contex.bot.delete_message(chat_id=event.message.chat.id, message_id=event.message.message_id)

        elif isinstance(event, Message):
            cities = self.contex.weather_service.get_location(event.text)
            chat_id = event.chat.id
            self.contex.bot.delete_message(chat_id=event.chat.id, message_id=event.message_id)
            cached_message = self.contex.users[event.from_user.id].cached_message

            if cached_message is not None:
                self.contex.bot.delete_message(chat_id=cached_message.chat.id, message_id=cached_message.message_id)
                self.contex.users[event.from_user.id].cached_message = None

            if cities is None:
                self.contex.bot.send_message(chat_id,
                                             f"Не удалось найти город {event.text}, попробуй еще:",
                                             reply_markup=WeatherKeyboards.get_back_keyboard())
            else:
                user_id = event.from_user.id
                self.contex.users[user_id].city = cities[0].name
                self.contex.users[user_id].state = BaseState(self.contex)
                self.contex.bot.send_message(chat_id, f"Домашний город изменен на - {event.text}.",
                                             reply_markup=WeatherKeyboards.get_back_keyboard())
                self.contex.bot.delete_message(chat_id=event.chat.id, message_id=event.message_id)


class WeatherInfoState(State):
    def handle(self, event):
        if isinstance(event, CallbackQuery):
            self.contex.users[event.from_user.id].state = self.name
            user_city = self.contex.users[event.from_user.id].city
            self.contex.bot.send_message(event.message.chat.id,
                                         self.contex.weather_service.get_about_weather(user_city),
                                         reply_markup=WeatherKeyboards.get_back_keyboard())

            self.contex.bot.delete_message(chat_id=event.message.chat.id, message_id=event.message.message_id)
