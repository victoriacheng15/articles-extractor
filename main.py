import logging
import asyncio
from utils.get_page import PageFetcher
from utils.sheet import articles_sheet, get_all_providers, send_articles_sheet
from utils.extractors import provider_dict, get_articles
from utils.format_date import current_time

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


async def process_provider(fetcher, provider):
    """Process a single provider asynchronously"""
    provider_name = provider["name"]
    provider_url = provider["url"]
    provider_element = provider["element"]

    handlers = provider_dict(provider_element)
    handler = handlers.get(provider_name)

    if not handler:
        logger.info(f"Unknown provider: {provider_name}")
        return

    try:
        soup = await fetcher.get_page(provider_url)
        if not soup:
            return

        element_args = handler["element"]()
        elements = (
            soup.find_all(**element_args)
            if isinstance(element_args, dict)
            else soup.find_all(element_args)
        )

        for article_info in get_articles(elements, handler["extractor"]):
            send_articles_sheet(article_info)

    except Exception as e:
        logger.error(f"Error processing {provider_name}: {str(e)}")


async def async_main(timestamp):
    """Async version of main logic"""
    fetcher = PageFetcher()
    providers = get_all_providers()

    # Process providers sequentially (one at a time)
    for provider in providers:
        await process_provider(fetcher, provider)

    # Final sheet operations
    articles_sheet.sort((1, "des"))
    articles_sheet.update_cell(1, 6, f"Updated at\n{timestamp}")

    await fetcher.close()


def main(timestamp):
    """Sync wrapper for async code"""
    asyncio.run(async_main(timestamp))


if __name__ == "__main__":
    date, time = current_time()
    timestamp = f"{date} - {time}"
    print(f"The process is starting at {timestamp}\n")
    main(timestamp)
    print("\nThe process is completed")
