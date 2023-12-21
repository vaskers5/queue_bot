from src.bot_singleton import TrainerSingleton

from src.markups import get_start_markup


@TrainerSingleton.bot.message_handler(func=lambda message: message.text == "Изменить запись")
def change_workout_day(message):
    user_id = message.chat.id
    TrainerSingleton.bot.send_message(user_id, "Выберите опцию:", reply_markup=get_start_markup())
    # user_states[user_id] = "change_workout"
    # BotSingleton.bot.send_message(message.chat.id, "Выберите день недели или введите его в текстовом формате (например, Понедельник):", reply_markup=get_week_days_markup())


    
@TrainerSingleton.bot.message_handler(func=lambda message: all([message.text in weeks_days,user_states.get(message.chat.id) == "change_workout"]))
def handle_selected_change_day(message):
    if message.text == "Назад":
        user_states[message.chat.id] = "start"
        TrainerSingleton.bot.send_message(message.chat.id, "Выберите опцию:", reply_markup=get_training_options_markup())
    else:
        user_id = message.chat.id
        user_states[user_id] = "selected_day_changing_slot"
        example_slots = ["10:00-11:00", "13:00-14:00", "17:00-18:00"]
        TrainerSingleton.bot.send_message(user_id,
                        f"Какой слот вы хотите изменить",
                        reply_markup=get_day_slots_markup(slots=example_slots))


@TrainerSingleton.bot.message_handler(func=lambda message: all([validate_time(message.text),user_states.get(message.chat.id) == "selected_day_changing_slot"]))
def handle_selected_change_slot(message):
    if message.text == "Назад":
        user_states[message.chat.id] = "start"
        TrainerSingleton.bot.send_message(message.chat.id, "Выберите опцию:", reply_markup=get_training_options_markup())
    else:
        user_id = message.chat.id
        user_states[user_id] = "selected_day_changing_slot"
        TrainerSingleton.bot.send_message(user_id,
                        f"Что вы хотите поменять?",
                        reply_markup=get_change_workout_options_markup())


@TrainerSingleton.bot.message_handler(func=lambda message: all([message.text == "Изменить время",user_states.get(message.chat.id) == "selected_day_changing_slot"]))
def handle_change_workout_time(message):
    user_states[user_id] = "start"
    TrainerSingleton.bot.send_message(user_id, "Выберите опцию:", reply_markup=get_start_markup())

@TrainerSingleton.bot.message_handler(func=lambda message: all([message.text == "Удалить тренировку",user_states.get(message.chat.id) == "selected_day_changing_slot"]))
def handle_delete_workout(message):
    user_states[user_id] = "start"
    TrainerSingleton.bot.send_message(user_id, "Выберите опцию:", reply_markup=get_start_markup())

@TrainerSingleton.bot.message_handler(func=lambda message: all([message.text == "Освободить слот и уведомить пользователей",
                                               user_states.get(message.chat.id) == "selected_day_changing_slot"]))
def handle_make_slot_free(message):
    user_states[user_id] = "start"
    TrainerSingleton.bot.send_message(user_id, "Выберите опцию:", reply_markup=get_start_markup())