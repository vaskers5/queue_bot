from datetime import datetime

from src.bot_singleton import BotSingleton

from src.options import generate_calendar_for_two_weeks, validate_time, check_current_user_state, parse_date
from src.markups import generate_markup_from_list, get_day_hours_markup, get_start_markup

@BotSingleton.bot.message_handler(func=lambda message: message.text == "Запланировать тренировку")
def handle_workout_date(message):
    str_dates, dates = generate_calendar_for_two_weeks()
    markup = generate_markup_from_list(str_dates)
    dates_dict = {k: str(v) for k, v in zip(str_dates, dates)}
    BotSingleton.manager.change_current_user_state(message.chat.id, "plan_workout", state_info=dates_dict)
    BotSingleton.bot.send_message(message.chat.id, "Выберите удобную вам дату. Либи введите ее в формате DD.MM.pYYYY. Например 1", reply_markup=markup)


@BotSingleton.bot.message_handler(func=lambda message: all([check_current_user_state(message.chat.id, "plan_workout"), message.text != "Назад"])) 
def handle_workout_place(message):
    user_id = message.chat.id
    last_state = BotSingleton.manager.get_current_user_state(user_id)
    workout_date = parse_date(message.text)
    if message.text in last_state["state_info"]:
        workout_date = last_state["state_info"][message.text]
    elif workout_date is None or workout_date < datetime.now():
        BotSingleton.bot.send_message(user_id, "Введите дату в корректном формате")
    if workout_date:
        workout_date = str(workout_date)
        BotSingleton.manager.change_current_user_state(user_id, "selected_day", state_info={"date": workout_date})
        user_places = BotSingleton.manager.get_user_places(user_id)
        if len(user_places) == 0:
            BotSingleton.manager.change_current_user_state(user_id, "start")
            BotSingleton.bot.send_message(user_id, "У вас нет мест для тренировок. Добавьте их в настройках.", reply_markup=get_start_markup())
        else:
            places_data = {place.name: place.place_id for place in user_places}
            BotSingleton.manager.change_current_user_state(user_id, "enter_place", state_info={"places": places_data, "date": workout_date})
            BotSingleton.bot.send_message(user_id, "Выберите место тренировки:", reply_markup=generate_markup_from_list([place.name for place in user_places]))


@BotSingleton.bot.message_handler(func=lambda message: all([check_current_user_state(message.chat.id, "enter_place"), message.text != "Назад"]))
def handle_workout_time(message):
    user_id = message.chat.id
    last_state = BotSingleton.manager.get_current_user_state(user_id)
    text_place = message.text
    workout_date = last_state["state_info"]["date"]
    if not(text_place in last_state["state_info"]["places"]):
        # BotSingleton.manager.change_current_user_state(user_id, "selected_day")
        text_msg = "Выберите место из предложенных нами. Если вашего место нет в списке - добавьте его на начальном экране"
        BotSingleton.bot.send_message(user_id, text_msg)
    else:
        place_id, place_name = last_state["state_info"]["places"][message.text], message.text
        BotSingleton.manager.change_current_user_state(user_id, "selected_place", state_info={"date": workout_date, "place": {"place_id": place_id, "place_name": place_name}})
        text = f"Вы выбрали день {message.text}. Теперь введите время начала и конца тренировки (например, 09:00-10:00). Вы можете использовать заготовленные нами варианты, или задать сами введя текст:",
        BotSingleton.bot.send_message(user_id, text, reply_markup=get_day_hours_markup())


@BotSingleton.bot.message_handler(func=lambda message: all([check_current_user_state(message.chat.id, "selected_place"), message.text != "Назад"]))
def handle_entered_time(message):
    user_id = message.chat.id
    if not validate_time(message.text):
        # BotSingleton.manager.change_current_user_state(user_id, "enter_place")
        text_msg = "Задайте время в формате hh:mm-hh.mm. Например 10:00-11:00"
        BotSingleton.bot.send_message(user_id, text_msg)
    else:
        start_time, end_time = message.text.split("-")
        last_state = BotSingleton.manager.get_current_user_state(user_id)
        date = datetime.strptime(last_state["state_info"]["date"], '%Y-%m-%d %H:%M:%S.%f')
        workout_start_time = str(datetime.combine(date, datetime.strptime(start_time, '%H:%M').time()))
        workout_end_time = str(datetime.combine(date, datetime.strptime(end_time, '%H:%M').time()))
        BotSingleton.manager.change_current_user_state(user_id, "entered_time", 
                                                    state_info={"start_time": workout_start_time, "end_time": workout_end_time,
                                                                **last_state["state_info"]["place"]})
        markup = generate_markup_from_list(["Свободный слот", "Занятый слот", "Постоянный слот"])
        confirmation_msg = f"Итоговая информация: {last_state['state_info']['place']['place_name']}, {str(date.date())} {start_time}-{end_time}. Выберите тип слота:"
        BotSingleton.bot.send_message(user_id, confirmation_msg, reply_markup=markup)


@BotSingleton.bot.message_handler(func=lambda message: all([check_current_user_state(message.chat.id, "entered_time"), message.text != "Назад"]))
def handle_confirm_slot(message):
    user_id = message.chat.id
    slot_confirmation = message.text
    last_state = BotSingleton.manager.get_current_user_state(user_id)
    if slot_confirmation == "Свободный слот":
        BotSingleton.manager.add_new_slot(user_id, **last_state["state_info"])
    elif slot_confirmation == "Занятый слот":
        BotSingleton.manager.add_new_slot(user_id, **last_state["state_info"])
    elif slot_confirmation == "Постоянный слот":
        BotSingleton.manager.add_new_slot(user_id, **last_state["state_info"])
    else:
        # BotSingleton.manager.change_current_user_state(user_id, "selected_place")
        text_msg = "Вы задали неправильный тип слота, выберите один из предложенных нами:"
        BotSingleton.bot.send_message(user_id, text_msg)
        return None
    BotSingleton.bot.send_message(user_id, "Слот успешно добавлен!")
    BotSingleton.manager.change_current_user_state(user_id, "start")
    BotSingleton.bot.send_message(user_id, "Выберите опцию:", reply_markup=get_start_markup())

