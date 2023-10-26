from datetime import datetime

from src.bot_singleton import BotSingleton

from src.options import generate_calendar_for_two_weeks, validate_time
from src.markups import generate_markup_from_list, get_day_hours_markup, get_start_markup


def check_current_user_state(chat_id: str, state: str) -> bool:
    return BotSingleton.manager.get_current_user_state(chat_id)["state"] == state


@BotSingleton.bot.message_handler(func=lambda message: message.text == "Запланировать тренировку")
def handle_workout_date(message):
    str_dates, dates = generate_calendar_for_two_weeks()
    markup = generate_markup_from_list(str_dates)
    BotSingleton.manager.change_current_user_state(message.chat.id, "plan_workout", state_info={k: v for k, v in zip(str_dates, dates)})
    BotSingleton.bot.send_message(message.chat.id, "Выберите удобную вам дату:", reply_markup=markup)


@BotSingleton.bot.message_handler(func=lambda message: all([check_current_user_state(message.chat.id, "selected_day"), message.text == "Назад"])) 
def handle_workout_place(message):
    user_id = message.chat.id
    last_state = BotSingleton.manager.get_current_user_state_info(user_id)
    workout_date = last_state["state_info"][message.text]
    BotSingleton.manager.change_current_user_state(user_id, "selected_day", state_info={"date": workout_date})
    user_places = BotSingleton.manager.get_user_places(user_id)
    if len(user_places) == 0:
        BotSingleton.change_current_user_state(user_id, "start")
        return BotSingleton.bot.send_message(user_id, "У вас нет мест для тренировок. Добавьте их в настройках.", reply_markup=get_start_markup())
    places_data = [{place.name: place} for place in user_places]
    BotSingleton.manager.change_current_user_state(user_id, "enter_place", state_info={"places": places_data, "date": workout_date})
    return BotSingleton.bot.send_message(user_id, "Выберите место тренировки:", reply_markup=generate_markup_from_list([list(place.keys())[0] for place in places_data]))


@BotSingleton.bot.message_handler(func=lambda message: all([check_current_user_state(message.chat.id, "enter_place"), message.text != "Назад"]))
def handle_workout_time(message):
    user_id = message.chat.id
    last_state = BotSingleton.manager.get_current_user_state_info(user_id)
    text_place = message.text
    workout_date = last_state["state_info"]["date"]
    if text_place in last_state["state_info"]["places"]:
        workout_place = last_state["state_info"]["places"][message.text]
    else:
        BotSingleton.manager.change_current_user_state(user_id, "selected_day")
        text_msg = "Выберите место из предложенных нами. Если вашего место нет в списке - добавьте его на начальном экране"
        return BotSingleton.bot.send_message(user_id, text_msg)
    
    BotSingleton.manager.change_current_user_state(user_id, "selected_place", state_info={"date": workout_date, "place": workout_place})
    text = f"Вы выбрали день {message.text}. Теперь введите время начала и конца тренировки (например, 09:00-10:00). Вы можете использовать заготовленные нами варианты, или задать сами введя текст:",
    return BotSingleton.bot.send_message(user_id, text, reply_markup=get_day_hours_markup())


@BotSingleton.bot.message_handler(func=lambda message: all([check_current_user_state(message.chat.id, "selected_place"), message.text != "Назад"]))
def handle_entered_time(message):
    user_id = message.chat.id
    if not validate_time(message.text):
        BotSingleton.manager.change_current_user_state(user_id, "enter_place")
        text_msg = "Задайте время в формате hh:mm-hh.mm. Например 10:00-11:00"
        return BotSingleton.bot.send_message(user_id, text_msg)
    
    start_time, end_time = message.text.split("-")
    last_state = BotSingleton.manager.get_current_user_state_info(user_id)
    workout_start_time = datetime.combine(last_state["state_info"]["date"], datetime.strptime(start_time, '%H:%M').time())
    workout_end_time = datetime.combine(last_state["state_info"]["date"], datetime.strptime(end_time, '%H:%M').time())
    BotSingleton.manager.change_current_user_state(user_id, "entered_time", 
                                                state_info={"start_time": workout_start_time, "end_time": workout_end_time,
                                                            "place": last_state["state_info"]["place"]})
    markup = generate_markup_from_list(["Свободный слот", "Занятый слот", "Постоянный слот", "Назад"])
    confirmation_msg = f"Итоговая информация: {last_state['state_info']['place'].name}, {start_time}-{end_time}. Выберите тип слота:"
    return BotSingleton.bot.send_message(user_id, confirmation_msg, reply_markup=markup)


@BotSingleton.bot.message_handler(func=lambda message: all([check_current_user_state(message.chat.id, "entered_time"), message.text != "Назад"]))
def handle_confirm_slot(message):
    user_id = message.chat.id
    slot_confirmation = message.text
    last_state = BotSingleton.manager.get_current_user_state_info(user_id)
    if slot_confirmation == "Свободный слот":
        BotSingleton.manager.add_new_slot(user_id, last_state["info"])
    elif slot_confirmation == "Занятый слот":
        BotSingleton.manager.add_new_slot(user_id, last_state["info"])
    elif slot_confirmation == "Постоянный слот":
        BotSingleton.manager.add_new_slot(user_id, last_state["info"])
    else:
        BotSingleton.manager.change_current_user_state(user_id, "selected_place")
        text_msg = "Вы задали неправильный тип слота, выберите один из предложенных нами:"
        return BotSingleton.bot.send_message(user_id, text_msg)
    
    BotSingleton.manager.change_current_user_state(user_id, "start")
    return BotSingleton.bot.send_message(user_id, "Выберите опцию:", reply_markup=get_start_markup())

