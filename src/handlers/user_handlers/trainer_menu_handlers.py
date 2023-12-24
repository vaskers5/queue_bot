from datetime import datetime

from src.bot_singleton import UserSingleton

from src.options import check_current_user_state
from src.markups import generate_markup_from_list
from src.handlers.user_handlers.user_markups import get_start_markup


@UserSingleton.bot.message_handler(func=lambda message: message.text == "Привязаться к тренеру")
def handle_add_user_trainer(message):
    user_id = message.chat.id
    UserSingleton.manager.change_current_user_state(user_id, "add_trainer")
    UserSingleton.bot.send_message(user_id, "Введите телеграм ник тренера:")


@UserSingleton.bot.message_handler(func=lambda message: message.text == "Удалить привязку к тренеру")
def handle_delete_user_trainer_connection(message):
    user_id = message.chat.id
    # get user telegram nick
    user_tg_nick  = message.from_user.username
    UserSingleton.manager.change_current_user_state(user_id, "delete_user_trainer")
    text = "Выберите тренера, которого хотите удалить:"
    trainers = UserSingleton.manager.get_user_trainer(user_tg_nick)
    UserSingleton.bot.send_message(user_id, text, reply_markup=generate_markup_from_list(trainers))


@UserSingleton.bot.message_handler(func=lambda message: all([check_current_user_state(message.chat.id, "add_trainer"), message.text != "Назад"])) 
def handle_add_trainer_tg_nick(message):
    user_id = message.chat.id
    # get user telegram nick
    user_tg_nick  = message.from_user.username
    result_text = UserSingleton.manager.add_user_trainer(user_tg_nick, message.text)
    UserSingleton.manager.change_current_user_state(user_id, "start")
    UserSingleton.bot.send_message(user_id, result_text, reply_markup=get_start_markup())


@UserSingleton.bot.message_handler(func=lambda message: all([check_current_user_state(message.chat.id, "delete_user_trainer"), message.text != "Назад"])) 
def handle_delete_trainer_nick(message):
    user_id = message.chat.id
    # get user telegram nick
    user_tg_nick  = message.from_user.username
    result_text = UserSingleton.manager.delete_user_trainer(user_tg_nick, message.text)
    UserSingleton.manager.change_current_user_state(user_id, "start")
    UserSingleton.bot.send_message(user_id, result_text, reply_markup=get_start_markup())
