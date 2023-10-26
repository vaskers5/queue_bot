from ldclient import get
from sympy import im, use
import telebot
from telebot import types

from src.markups import generate_markup_from_list
from src.options import generate_calendar_for_two_weeks


bot = telebot.TeleBot("1923472646:AAHrWfdgLlRP3FRzRn-xWx09f5WM_mfBXHQ")

# Определение состояния пользователя
user_states = {}


# Добавьте новые состояния
SELECT_DAY, ENTER_TIME, CONFIRM_SLOT = range(3)

from telebot import types


weeks_days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
day_hours = [f"{i}:00-{i+1}:00" for i in range(8, 23)]
user_workout_data = {}



@bot.message_handler(func=lambda message: message.text == "Изменить запись")
def change_workout_day(message):
    user_id = message.chat.id
    user_states[user_id] = "change_workout"
    bot.send_message(message.chat.id, "Выберите день недели или введите его в текстовом формате (например, Понедельник):", reply_markup=get_week_days_markup())


    
@bot.message_handler(func=lambda message: all([message.text in weeks_days,user_states.get(message.chat.id) == "change_workout"]))
def handle_selected_change_day(message):
    if message.text == "Назад":
        user_states[message.chat.id] = "start"
        bot.send_message(message.chat.id, "Выберите опцию:", reply_markup=get_training_options_markup())
    else:
        user_id = message.chat.id
        user_states[user_id] = "selected_day_changing_slot"
        example_slots = ["10:00-11:00", "13:00-14:00", "17:00-18:00"]
        bot.send_message(user_id,
                        f"Какой слот вы хотите изменить",
                        reply_markup=get_day_slots_markup(slots=example_slots))


def validate_time(time: str) -> bool:
    return True


@bot.message_handler(func=lambda message: all([validate_time(message.text),user_states.get(message.chat.id) == "selected_day_changing_slot"]))
def handle_selected_change_slot(message):
    if message.text == "Назад":
        user_states[message.chat.id] = "start"
        bot.send_message(message.chat.id, "Выберите опцию:", reply_markup=get_training_options_markup())
    else:
        user_id = message.chat.id
        user_states[user_id] = "selected_day_changing_slot"
        bot.send_message(user_id,
                        f"Что вы хотите поменять?",
                        reply_markup=get_change_workout_options_markup())
        

@bot.message_handler(func=lambda message: all([message.text == "Изменить время",user_states.get(message.chat.id) == "selected_day_changing_slot"]))
def handle_change_workout_time(message):
    user_states[user_id] = "start"
    bot.send_message(user_id, "Выберите опцию:", reply_markup=get_start_markup())

@bot.message_handler(func=lambda message: all([message.text == "Удалить тренировку",user_states.get(message.chat.id) == "selected_day_changing_slot"]))
def handle_delete_workout(message):
    user_states[user_id] = "start"
    bot.send_message(user_id, "Выберите опцию:", reply_markup=get_start_markup())

@bot.message_handler(func=lambda message: all([message.text == "Освободить слот и уведомить пользователей",
                                               user_states.get(message.chat.id) == "selected_day_changing_slot"]))
def handle_make_slot_free(message):
    user_states[user_id] = "start"
    bot.send_message(user_id, "Выберите опцию:", reply_markup=get_start_markup())

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Выберите опцию:", reply_markup=get_start_markup())


@bot.message_handler(func=lambda message: message.text == "Тренировки")
def handle_training_options(message):
    user_states[message.chat.id] = ""
    bot.send_message(message.chat.id, "Выберите опцию:", reply_markup=get_training_options_markup())

@bot.message_handler(func=lambda message: message.text == "Все мои доступные тренировки")
def handle_all_trains_info(message):
    user_states[message.chat.id] = "start"
    example_data = "\n".join(
    ["28.05 Пятница 09:00-10:00",
    "28.05 Пятница 10:00-11:00",
    "28.05 Пятница 11:00-12:00",
    "31.05 Понедельник 09:00-10:00"])
    bot.send_message(message.chat.id, example_data)
    bot.send_message(message.chat.id, "Выберите опцию для тренировок:", reply_markup=get_start_markup())
    

@bot.message_handler(func=lambda message: message.text == "Фитнес-клубы")
def handle_fitness_club_option(message):
    user_states[message.chat.id] = "fitness_clubs"
    bot.send_message(message.chat.id, "Выберите опцию:", reply_markup=get_fitness_club_markup())

@bot.message_handler(func=lambda message: message.text == "Назад")
def handle_back_option(message):
    user_states[message.chat.id] = "start"
    bot.send_message(message.chat.id, "Выберите опцию для тренировок:", reply_markup=get_start_markup())



if __name__ == "__main__":
    bot.add_message_handler(handle_training_options)
    bot.add_message_handler(handle_back_option)
    bot.add_message_handler(handle_fitness_club_option)

    bot.add_message_handler(handle_plan_workout)
    bot.add_message_handler(handle_selected_day)
    bot.add_message_handler(handle_entered_time)
    bot.add_message_handler(handle_confirm_slot)
    bot.add_message_handler(handle_all_trains_info)
    
    bot.add_message_handler(change_workout_day)
    bot.add_message_handler(handle_selected_change_day)
    bot.add_message_handler(handle_selected_change_slot)
    
    bot.add_message_handler(handle_change_workout_time)
    bot.add_message_handler(handle_delete_workout)
    bot.add_message_handler(handle_make_slot_free)
    bot.polling()
