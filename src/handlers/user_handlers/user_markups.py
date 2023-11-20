from src.tools import generate_markup_from_list


def get_start_markup():
    start_options = ["Тренировки", "Тренера"]
    return generate_markup_from_list(start_options, add_back_button=False)

def get_training_options_markup():
    options = ["Занять слот",
               "Удалить запись", 
            #    "Изменить запись"
               ]
    return generate_markup_from_list(options)

def get_trainers_options_markup():
    options = ["Привязаться к тренеру",
               "Удалить запись к тренеру", 
               ]
    return generate_markup_from_list(options)