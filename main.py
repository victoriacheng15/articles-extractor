from utils.sheet import main_sheet, check_existing_header, send_articles_sheet
from utils.extractors import extract_fcc_articles, extract_substack_articles
from utils.extractors import get_articles
from utils.format_date import current_time
from data.providers import freecodecamp, substack


def main():
    check_existing_header()

    fcc_url = freecodecamp["url"]
    fcc_class = freecodecamp["class"]
    for article_info in get_articles(fcc_url, fcc_class, extract_fcc_articles):
        send_articles_sheet(article_info)

    ss_class = substack["class"]
    for url in substack["urls"]:
        for article_info in get_articles(url, ss_class, extract_substack_articles):
            send_articles_sheet(article_info)

    main_sheet.sort((1, "des"))


if __name__ == "__main__":
    current = current_time()
    print(f"The process is starting at {current}")
    print()
    main()
    print()
    print("The process is completed")
