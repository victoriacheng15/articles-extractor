import logging
import asyncio
from utils import (
    # Sheet operations
    get_client,
    get_worksheet,
    get_all_providers,
    get_all_titles,
    append_article,
    SHEET_ID,
    # Web scraping
    init_fetcher_state,
    fetch_page,
    close_fetcher,
    # Article extraction
    provider_dict,
    get_articles,
    # Date utilities
    current_time,
    # Constants
    ARTICLES_WORKSHEET,
    PROVIDERS_WORKSHEET,
)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


async def process_provider(fetcher_state, provider, articles_sheet, existing_titles):
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
        soup, fetcher_state = await fetch_page(fetcher_state, provider_url)
        if not soup:
            logger.warning(f"Failed to fetch page for {provider_name}")
            return fetcher_state

        element_args = handler["element"]()
        elements = (
            soup.find_all(**element_args)
            if isinstance(element_args, dict)
            else soup.find_all(element_args)
        )

        articles_found = 0
        for article_info in get_articles(
            elements, handler["extractor"], existing_titles
        ):
            append_article(articles_sheet, article_info)
            articles_found += 1
        
        logger.info(f"Processed {provider_name}: {articles_found} new articles found")

    except Exception as e:
        logger.error(f"Error processing {provider_name}: {str(e)}", exc_info=True)
    
    return fetcher_state


async def async_main(timestamp):
    client = get_client()
    articles_sheet = get_worksheet(client, SHEET_ID, ARTICLES_WORKSHEET)
    providers_sheet = get_worksheet(client, SHEET_ID, PROVIDERS_WORKSHEET)

    existing_titles = get_all_titles(articles_sheet)
    providers = get_all_providers(providers_sheet)

    fetcher_state = init_fetcher_state()

    for provider in providers:
        await process_provider(fetcher_state, provider, articles_sheet, existing_titles)

    articles_sheet.sort((1, "des"))
    articles_sheet.update_cell(1, 6, f"Updated at\n{timestamp}")
    await close_fetcher(fetcher_state)


def main(timestamp):
    """Sync wrapper for async code"""
    asyncio.run(async_main(timestamp))


if __name__ == "__main__":
    date, time = current_time()
    timestamp = f"{date} - {time}"
    print(f"The process is starting at {timestamp}\n")
    main(timestamp)
    print("\nThe process is completed")
