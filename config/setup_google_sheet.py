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
