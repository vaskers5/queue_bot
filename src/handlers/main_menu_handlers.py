from src.bot_singleton import BotSingleton

from src.markups import get_start_markup, get_training_options_markup, get_fitness_club_markup


@BotSingleton.bot.message_handler(commands=['start'])
def handle_start(message):
    BotSingleton.bot.send_message(message.chat.id, "Выберите опцию:", reply_markup=get_start_markup())



@BotSingleton.bot.message_handler(func=lambda message: message.text == "Тренировки")
def handle_training_options(message):
    BotSingleton.bot.send_message(message.chat.id, "Выберите опцию:", reply_markup=get_training_options_markup())
    


@BotSingleton.bot.message_handler(func=lambda message: message.text == "Фитнес-клубы")
def handle_fitness_club_option(message):
    BotSingleton.bot.send_message(message.chat.id, "Выберите опцию:", reply_markup=get_fitness_club_markup())


@BotSingleton.bot.message_handler(func=lambda message: message.text == "Назад")
def handle_back_option(message):
    BotSingleton.manager.change_current_user_state(message.chat.id, "start")
    BotSingleton.bot.send_message(message.chat.id, "Выберите опцию для тренировок:", reply_markup=get_start_markup())

