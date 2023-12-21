from src.bot_singleton import TrainerSingleton

from src.handlers.user_handlers.user_markups import get_start_markup, get_training_options_markup, get_trainers_options_markup
from src.options import check_current_user_state




start_commands = set(["start", "/start","Тренировки", "Тренера"])


@TrainerSingleton.bot.message_handler(func=lambda message: all([not(message.text in start_commands), check_current_user_state(message.chat.id, "start")]))
def handle_user_wrong_message(message):
    TrainerSingleton.bot.send_message(message.chat.id, "Я не понимаю ваш запрос. Пожалуйста, попробуйте ещё раз или воспользуйтесь командами бота.")



@TrainerSingleton.bot.message_handler(commands=['start'])
def handle_user_start(message):
    TrainerSingleton.manager.change_current_user_state(message.chat.id, "start")
    TrainerSingleton.bot.send_message(message.chat.id, "Выберите опцию:", reply_markup=get_start_markup())



@TrainerSingleton.bot.message_handler(func=lambda message: all([message.text == "Тренировки", check_current_user_state(message.chat.id, "start")]))
def handle_user_training_options(message):
    TrainerSingleton.bot.send_message(message.chat.id, "Выберите опцию:", reply_markup=get_training_options_markup())
    


@TrainerSingleton.bot.message_handler(func=lambda message: all([message.text == "Тренера", check_current_user_state(message.chat.id, "start")]))
def handle_user_fitness_club_option(message):
    TrainerSingleton.bot.send_message(message.chat.id, "Выберите опцию:", reply_markup=get_trainers_options_markup())


@TrainerSingleton.bot.message_handler(func=lambda message: message.text == "Назад")
def handle_user_back_option(message):
    TrainerSingleton.manager.change_current_user_state(message.chat.id, "start")
    TrainerSingleton.bot.send_message(message.chat.id, "Выберите опцию:", reply_markup=get_start_markup())

