from datetime import datetime, timedelta

from src.bot_singleton import BotSingleton


weeks_days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]


def check_current_user_state(chat_id: str, state: str) -> bool:
    return BotSingleton.manager.get_current_user_state(chat_id)["state"] == state


def generate_calendar_for_two_weeks()-> tuple[list[str], list[datetime]]:
    current_date = datetime.now()
    str_dates, dates = [], []
    for i in range(14):
        next_day = current_date + timedelta(days=i)
        formatted_day = f"{weeks_days[next_day.weekday()]}({next_day.day:02d}.{next_day.month}.{next_day.year})"
        str_dates.append(formatted_day)
        dates.append(next_day)
    return str_dates, dates

def validate_time(time: str) -> bool:
    "must be in format hh:mm-hh:mm"
    try:
        start, end = time.split("-")
        datetime.strptime(start, '%H:%M')
        datetime.strptime(end, '%H:%M')
        return True
    except ValueError:
        return False
