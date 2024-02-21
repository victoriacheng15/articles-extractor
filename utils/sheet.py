import os
import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv

load_dotenv()
SHEET_ID = os.environ.get("SHEET_ID")


def get_creds():
    return os.path.join(os.path.dirname(__file__), "..", "credentials.json")


def setup_google_sheet():
    creds = get_creds()
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_file(creds, scopes=scopes)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(SHEET_ID)
    return sheet.sheet1


main_sheet = setup_google_sheet()


def check_existing_header():
    header = ["date", "title", "author", "link", "category", "read?"]
    existing_header = main_sheet.row_values(1)
    if existing_header != header:
        main_sheet.append_row(header)


def get_all_titles():
    data = main_sheet.get_all_values()[1:]
    return tuple(row[1] for row in data)


existing_titles = get_all_titles()


def send_articles_sheet(article_info):
    print(f"===> adding {article_info[1]}!")
    main_sheet.append_row(list(article_info))
