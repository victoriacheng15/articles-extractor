from utils.sheet import articles_sheet, get_all_providers, send_articles_sheet
from utils.get_page import get_page
from utils.extractors import get_articles
from utils.extractors import (
    extract_fcc_articles,
    extract_substack_articles,
    extract_github_articles,
)
from utils.format_date import current_time
import re

def add_articles_sheet(provider, provider_url, provider_element):
    if provider == "freecodecamp":
        elements = get_page(provider_url).find_all(provider_element)
        for article_info in get_articles(elements, extract_fcc_articles):
            send_articles_sheet(article_info)
    elif provider == "substack":
        elements = get_page(provider_url).find_all(class_=re.compile(provider_element))
        for article_info in get_articles(elements, extract_substack_articles):
            send_articles_sheet(article_info)
    elif provider == "github":
        elements = get_page(provider_url).find_all(provider_element)
        for article_info in get_articles(elements, extract_github_articles):
            send_articles_sheet(article_info)


def main(time):
    all_providers = get_all_providers()

    for provider in all_providers:
        provider_name = provider["name"]
        provider_url = provider["url"]
        provider_element = provider["element"]
        add_articles_sheet(provider_name, provider_url, provider_element)

    articles_sheet.sort((1, "des"))
    articles_sheet.update_cell(1, 7, f"Updated at\n{time}")


if __name__ == "__main__":
    date, time = current_time()
    timestamp = f"{date} - {time}"
    print(f"The process is starting at Updated at {timestamp}")
    print()
    main(f"{timestamp}")
    print()
    print("The process is completed")
