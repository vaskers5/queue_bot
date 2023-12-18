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
        if len(trainer_slots) == 0:
            BotSingleton.bot.send_message(user_id, "У тренера нет свободных слотов!")
        else:
            slots_data = {str(slot): slot.__dict__() for slot in trainer_slots}
            BotSingleton.manager.change_current_user_state(user_id, "selected_trainer", state_info={"trainer": message.text, "slots": slots_data})
            BotSingleton.bot.send_message(user_id, "Выберите свободный слот:", reply_markup=generate_markup_from_list([str(slot) for slot in trainer_slots]))

    
@BotSingleton.bot.message_handler(func=lambda message: all([check_current_user_state(message.chat.id, "selected_trainer"), message.text != "Назад"])) 
def handle_user_choose_trainer(message):
    user_id = message.chat.id
    # get user telegram nick
    user_tg_nick  = message.from_user.username
    user_state = BotSingleton.manager.get_current_user_state(user_id)
    if not(message.text in user_state["state_info"]["slots"]):
        BotSingleton.bot.send_message(user_id, "Вы выбрали некорректный слот!")
    else:
        slot_data = user_state["state_info"]["slots"][message.text]
        # Send notification to trainer
        trainer_nick = self.trainers_table.get(Query().id == slot["trainer_id"])["tg_id"]
        BotSingleton.bot.send_message(chat_id=trainer_nick, text=f"User {user_tg_nick} has booked a slot for {slot_data['start_time']}-{slot_data['end_time']} at {slot_data['place_name']}")


@BotSingleton.bot.message_handler(func=lambda message: message.text == "Удалить слот")
def show_and_handle_user_booked_slots(message):
    """
    Отображает пользователю список слотов, на которые он записан, и обрабатывает сообщение пользователя о желании отменить запись.

    Args:
        user_id: Идентификатор пользователя.
    """
    user_id = message.chat.id
    # get user telegram nick
    user_tg_nick  = message.from_user.username
    booked_slots =  BotSingleton.manager.get_user_booked_slots(user_id)
    if len(booked_slots) == 0:
        BotSingleton.bot.send_message(user_id, "У вас нет записей на занятия!")
    else:
        slots_data = {str(slot): slot.__dict__() for slot in booked_slots}
        slots_markup = generate_markup_from_list([str(slot) for slot in booked_slots])
        BotSingleton.bot.send_message(user_id, "Выберите слот для отмены записи:", reply_markup=slots_markup)

        while True:
            message = BotSingleton.bot.get_updates()[0]
            user_id = message.chat.id
            if message.text == "Назад":
                BotSingleton.manager.change_current_user_state(user_id, "main")
                break

            slot_id = message.text
            if slot_id not in slots_data:
                BotSingleton.bot.send_message(user_id, "Вы не записаны на этот слот!")
                continue

            cancel_booking(user_id, slot_id)
            break
            
        # Send notification to trainer
        slot_data = slots_data[slot_id]
        trainer_id = slot_data["trainer_id"]
        trainer_tg = self.trainers_table.get(Query().id == trainer_id)["tg_id"]
        BotSingleton.bot.send_message(chat_id=trainer_tg, text=f"User {user_id} has canceled the booking for {slot['start_time']}-{slot['end_time']} at {slot['place_name']}")


def cancel_booking(user_id, slot_id):
    """
    Удаляет запись пользователя со слота.

    Args:
        user_id: Идентификатор пользователя.
        slot_id: Идентификатор слота.
    """

    BotSingleton.manager.cancel_booking(user_id, slot_id)
    BotSingleton.bot.send_message(user_id, f"Запись на слот {slot_id} успешно отменена!")


