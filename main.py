from config.setup_google_sheet import setup_google_sheet
from utils.extractors import extract_fcc_articles, extract_substack_articles
from utils.extractors import get_articles
from utils.sheet import check_existing_header, get_all_titles
from data.providers import freecodecamp, substack

def main():
    all_articles = []
    header = ["date", "title", "author", "link", "category"]
    worksheet = setup_google_sheet()
    existing_title = get_all_titles(worksheet)

    check_existing_header(worksheet, header)

    get_articles(
        freecodecamp["url"], freecodecamp["class"], extract_fcc_articles, all_articles
    )
    for url in substack["urls"]:
        get_articles(url, substack["class"], extract_substack_articles, all_articles)

    filtered_articles = [
        article for article in all_articles if article[1] not in existing_title
    ]

    for article in filtered_articles:
        worksheet.append_row(list(article))



if __name__ == "__main__":
    print("Starting the process!")
    main()
    print("The process is coimpleted")