from datetime import datetime


def format_date(date: str) -> str:
    date_object = datetime.strptime(date, "%a %b %d %Y %H:%M:%S GMT%z")
    return date_object.strftime("%Y-%m-%d")
