import os
import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv

load_dotenv()
SHEET_ID = os.environ.get("SHEET_ID")
scopes = ["https://www.googleapis.com/auth/spreadsheets"]


def get_creds():
    return os.path.join(os.path.dirname(__file__), "..", "credentials.json")


def get_sheet(sheet_name):
    creds = get_creds()
    creds = Credentials.from_service_account_file(creds, scopes=scopes)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(SHEET_ID)
    return sheet.worksheet(sheet_name)


articles_sheet = get_sheet("articles")
providers_sheet = get_sheet("providers")


def get_all_titles():
    all_titles = articles_sheet.get_all_values()[1:]
    return tuple(row[1] for row in all_titles)


existing_titles = get_all_titles()


def send_articles_sheet(article_info):
    date = article_info[0]
    title = article_info[1]
    author = article_info[2]
    print(f"===> adding {title} by {author} at {date}!")
    articles_sheet.append_row(list(article_info))


def get_all_providers():
    return providers_sheet.get_all_records()