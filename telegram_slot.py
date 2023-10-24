from ldclient import get
from sympy import use
import telebot
from telebot import types

bot = telebot.TeleBot("1923472646:AAHrWfdgLlRP3FRzRn-xWx09f5WM_mfBXHQ")

# Определение состояния пользователя
user_states = {}


# Добавьте новые состояния
SELECT_DAY, ENTER_TIME, CONFIRM_SLOT = range(3)

from telebot import types


weeks_days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
day_hours = [f"{i}:00-{i+1}:00" for i in range(8, 23)]
user_workout_data = {}

def get_week_days_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True,)
    buttons = [types.KeyboardButton(day) for day in weeks_days]
    markup.add(*buttons)
    markup.add(types.KeyboardButton("Назад"))
    return markup

def get_day_hours_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True,)
    buttons = [types.KeyboardButton(slot) for slot in day_hours]
    markup.add(*buttons)
    return markup

def get_training_options_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Запланировать тренировку")
    item2 = types.KeyboardButton("Все мои доступные тренировки")
    item3 = types.KeyboardButton("Изменить запись")
    item4 = types.KeyboardButton("Добавить новый свободный слот")
    item5 = types.KeyboardButton("Назад")
    markup.add(item1, item2, item3, item4, item5)
    return markup

def get_fitness_club_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Добавить новое место")
    item2 = types.KeyboardButton("Удалить фитнес-клуб")
    item3 = types.KeyboardButton("Назад")
    markup.add(item1, item2, item3)
    return markup

def get_start_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Тренировки")
    item2 = types.KeyboardButton("Фитнес-клубы")
    markup.add(item1, item2)
    return markup

@bot.message_handler(func=lambda message: message.text == "Запланировать тренировку")
def handle_plan_workout(message):
    user_states[message.chat.id] = "plan_workout"
    bot.send_message(message.chat.id, "Выберите день недели или введите его в текстовом формате (например, Понедельник):", reply_markup=get_week_days_markup())

@bot.message_handler(func=lambda message: all([message.text in weeks_days,user_states.get(message.chat.id) == "plan_workout"]))
def handle_selected_day(message):
    if message.text == "Назад":
        user_states[message.chat.id] = "start"
        bot.send_message(message.chat.id, "Выберите опцию:", reply_markup=get_training_options_markup())
    else:
        user_id = message.chat.id
        user_states[user_id] = "selected_day"
        user_workout_data[user_id] = {"day": message.text}
        bot.send_message(user_id,
                        f"Вы выбрали день {message.text}. Теперь введите время начала и конца тренировки (например, 09:00-10:00). Вы можете использовать заготовленные нами варианты, или задать сами введя текст:",
                        reply_markup=get_day_hours_markup())

@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == "selected_day")
def handle_entered_time(message):
    user_id = message.chat.id
    user_states[user_id] = "entered_time"
    time = message.text
    user_workout_data[user_id]["time"] = time
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(types.KeyboardButton("Да"), types.KeyboardButton("Нет"))
    bot.send_message(user_id, f"Вы выбрали время: {time}. Это свободный слот?", reply_markup=markup)

@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == "entered_time")
def handle_confirm_slot(message):
    user_id = message.chat.id
    slot_confirmation = message.text

    if slot_confirmation == "Да":
        # Получаем день и время из user_workout_data
        workout_data = user_workout_data[user_id]
        day = workout_data["day"]
        time = workout_data["time"]

        # Выполняйте логику для свободного слота, используя day и time
        pass  # Здесь добавьте свою логику
    elif slot_confirmation == "Нет":
        # Выполняйте логику для занятого слота
        pass  # Здесь добавьте свою логику

    user_states[user_id] = "start"
    bot.send_message(user_id, "Выберите опцию:", reply_markup=get_start_markup())


@bot.message_handler(func=lambda message: message.text == "Изменить запись")
def change_workout_day(message):
    user_id = message.chat.id
    user_states[user_id] = "change_workout"
    bot.send_message(message.chat.id, "Выберите день недели или введите его в текстовом формате (например, Понедельник):", reply_markup=get_week_days_markup())


def get_day_slots_markup(slots):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True,)
    buttons = [types.KeyboardButton(slot) for slot in slots]
    markup.add(*buttons)
    markup.add(types.KeyboardButton("Назад"))
    return markup
    
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


def get_change_workout_options_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True,)
    buttons = [types.KeyboardButton("Изменить время"),
               types.KeyboardButton("Удалить тренировку"),
               types.KeyboardButton("Освободить слот и уведомить пользователей")]
    markup.add(*buttons)
    markup.add(types.KeyboardButton("Назад"))
    return markup


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
