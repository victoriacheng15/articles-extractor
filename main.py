import os
import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv
from utils.extractors import extract_fcc_articles
from utils.extractors import get_articles

load_dotenv()
SHEET_ID = os.environ.get("SHEET_ID")

scopes = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
client = gspread.authorize(creds)
sheet = client.open_by_key(SHEET_ID)
worksheet = sheet.sheet1

header = ["date", "title", "author", "link", "category"]
existing_header = worksheet.row_values(1)

if existing_header != header:
    worksheet.append_row(header)

all_articles = []


def main():
    get_articles(
        "https://www.freecodecamp.org/news/",
        "post-card",
        extract_fcc_articles,
        all_articles,
    )
    print(all_articles)
    for article in all_articles:
        existing_article = worksheet.find(article["title"], in_column=2)
        if not existing_article:
            article_values = [article[key] for key in header]
            worksheet.append_row(article_values)


if __name__ == "__main__":
    main()
