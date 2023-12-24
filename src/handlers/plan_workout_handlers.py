from datetime import datetime

from src.bot_singleton import TrainerSingleton

from src.options import generate_calendar_for_two_weeks, validate_time, check_current_user_state, parse_date
from src.markups import generate_markup_from_list, get_day_hours_markup, get_start_markup


@TrainerSingleton.bot.message_handler(func=lambda message: message.text == "Запланировать тренировку")
def handle_workout_date(message):
    str_dates, dates = generate_calendar_for_two_weeks()
    markup = generate_markup_from_list(str_dates)
    dates_dict = {k: str(v) for k, v in zip(str_dates, dates)}
    TrainerSingleton.manager.change_current_user_state(message.chat.id, "plan_workout", state_info=dates_dict)
    TrainerSingleton.bot.send_message(message.chat.id, "Выберите удобную вам дату. Либи введите ее в формате DD.MM.pYYYY. Например 1", reply_markup=markup)


@TrainerSingleton.bot.message_handler(func=lambda message: all([check_current_user_state(message.chat.id, "plan_workout"), message.text != "Назад"])) 
def handle_workout_place(message):
    user_id = message.chat.id
    last_state = TrainerSingleton.manager.get_current_user_state(user_id)
    workout_date = parse_date(message.text)
    if message.text in last_state["state_info"]:
        workout_date = last_state["state_info"][message.text]
    elif workout_date is None or workout_date.date() < datetime.now().date():
        workout_date  = None
        TrainerSingleton.bot.send_message(user_id, "Введите дату в корректном формате")
    if workout_date:
        workout_date = str(workout_date)
        TrainerSingleton.manager.change_current_user_state(user_id, "selected_day", state_info={"date": workout_date})
        user_places = TrainerSingleton.manager.get_trainer_places(user_id)
        if len(user_places) == 0:
            TrainerSingleton.manager.change_current_user_state(user_id, "start")
            TrainerSingleton.bot.send_message(user_id, "У вас нет мест для тренировок. Добавьте их в настройках.", reply_markup=get_start_markup())
        else:
            places_data = {place.name: place.place_id for place in user_places}
            TrainerSingleton.manager.change_current_user_state(user_id, "enter_place", state_info={"places": places_data, "date": workout_date})
            TrainerSingleton.bot.send_message(user_id, "Выберите место тренировки:", reply_markup=generate_markup_from_list([place.name for place in user_places]))


@TrainerSingleton.bot.message_handler(func=lambda message: all([check_current_user_state(message.chat.id, "enter_place"), message.text != "Назад"]))
def handle_workout_time(message):
    user_id = message.chat.id
    last_state = TrainerSingleton.manager.get_current_user_state(user_id)
    text_place = message.text
    workout_date = last_state["state_info"]["date"]
    if not(text_place in last_state["state_info"]["places"]):
        # TrainerSingleton.manager.change_current_user_state(user_id, "selected_day")
        text_msg = "Выберите место из предложенных нами. Если вашего место нет в списке - добавьте его на начальном экране"
        TrainerSingleton.bot.send_message(user_id, text_msg)
    else:
        place_id, place_name = last_state["state_info"]["places"][message.text], message.text
        TrainerSingleton.manager.change_current_user_state(user_id, "selected_place", state_info={"date": workout_date, "place": {"place_id": place_id, "place_name": place_name}})
        text = "Вы выбрали день. Теперь введите время начала и конца тренировки (например, 09:00-10:00). Вы можете использовать заготовленные нами варианты, или задать сами введя текст:"
        TrainerSingleton.bot.send_message(user_id, text, reply_markup=get_day_hours_markup())


@TrainerSingleton.bot.message_handler(func=lambda message: all([check_current_user_state(message.chat.id, "selected_place"), message.text != "Назад"]))
def handle_entered_time(message):
    user_id = message.chat.id
    if not validate_time(message.text):
        # TrainerSingleton.manager.change_current_user_state(user_id, "enter_place")
        text_msg = "Задайте время в формате hh:mm-hh.mm. Например 10:00-11:00"
        TrainerSingleton.bot.send_message(user_id, text_msg)
    else:
        start_time, end_time = message.text.split("-")
        last_state = TrainerSingleton.manager.get_current_user_state(user_id)
        date = datetime.strptime(last_state["state_info"]["date"], '%Y-%m-%d %H:%M:%S.%f')
        workout_start_time = str(datetime.combine(date, datetime.strptime(start_time, '%H:%M').time()))
        workout_end_time = str(datetime.combine(date, datetime.strptime(end_time, '%H:%M').time()))
        TrainerSingleton.manager.change_current_user_state(user_id, "entered_time", 
                                                    state_info={"start_time": workout_start_time, "end_time": workout_end_time,
                                                                **last_state["state_info"]["place"]})
        markup = generate_markup_from_list(["Свободный слот", "Занятый слот", "Постоянный слот"])
        confirmation_msg = f"Итоговая информация: {last_state['state_info']['place']['place_name']}, {str(date.date())} {start_time}-{end_time}. Выберите тип слота:"
        TrainerSingleton.bot.send_message(user_id, confirmation_msg, reply_markup=markup)


@TrainerSingleton.bot.message_handler(func=lambda message: all([check_current_user_state(message.chat.id, "entered_time"), message.text != "Назад"]))
def handle_confirm_slot(message):
    user_id = message.chat.id
    slot_confirmation = message.text
    last_state = TrainerSingleton.manager.get_current_user_state(user_id)
    if slot_confirmation in ["Занятый слот", "Постоянный слот"]:
        trainer_clients = TrainerSingleton.manager.get_trainer_clients(message.from_user.username)
        if len(trainer_clients) == 0:
            text = "У вас нет клиентов, чтоб мы могли записать их на этот слот."
            TrainerSingleton.bot.send_message(user_id, text)
        else:
            clients_data = {str(i + 1): client_nick for i, client_nick in enumerate(trainer_clients)}
            last_state["state_info"]["slot_type"] = slot_confirmation
            TrainerSingleton.manager.change_current_user_state(user_id, "enter_client", state_info={"clients": clients_data,
                                                                                                **last_state["state_info"]})
            text = "Выберите клиента, которого хотите записать на этот слот:\n"
            text += "\n".join([f"{i+1}. {client}" for i, client in enumerate(trainer_clients)])
            TrainerSingleton.bot.send_message(user_id, text, reply_markup=generate_markup_from_list(list(range(1, len(trainer_clients)+1))))
    else:
        if slot_confirmation == "Свободный слот":
            trainer_nickname = message.from_user.username
            TrainerSingleton.manager.add_new_slot(user_id, **last_state["state_info"], slot_type="free", trainer_nickname=trainer_nickname)
            TrainerSingleton.bot.send_message(user_id, "Слот успешно добавлен!")
            TrainerSingleton.manager.change_current_user_state(user_id, "start")
            TrainerSingleton.bot.send_message(user_id, "Выберите опцию:", reply_markup=get_start_markup())
        else:
            # TrainerSingleton.manager.change_current_user_state(user_id, "selected_place")
            text_msg = "Вы задали неправильный тип слота, выберите один из предложенных нами:"
            TrainerSingleton.bot.send_message(user_id, text_msg)


@TrainerSingleton.bot.message_handler(func=lambda message: all([check_current_user_state(message.chat.id, "enter_client"), message.text != "Назад"]))
def handle_choose_clinet(message):
    user_id = message.chat.id
    last_state = TrainerSingleton.manager.get_current_user_state(user_id)
    if not(message.text in last_state["state_info"]["clients"]):
        # TrainerSingleton.manager.change_current_user_state(user_id, "enter_client")
        text_msg = "Выберите клиента из предложенных нами. Если вашего клиента нет в списке - добавьте его на начальном экране"
        TrainerSingleton.bot.send_message(user_id, text_msg)
    else:
        client_nick = last_state["state_info"]["clients"][message.text]
        user_tg_nick  = message.from_user.username
        last_state["state_info"]["slot_type"] = "reserved"
        last_state["state_info"]["user_nickname"] = client_nick
        last_state["state_info"].pop("clients")
        TrainerSingleton.manager.add_new_slot(user_id, **last_state["state_info"], trainer_nickname=user_tg_nick)
        TrainerSingleton.bot.send_message(user_id, "Слот успешно добавлен!")
        TrainerSingleton.manager.change_current_user_state(user_id, "start")
        TrainerSingleton.bot.send_message(user_id, "Выберите опцию:", reply_markup=get_start_markup())

