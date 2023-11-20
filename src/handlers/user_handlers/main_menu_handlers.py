from src.bot_singleton import BotSingleton

from src.handlers.user_handlers.user_markups import get_start_markup, get_training_options_markup, get_trainers_options_markup
from src.options import check_current_user_state




start_commands = set(["start", "/start","Тренировки", "Тренера"])


@BotSingleton.bot.message_handler(func=lambda message: all([not(message.text in start_commands), check_current_user_state(message.chat.id, "start")]))
def handle_wrong_message(message):
    BotSingleton.bot.send_message(message.chat.id, "Я не понимаю ваш запрос. Пожалуйста, попробуйте ещё раз или воспользуйтесь командами бота.")



@BotSingleton.bot.message_handler(commands=['start'])
def handle_start(message):
    BotSingleton.manager.change_current_user_state(message.chat.id, "start")
    BotSingleton.bot.send_message(message.chat.id, "Выберите опцию:", reply_markup=get_start_markup())



@BotSingleton.bot.message_handler(func=lambda message: all([message.text == "Тренировки", check_current_user_state(message.chat.id, "start")]))
def handle_training_options(message):
    BotSingleton.bot.send_message(message.chat.id, "Выберите опцию:", reply_markup=get_training_options_markup())
    


@BotSingleton.bot.message_handler(func=lambda message: all([message.text == "Тренера", check_current_user_state(message.chat.id, "start")]))
def handle_fitness_club_option(message):
    BotSingleton.bot.send_message(message.chat.id, "Выберите опцию:", reply_markup=get_trainers_options_markup())


@BotSingleton.bot.message_handler(func=lambda message: message.text == "Назад")
def handle_back_option(message):
    BotSingleton.manager.change_current_user_state(message.chat.id, "start")
    BotSingleton.bot.send_message(message.chat.id, "Выберите опцию:", reply_markup=get_start_markup())

