from datetime import datetime

from src.bot_singleton import TrainerSingleton

from src.options import check_current_user_state
from src.markups import generate_markup_from_list, get_start_markup


@TrainerSingleton.bot.message_handler(func=lambda message: message.text == "Добавить новое место")
def handle_add_place(message):
    user_id = message.chat.id
    TrainerSingleton.manager.change_current_user_state(user_id, "add_place")
    TrainerSingleton.bot.send_message(user_id, "Введите название места тренировки:")


@TrainerSingleton.bot.message_handler(func=lambda message: message.text == "Удалить место")
def handle_delete_place(message):
    user_id = message.chat.id
    all_user_places = TrainerSingleton.manager.get_user_places(user_id)
    places_data = {place.name: place.place_id for place in all_user_places}
    if places_data:
        TrainerSingleton.manager.change_current_user_state(user_id, "delete_place", state_info=places_data)
        markup = generate_markup_from_list([place.name for place in all_user_places])
        TrainerSingleton.bot.send_message(user_id, "Выберите место, которое хотите удалить", reply_markup=markup)
    else:
        TrainerSingleton.bot.send_message(user_id, "У вас нет мест для тренировок. Добавьте их в настройках.", reply_markup=get_start_markup())


@TrainerSingleton.bot.message_handler(func=lambda message: message.text == "Мои места")
def handle_get_all_user_places(message):
    user_id = message.chat.id
    all_user_places = TrainerSingleton.manager.get_user_places(user_id)
    if all_user_places:
        msg = "Ваши места:\n"
        msg += "\n".join([place.name for place in all_user_places])
        TrainerSingleton.bot.send_message(user_id, msg)
    else:
        TrainerSingleton.bot.send_message(user_id, "У вас нет мест для тренировок. Добавьте их в настройках.", reply_markup=get_start_markup())


@TrainerSingleton.bot.message_handler(func=lambda message: all([check_current_user_state(message.chat.id, "add_place"), message.text != "Назад"])) 
def handle_write_new_place_name(message):
    user_id = message.chat.id
    TrainerSingleton.manager.add_user_place(user_id, message.text)
    TrainerSingleton.manager.change_current_user_state(user_id, "start")
    text = f"Место {message.text} успешно добавлено"
    TrainerSingleton.bot.send_message(user_id, text, reply_markup=get_start_markup())


@TrainerSingleton.bot.message_handler(func=lambda message: all([check_current_user_state(message.chat.id, "delete_place"), message.text != "Назад"])) 
def handle_write_deleted_place_name(message):
    user_id = message.chat.id
    last_state = TrainerSingleton.manager.get_current_user_state(user_id)
    places_dict = last_state["state_info"]
    if not (message.text in places_dict):
        TrainerSingleton.bot.send_message(user_id, "Вы здесь не занимаетесь!", reply_markup=get_start_markup())
    else:
        place_id = places_dict[message.text]
        last_state = TrainerSingleton.manager.delete_user_place(user_id, place_id)
        TrainerSingleton.manager.change_current_user_state(user_id, "start")
        TrainerSingleton.bot.send_message(user_id, f"Место {message.text} успешно удалено", reply_markup=get_start_markup())
