import os
import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv

load_dotenv()
SHEET_ID = os.environ.get("SHEET_ID")
scopes = ["https://www.googleapis.com/auth/spreadsheets"]


def get_creds_path():
    """
    Returns the path to the credentials.json file.
    """
    return os.path.join(os.path.dirname(__file__), "..", "credentials.json")


def get_client():
    creds_path = get_creds_path()
    creds = Credentials.from_service_account_file(creds_path, scopes=scopes)
    return gspread.authorize(creds)


def get_worksheet(client, sheet_id, sheet_name):
    """
    Opens and returns a specific worksheet by name.

    Args:
        client (gspread.Client): The authenticated gspread client.
        sheet_id (str): The ID of the Google Sheet.
        sheet_name (str): The name of the worksheet to open.

    Returns:
        gspread.models.Worksheet: The worksheet object
    """
    sheet = client.open_by_key(sheet_id)
    return sheet.worksheet(sheet_name)


def get_all_titles(articles_sheet):
    """
    Retrieves all article titles from the 'articles' sheet, excluding the header.

    Args:
        articles_sheet (gspread.models.Worksheet): The worksheet for articles.

    Returns:
        tuple: All titles in the sheet, as a tuple of strings.
    """
    all_titles = articles_sheet.get_all_values()[1:]
    return tuple(row[1] for row in all_titles)


def get_all_providers(providers_sheet):
    """
    Retrieves all provider data from the 'providers' sheet.

    Args:
        providers_sheet (gspread.models.Worksheet): The worksheet for providers.

    Returns:
        list: List of dicts, each representing one row (provider info).
    """
    return providers_sheet.get_all_records()


def append_article(sheet, article_info, log_func=print):
    """
    Appends a new article row to the given sheet and logs it.

    Args:
        sheet (gspread.models.Worksheet): The worksheet to update.
        article_info (tuple): The article data as (date, title, link, source).
        log_func (function, optional): Function used to log output. Defaults to print.
    """
    date = article_info[0]
    title = article_info[1]
    link = article_info[2]
    log_func(f"==>\n{title} - {date}\n{link}\n")
    # sheet.append_row(list(article_info))
