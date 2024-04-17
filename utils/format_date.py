from datetime import datetime


def format_date(date: str) -> str:
    date_object = datetime.strptime(date, "%a %b %d %Y %H:%M:%S GMT%z")
    return date_object.strftime("%Y-%m-%d")


def clean_and_convert_date(date_str):
    if date_str[0].isdigit():
        date_obj = datetime.strptime(date_str[:10], "%Y-%m-%d")
    else:
        date_obj = datetime.strptime(date_str[4:16].strip(), "%b %d %Y")

    return date_obj.strftime("%Y-%m-%d")


def current_time():
    date = datetime.now().date()
    time = datetime.now().time().strftime("%H:%M")
    return date, time
