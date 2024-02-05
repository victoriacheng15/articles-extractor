from utils.extractors import extract_fcc_articles
from utils.extractors import get_articles
from config.setup_google_sheet import setup_google_sheet


header = ["date", "title", "author", "link", "category"]
all_articles = []

worksheet = setup_google_sheet()

existing_header = worksheet.row_values(1)
if existing_header != header:
    worksheet.append_row(header)


def main():
    get_articles(
        "https://www.freecodecamp.org/news/",
        "post-card",
        extract_fcc_articles,
        all_articles,
    )
    for article in all_articles:
        existing_article = worksheet.find(article["title"], in_column=2)
        if not existing_article:
            article_values = [article[key] for key in header]
            worksheet.append_row(article_values)


if __name__ == "__main__":
    main()
