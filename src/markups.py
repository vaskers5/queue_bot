from ldclient import get
from sympy import use
import telebot
from telebot import types


def generate_markup_from_list(objects: list[str]):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True,)
    buttons = [types.KeyboardButton(obj) for obj in objects]
    markup.add(*buttons)
    markup.add(types.KeyboardButton("Назад"))
    return markup


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
    markup.add(types.KeyboardButton("Назад"))
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

def get_day_slots_markup(slots):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True,)
    buttons = [types.KeyboardButton(slot) for slot in slots]
    markup.add(*buttons)
    markup.add(types.KeyboardButton("Назад"))
    return markup

def get_change_workout_options_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True,)
    buttons = [types.KeyboardButton("Изменить время"),
               types.KeyboardButton("Удалить тренировку"),
               types.KeyboardButton("Освободить слот и уведомить пользователей")]
    markup.add(*buttons)
    markup.add(types.KeyboardButton("Назад"))
    return markup