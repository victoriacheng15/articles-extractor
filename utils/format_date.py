from datetime import datetime


def format_date(date):
    """
    Converts a date string from the format "%a %b %d %Y %H:%M:%S GMT%z" to "%Y-%m-%d".

    Args:
        date (str): The date string to format.

    Returns:
        str: The formatted date string in the format "%Y-%m-%d".
    """
    date_object = datetime.strptime(date, "%a %b %d %Y %H:%M:%S GMT%z")
    return date_object.strftime("%Y-%m-%d")


def clean_and_convert_date(date_str):
    """
    Cleans and converts a date string to the format "%Y-%m-%d".

    Args:
        date_str (str): The date string to clean and convert.

    Returns:
        str: The cleaned and converted date string in the format "%Y-%m-%d".
    """
    if date_str[0].isdigit():
        date_obj = datetime.strptime(date_str[:10], "%Y-%m-%d")
    else:
        date_obj = datetime.strptime(date_str[4:16].strip(), "%b %d %Y")

    return date_obj.strftime("%Y-%m-%d")


def current_time():
    """
    Retrieves the current date and time.

    Returns:
        tuple: A tuple containing the current date and time in the format (date, time).
    """
    date = datetime.now().date()
    time = datetime.now().time().strftime("%H:%M")
    return (date, time)
