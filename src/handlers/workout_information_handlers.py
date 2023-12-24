from collections import defaultdict

from datetime import datetime

from src.bot_singleton import TrainerSingleton
from src.markups import get_start_markup


@TrainerSingleton.bot.message_handler(func=lambda message: message.text == "Все мои доступные тренировки")
def handle_all_trains_info(message):
    user_id = message.chat.id
    user_tg_nick  = message.from_user.username
    user_workouts = TrainerSingleton.manager.get_user_slots(user_tg_nick)
    user_workouts_data_by_date = defaultdict(list)
    current_datetime = datetime.now()
    for workout in user_workouts:
        start_time = datetime.strptime(workout.start_time, '%Y-%m-%d %H:%M:%S')
        if start_time > current_datetime:
            user_workouts_data_by_date[start_time.date()].append(workout)

    result_msg = ""
    for date, workouts in user_workouts_data_by_date.items():
        result_msg += f"{date.strftime('%d.%m.%Y')}\n"
        for workout in workouts:
            #todo add workout type
            start_time = datetime.strptime(workout.start_time, '%Y-%m-%d %H:%M:%S')
            end_time = datetime.strptime(workout.end_time, '%Y-%m-%d %H:%M:%S')
            user_nickname = "Свободный слот" if workout.user_nickname is None else f"@{workout.user_nickname}"
            result_msg += f"{start_time.strftime('%H:%M')}-{end_time.strftime('%H:%M')} {workout.place_name} {user_nickname}\n"
            
        result_msg += "\n"
    TrainerSingleton.manager.change_current_user_state(user_id, "start")
    TrainerSingleton.bot.send_message(user_id, result_msg)
    TrainerSingleton.bot.send_message(user_id, "Выберите опцию:", reply_markup=get_start_markup())
