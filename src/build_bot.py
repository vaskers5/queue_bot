from src.bot_singleton import BotSingleton
from src.handlers.main_menu_handlers import handle_training_options, handle_back_option, handle_fitness_club_option, handle_start, handle_wrong_message
from src.handlers.plan_workout_handlers import handle_confirm_slot, handle_entered_time, handle_workout_date, handle_workout_place, handle_workout_time
from src.handlers.workout_information_handlers import handle_all_trains_info
from src.handlers.fitness_clubs_handlers import handle_add_place, handle_delete_place, handle_get_all_user_places, handle_write_deleted_place_name, handle_write_new_place_name

def build_bot():
    bot = BotSingleton.bot
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
