from telebot import types

def generate_markup_from_list(objects: list[str], add_back_button: bool = True):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    buttons = [types.KeyboardButton(obj) for obj in objects]
    markup.add(*buttons)
    if add_back_button:
        markup.add(types.KeyboardButton("Назад"))
    return markup