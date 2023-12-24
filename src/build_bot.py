from src.bot_singleton import TrainerSingleton, UserSingleton
# Trainer handlers

from src.handlers.main_menu_handlers import handle_training_options, handle_back_option, handle_fitness_club_option, handle_start, handle_wrong_message
from src.handlers.plan_workout_handlers import handle_confirm_slot, handle_entered_time, handle_workout_date, handle_workout_place, handle_workout_time
from src.handlers.workout_information_handlers import handle_all_trains_info
from src.handlers.fitness_clubs_handlers import handle_add_place, handle_delete_place, handle_get_all_user_places, handle_write_deleted_place_name, handle_write_new_place_name

# User handlers
from src.handlers.user_handlers.main_menu_handlers import handle_user_back_option, handle_user_start, handle_user_fitness_club_option, handle_user_training_options, handle_user_wrong_message
from src.handlers.user_handlers.trainer_menu_handlers import handle_add_trainer_tg_nick, handle_add_user_trainer, handle_delete_trainer_nick, handle_delete_user_trainer_connection
from src.handlers.user_handlers.workout_menu_handlers import handle_user_choose_trainer, handle_user_take_slot, handle_user_delete_slot, handle_user_choose_slot


def build_trainer_bot():
    bot = TrainerSingleton.bot
    # main menu handlers
    bot.add_message_handler(handle_start)
    bot.add_message_handler(handle_wrong_message)
    
    bot.add_message_handler(handle_training_options)
    bot.add_message_handler(handle_back_option)
    bot.add_message_handler(handle_fitness_club_option)
    # plan workout handlers
    bot.add_message_handler(handle_workout_date)
    bot.add_message_handler(handle_workout_place)
    bot.add_message_handler(handle_workout_time)
    bot.add_message_handler(handle_entered_time)
    bot.add_message_handler(handle_confirm_slot)
    # workout information handlers
    bot.add_message_handler(handle_all_trains_info)
    
    #fitness clubs handlers
    bot.add_message_handler(handle_add_place)
    bot.add_message_handler(handle_delete_place)
    bot.add_message_handler(handle_get_all_user_places)
    bot.add_message_handler(handle_write_deleted_place_name)
    bot.add_message_handler(handle_write_new_place_name)
    return bot

# main_menu, workout_menu
def build_user_bot():
    bot = UserSingleton.bot
    # main menu handlers
    bot.add_message_handler(handle_user_start)
    bot.add_message_handler(handle_user_wrong_message)
    bot.add_message_handler(handle_user_training_options)
    bot.add_message_handler(handle_user_back_option)
    bot.add_message_handler(handle_user_fitness_club_option)
    
    # trainer_menu_handlers
    bot.add_message_handler(handle_add_trainer_tg_nick)
    bot.add_message_handler(handle_add_user_trainer)
    bot.add_message_handler(handle_delete_trainer_nick)
    bot.add_message_handler(handle_delete_user_trainer_connection)
    
    #workout_menu_handlers
    bot.add_message_handler(handle_user_choose_trainer)
    bot.add_message_handler(handle_user_take_slot)
    bot.add_message_handler(handle_user_choose_slot)
    bot.add_message_handler(handle_user_delete_slot)
    return bot