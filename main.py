from utils.sheet import main_sheet, send_articles_sheet
from utils.extractors import (
    extract_fcc_articles,
    extract_substack_articles,
    extract_github_articles,
    extract_ztm_articles,
)
from utils.extractors import get_articles
from utils.format_date import current_time
from data.providers import freecodecamp, substack, github, ztm
from utils.get_page import get_page


def main(time):
    fcc_url = freecodecamp["url"]
    fcc_element = freecodecamp["element"]
    elements = get_page(fcc_url).find_all(fcc_element)
    for article_info in get_articles(elements, extract_fcc_articles):
        send_articles_sheet(article_info)

    gh_url = github["url"]
    gh_element = github["element"]
    elements = get_page(gh_url).find_all(gh_element)
    for article_info in get_articles(elements, extract_github_articles):
        send_articles_sheet(article_info)

    ss_element = substack["element"]
    for url in substack["urls"]:
        elements = get_page(url).find_all(class_=ss_element)
        for article_info in get_articles(elements, extract_substack_articles):
            send_articles_sheet(article_info)

    ztm_url = ztm["url"]
    ztm_element = ztm["element"]
    elements = get_page(ztm_url).find_all(class_=ztm_element)
    for article_info in get_articles(elements, extract_ztm_articles):
        send_articles_sheet(article_info)

    main_sheet.sort((1, "des"))
    main_sheet.update_cell(1, 7, f"Updated at\n{time}")


if __name__ == "__main__":
    date, time = current_time()
    print(f"The process is starting at Updated at {date} - {time}")
    print()
    main(f"{date}\n{time}")
    print()
    print("The process is completed")
