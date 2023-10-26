from datetime import datetime, timedelta

from src.bot_singleton import BotSingleton
from src.markups import get_start_markup

weeks_days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]


def check_current_user_state(chat_id: str, state: str) -> bool:
    cur_state = BotSingleton.manager.get_current_user_state(chat_id)
    if cur_state is None:
        BotSingleton.manager.change_current_user_state(chat_id, "start")
        cur_state = BotSingleton.manager.get_current_user_state(chat_id)
        BotSingleton.bot.send_message(chat_id, "Выберите опцию:", reply_markup=get_start_markup())
    return cur_state["state"] == state

def generate_calendar_for_two_weeks()-> tuple[list[str], list[datetime]]:
    current_date = datetime.now()
    str_dates, dates = [], []
    for i in range(14):
        next_day = current_date + timedelta(days=i)
        formatted_day = f"{weeks_days[next_day.weekday()]}({next_day.day:02d}.{next_day.month}.{next_day.year})"
        str_dates.append(formatted_day)
        dates.append(next_day)
    return str_dates, dates


def parse_date(date_string, date_format="%d.%m.%Y"):
    try:
        return datetime.strptime(date_string, date_format)
    except ValueError:
        return None

def validate_time(time: str) -> bool:
    "must be in format hh:mm-hh:mm"
    try:
        start, end = time.split("-")
        datetime.strptime(start, '%H:%M')
        datetime.strptime(end, '%H:%M')
        return True
    except ValueError:
        return False
