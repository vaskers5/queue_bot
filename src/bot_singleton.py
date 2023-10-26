import telebot

from src.manager import BotManager

class BotSingleton(object):
    bot = telebot.TeleBot("1923472646:AAHrWfdgLlRP3FRzRn-xWx09f5WM_mfBXHQ")
    manager = BotManager()
    def __new__(class_, *args, **kwargs):
        if not isinstance(class_.bot, class_):
            class_.bot = object.__new__(class_, *args, **kwargs)
        return class_.bot
