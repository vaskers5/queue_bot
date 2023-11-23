from datetime import datetime

from src.bot_singleton import BotSingleton

from src.options import check_current_user_state
from src.markups import generate_markup_from_list, get_start_markup


@BotSingleton.bot.message_handler(func=lambda message: message.text == "Привязаться к тренеру")
def handle_add_user_trainer(message):
    user_id = message.chat.id
    BotSingleton.manager.change_current_user_state(user_id, "add_trainer")
    BotSingleton.bot.send_message(user_id, "Введите телеграм ник тренера:")


@BotSingleton.bot.message_handler(func=lambda message: message.text == "Удалить привязку к тренеру")
def handle_delete_user_trainer_connection(message):
    user_id = message.chat.id
    # get user telegram nick
    user_tg_nick  = message.from_user.username
    BotSingleton.manager.change_current_user_state(user_id, "delete_user_trainer")
    text = "Выберите тренера, которого хотите удалить:"
    trainers = BotSingleton.manager.get_user_trainer(user_tg_nick)
    BotSingleton.bot.send_message(user_id, text, reply_markup=generate_markup_from_list(trainers))


@BotSingleton.bot.message_handler(func=lambda message: all([check_current_user_state(message.chat.id, "add_trainer"), message.text != "Назад"])) 
def handle_add_trainer_tg_nick(message):
    user_id = message.chat.id
    # get user telegram nick
    user_tg_nick  = message.from_user.username
    result_text = BotSingleton.manager.add_user_trainer(user_tg_nick, message.text)
    BotSingleton.manager.change_current_user_state(user_id, "start")
    BotSingleton.bot.send_message(user_id, result_text, reply_markup=get_start_markup())


@BotSingleton.bot.message_handler(func=lambda message: all([check_current_user_state(message.chat.id, "delete_user_trainer"), message.text != "Назад"])) 
def handle_delete_trainer_nick(message):
    user_id = message.chat.id
    # get user telegram nick
    user_tg_nick  = message.from_user.username
    result_text = BotSingleton.manager.delete_user_trainer(user_tg_nick, message.text)
    BotSingleton.manager.change_current_user_state(user_id, "start")
    BotSingleton.bot.send_message(user_id, result_text, reply_markup=get_start_markup())
