from datetime import datetime


def format_date(date: str) -> str:
    date_object = datetime.strptime(date, "%a %b %d %Y %H:%M:%S GMT%z")
    return date_object.strftime("%Y-%m-%d")


def current_time():
    date = datetime.now().date()
    time = datetime.now().time().strftime("%H:%M")
    return date, time
