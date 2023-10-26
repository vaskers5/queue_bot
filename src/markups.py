import telebot
from telebot import types


day_hours = [f"{i}:00-{i+1}:00" for i in range(8, 23)]
user_workout_data = {}

def generate_markup_from_list(objects: list[str], add_back_button: bool = True):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    buttons = [types.KeyboardButton(obj) for obj in objects]
    markup.add(*buttons)
    if add_back_button:
        markup.add(types.KeyboardButton("Назад"))
    return markup


def get_week_days_markup():
    week_days = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
    return generate_markup_from_list(week_days)


def get_day_hours_markup():
    return generate_markup_from_list(day_hours)


def get_training_options_markup():
    options = ["Запланировать тренировку",
               "Все мои доступные тренировки", 
            #    "Изменить запись"
               ]
    return generate_markup_from_list(options)


def get_fitness_club_markup():
    club_options = ["Добавить новое место", "Удалить место", "Мои места"]
    return generate_markup_from_list(club_options)


def get_start_markup():
    start_options = ["Тренировки", "Фитнес-клубы"]
    return generate_markup_from_list(start_options, add_back_button=False)


def get_day_slots_markup(slots):
    return generate_markup_from_list(slots)


def get_change_workout_options_markup():
    options = ["Изменить время", "Удалить тренировку", "Освободить слот и уведомить пользователей", "Назад"]
    return generate_markup_from_list(options)
