from datetime import datetime

from src.bot_singleton import BotSingleton

from src.options import check_current_user_state
from src.markups import generate_markup_from_list, get_start_markup


@BotSingleton.bot.message_handler(func=lambda message: message.text == "Занять слот")
def handle_user_take_slot(message):
    user_id = message.chat.id
    BotSingleton.manager.change_current_user_state(user_id, "take_slot")
    trainers = BotSingleton.manager.get_user_trainer(message.from_user.username)
    BotSingleton.bot.send_message(user_id, "Выберите тренера, к которому вы хотите записаться:", reply_markup=generate_markup_from_list(trainers))


@BotSingleton.bot.message_handler(func=lambda message: all([check_current_user_state(message.chat.id, "take_slot"), message.text != "Назад"])) 
def handle_user_choose_trainer(message):
    user_id = message.chat.id
    # get user telegram nick
    user_tg_nick  = message.from_user.username
    check_trainer = BotSingleton.manager.check_trainer(trainer_nick=message.text, user_nick=user_tg_nick)
    if not check_trainer:
        BotSingleton.bot.send_message(user_id, "Вы не записаны к этому тренеру!")
    else:
        trainer_slots = BotSingleton.manager.get_trainer_slots(message.text)
    


# @BotSingleton.bot.message_handler(func=lambda message: message.text == "delete_slot")
# def handle_delete_user_trainer_connection(message):
#     user_id = message.chat.id
#     # get user telegram nick
#     user_tg_nick  = message.from_user.username
#     BotSingleton.manager.change_current_user_state(user_id, "delete_user_trainer")
#     text = "Выберите тренера, которого хотите удалить:"
#     trainers = BotSingleton.manager.get_user_trainer(user_tg_nick)
#     BotSingleton.bot.send_message(user_id, text, reply_markup=generate_markup_from_list(trainers))


# @BotSingleton.bot.message_handler(func=lambda message: all([check_current_user_state(message.chat.id, "delete_user_trainer"), message.text != "Назад"])) 
# def handle_delete_trainer_nick(message):
#     user_id = message.chat.id
#     # get user telegram nick
#     user_tg_nick  = message.from_user.username
#     result_text = BotSingleton.manager.delete_user_trainer(user_tg_nick, message.text)
#     BotSingleton.manager.change_current_user_state(user_id, "start")
#     BotSingleton.bot.send_message(user_id, result_text, reply_markup=get_start_markup())
