import os
import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv

load_dotenv()
SHEET_ID = os.environ.get("SHEET_ID")
scopes = ["https://www.googleapis.com/auth/spreadsheets"]


def get_creds():
    """
    Returns the path to the credentials.json file.
    """
    return os.path.join(os.path.dirname(__file__), "..", "credentials.json")


def get_sheet(sheet_name):
    """
    Given a sheet name, returns the corresponding worksheet object.

    Args:
        sheet_name (str): The name of the sheet to retrieve.

    Returns:
        gspread.models.Worksheet: The worksheet object for the given sheet name.
    """
    creds = get_creds()
    creds = Credentials.from_service_account_file(creds, scopes=scopes)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(SHEET_ID)
    return sheet.worksheet(sheet_name)


articles_sheet = get_sheet("articles")
providers_sheet = get_sheet("providers")


def get_all_titles():
    """
    Retrieves all titles from the 'articles' sheet, excluding the header row.

    Returns:
        tuple: A tuple containing all titles from the 'articles' sheet.
    """
    all_titles = articles_sheet.get_all_values()[1:]
    return tuple(row[1] for row in all_titles)


existing_titles = get_all_titles()


def send_articles_sheet(article_info):
    """
    Appends a new row to the 'articles' sheet with the provided article information.

    Args:
        article_info (tuple): A tuple containing the article information in the order (date, title, author).
    """
    date = article_info[0]
    title = article_info[1]
    author = article_info[2]
    print(f"===> adding {title} by {author} at {date}!")
    articles_sheet.append_row(list(article_info))


def get_all_providers():
    """
    Retrieves all records from the 'providers' sheet.

    Returns:
        list: A list of dictionaries, where each dictionary represents a row in the 'providers' sheet.
    """
    return providers_sheet.get_all_records()
