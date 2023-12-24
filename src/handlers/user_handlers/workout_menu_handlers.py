from datetime import datetime

from src.bot_singleton import UserSingleton, TrainerSingleton

from src.options import check_current_user_state
from src.markups import generate_markup_from_list
from src.handlers.user_handlers.user_markups import get_start_markup


@UserSingleton.bot.message_handler(func=lambda message: message.text == "Занять слот")
def handle_user_take_slot(message):
    user_id = message.chat.id
    UserSingleton.manager.change_current_user_state(user_id, "take_slot")
    trainers = UserSingleton.manager.get_user_trainer(message.from_user.username)
    UserSingleton.bot.send_message(user_id, "Выберите тренера, к которому вы хотите записаться:", reply_markup=generate_markup_from_list(trainers))


@UserSingleton.bot.message_handler(func=lambda message: all([check_current_user_state(message.chat.id, "take_slot"), message.text != "Назад"])) 
def handle_user_choose_trainer(message):
    user_id = message.chat.id
    # get user telegram nick
    user_tg_nick  = message.from_user.username
    check_trainer = UserSingleton.manager.check_trainer(trainer_nick=message.text, user_nick=user_tg_nick)
    if not check_trainer:
        UserSingleton.bot.send_message(user_id, "Вы не записаны к этому тренеру!")
    else:
        trainer_slots = UserSingleton.manager.get_trainer_slots(message.text)
        if len(trainer_slots) == 0:
            UserSingleton.bot.send_message(user_id, "У тренера нет свободных слотов!")
        else:
            slots_data = {str(slot): slot.__dict__() for slot in trainer_slots}
            UserSingleton.manager.change_current_user_state(user_id, "selected_trainer", state_info={"trainer": message.text, "slots": slots_data})
            UserSingleton.bot.send_message(user_id, "Выберите свободный слот:", reply_markup=generate_markup_from_list([str(slot) for slot in trainer_slots]))

    
@UserSingleton.bot.message_handler(func=lambda message: all([check_current_user_state(message.chat.id, "selected_trainer"), message.text != "Назад"])) 
def handle_user_choose_trainer(message):
    user_id = message.chat.id
    # get user telegram nick
    user_tg_nick  = message.from_user.username
    user_state = UserSingleton.manager.get_current_user_state(user_id)
    if not(message.text in user_state["state_info"]["slots"]):
        UserSingleton.bot.send_message(user_id, "Вы выбрали некорректный слот!")
    else:
        slot_data = user_state["state_info"]["slots"][message.text]
        UserSingleton.manager.add_user_to_slot(user_tg=user_tg_nick, slot=slot_data)
        UserSingleton.manager.change_current_user_state(user_id, "start")
        # Send notification to trainer/ todo fix time format
        UserSingleton.bot.send_message(chat_id=slot_data["trainer_id"], text=f"@{user_tg_nick} занял слот на {slot_data['start_time']}-{slot_data['end_time']} в {slot_data['place_name']}")
        UserSingleton.bot.send_message(user_id, "Вы успешно записаны на слот.", reply_markup=get_start_markup())


def get_user_slots_repr(tg_nick: str):
    booked_slots =  UserSingleton.manager.get_user_booked_slots(tg_nick)
    print(booked_slots)
    data = {}
    current_datetime = datetime.now()
    for slot in booked_slots:
        start_time = datetime.strptime(slot["start_time"], '%Y-%m-%d %H:%M:%S')
        if start_time > current_datetime:
            key = f'{slot["start_time"]} - {slot["end_time"]} {slot["trainer_nickname"]} {slot["place_name"]}'
            data[key] = slot
    return data
# handle_user_choose_slot, handle_user_delete_slot
@UserSingleton.bot.message_handler(func=lambda message: message.text == "Удалить запись")
def handle_user_delete_slot(message):
    # get user telegram nick
    user_id = message.chat.id
    user_tg_nick  = message.from_user.username
    slots_data = get_user_slots_repr(user_tg_nick)
    UserSingleton.manager.change_current_user_state(user_id, "start")
    if len(slots_data) == 0:
        UserSingleton.bot.send_message(user_id, "У вас нет записей на занятия!")
    else:
        UserSingleton.manager.change_current_user_state(user_id, "choose_slot", state_info={"slots": slots_data})
        slots_markup = generate_markup_from_list([key for key in slots_data])
        UserSingleton.bot.send_message(user_id, "Выберите слот для отмены записи:", reply_markup=slots_markup)


@UserSingleton.bot.message_handler(func=lambda message: all([check_current_user_state(message.chat.id, "choose_slot"), message.text != "Назад"]))
def handle_user_choose_slot(message):
    """
    Подтверждает удаление записи пользователя со слота.

    Args:
        user_id: Идентификатор пользователя.
        slot_id: Идентификатор слота.
    """

    user_id = message.chat.id
    # get user telegram nick
    user_tg_nick  = message.from_user.username
    user_state = UserSingleton.manager.get_current_user_state(user_id)
    
    if message.text in user_state["state_info"]["slots"]:
        slot_data = user_state["state_info"]["slots"][message.text]
        cancel_booking(user_id, slot_data)
        UserSingleton.bot.send_message(user_id, f"Запись на слот {message.text} успешно отменена!")
        UserSingleton.manager.change_current_user_state(user_id, "start")
        # Send notification to trainer
        # UserSingleton.bot.send_message(chat_id=slot_data["trainer_nickname"], text=f"User {user_id} has canceled the booking for {slot_data['start_time']}-{slot_data['end_time']} at {slot_data['place_name']}")
    else:
        UserSingleton.bot.send_message(user_id, "Вы ввели неправильный слот")



def cancel_booking(user_id, slot_data: dict[str, str]):
    """
    Удаляет запись пользователя со слота.

    Args:
        user_id: Идентификатор пользователя.
        slot_id: Идентификатор слота.
    """

    UserSingleton.manager.cancel_booking(slot_data)
    UserSingleton.bot.send_message(user_id, f"Запись на слот успешно отменена!", reply_markup=get_start_markup())


