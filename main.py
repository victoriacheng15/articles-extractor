import logging
from utils.sheet import articles_sheet, get_all_providers, send_articles_sheet
from utils.get_page import get_page
from utils.extractors import provider_dict, get_articles
from utils.format_date import current_time

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def main(timestamp):
    """
    Extracts articles from various providers and updates the Google Sheet.
    """
    providers = get_all_providers()
    for provider in providers:
        provider_name = provider["name"]
        provider_url = provider["url"]
        provider_element = provider["element"]

        handlers = provider_dict(provider_element)
        handler = handlers.get(provider_name)

        if handler:
            element_args = handler["element"]()
            extractor = handler["extractor"]

            # Choose find_all argument format based on element_args type.
            if isinstance(element_args, dict):
                elements = get_page(provider_url).find_all(**element_args)
            else:
                elements = get_page(provider_url).find_all(element_args)

            for article_info in get_articles(elements, extractor):
                send_articles_sheet(article_info)
        else:
            logger.info(f"Unknown provider: {provider_name}")

    # Assuming sorting and timestamp updating is still required.
    articles_sheet.sort((1, "des"))
    articles_sheet.update_cell(1, 6, f"Updated at\n{timestamp}")


if __name__ == "__main__":
    date, time = current_time()
    timestamp = f"{date} - {time}"
    print(f"The process is starting at {timestamp}\n")
    main(timestamp)
    print("\nThe process is completed")
