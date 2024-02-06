from config.setup_google_sheet import setup_google_sheet
from utils.extractors import extract_fcc_articles, extract_substack_articles
from utils.extractors import get_articles
from utils.format_date import current_time
from utils.sheet import check_existing_header, get_all_titles
from data.providers import freecodecamp, substack

def main():
    all_articles = []
    header = ["date", "title", "author", "link", "category"]
    main_sheet = setup_google_sheet()
    existing_title = get_all_titles(main_sheet)

    check_existing_header(main_sheet, header)

    get_articles(
        freecodecamp["url"], freecodecamp["class"], extract_fcc_articles, all_articles
    )

    for url in substack["urls"]:
        get_articles(url, substack["class"], extract_substack_articles, all_articles)

    filtered_articles = [
        article for article in all_articles if article[1] not in existing_title
    ]

    for article in filtered_articles:
        print(f"==> {article[1]} is adding now!")
        main_sheet.append_row(list(article))

    main_sheet.sort((1, "des"))



if __name__ == "__main__":
    current = current_time()
    print(f"The process is starting at {current}")
    print()
    main()
    print()
    print("The process is completed")