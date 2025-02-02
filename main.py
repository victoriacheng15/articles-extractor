import re
from utils.sheet import articles_sheet, get_all_providers, send_articles_sheet
from utils.get_page import get_page
from utils.extractors import provider_dict, get_articles
from utils.format_date import current_time


def main(time):
    all_providers = get_all_providers()

    for provider in all_providers:
        provider_name = provider["name"]
        provider_url = provider["url"]
        provider_element = provider["element"]

        provider_handlers = provider_dict(provider_element)
        handler = provider_handlers.get(provider_name)

        if handler:
            element = handler["element"]()
            extractor = handler["extractor"]

            elements = get_page(provider_url).find_all(element)
            for article_info in get_articles(elements, extractor):
                send_articles_sheet(article_info)
        else:
            print(f"Unknown provider: {provider_name}")

    articles_sheet.sort((1, "des"))
    articles_sheet.update_cell(1, 7, f"Updated at\n{time}")


if __name__ == "__main__":
    date, time = current_time()
    timestamp = f"{date} - {time}"
    print(f"The process is starting at {timestamp}")
    print()
    main(f"{timestamp}")
    print()
    print("The process is completed")
