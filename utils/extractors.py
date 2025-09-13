import re
import logging
import sys
from datetime import datetime
from utils.format_date import clean_and_convert_date


logger = logging.getLogger(__name__)
# Configure logging to write to stdout for log file capture
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stdout,
)


# Error handling decorator for extractors
def extractor_error_handler(site_name):
    def decorator(func):
        def wrapper(article):
            try:
                return func(article)
            except Exception as e:
                logger.error(f"Error extracting {site_name} article: {e}")
                raise

        return wrapper

    return decorator


@extractor_error_handler("freeCodeCamp")
def extract_fcc_articles(article):
    """
    Extracts article information from a freeCodeCamp article element.
    """
    title = article.find("h2").get_text().strip()
    href = article.find("a").get("href")
    link = f"https://www.freecodecamp.org{href}"
    date = clean_and_convert_date(article.find("time").get("datetime"))
    return (date, title, link, "freeCodeCamp")


@extractor_error_handler("Substack")
def extract_substack_articles(article):
    """
    Extracts article information from a Substack article element.
    """
    title = article.find(attrs={"data-testid": "post-preview-title"}).get_text().strip()
    link = article.find(attrs={"data-testid": "post-preview-title"}).get("href")
    # Date is assumed to be in a format like "YYYY-MM-DD"
    date = article.find("time").get("datetime").split("T")[0]
    return (date, title, link, "substack")


@extractor_error_handler("GitHub")
def extract_github_articles(article):
    """
    Extracts article information from a GitHub article element.
    """
    title = article.find("h3").get_text().strip()
    link = article.find(class_="Link--primary").get("href")
    date = article.find("time").get("datetime")
    return (date, title, link, "github")


@extractor_error_handler("Shopify")
def extract_shopify_articles(article):
    """
    Extracts article information from a Shopify article element.
    """
    title_element = article.find(
        "a",
        {
            "class": lambda x: x
            and "tracking-[-.02em]" in x
            and "pb-4" in x
            and "hover:underline" in x,
            "target": "_self",
            "rel": "",
        },
    )
    title = title_element.get_text().strip()
    blog_address = title_element.get("href")
    link = f"https://shopify.engineering{blog_address}"
    date_element = (
        article.find(
            "p",
            class_="richtext text-body-sm font-normal text-engineering-dark-author-text font-sans",
        )
        .get_text()
        .strip()
    )
    before_format_date = datetime.strptime(date_element, "%b %d, %Y")
    date = before_format_date.strftime("%Y-%m-%d")
    return (date, title, link, "shopify")


def get_articles(elements, extract_func, existing_titles):
    """
    Extracts articles from a given provider.

    Args:
        elements (list): A list of BeautifulSoup elements representing articles.
        extract_func (function): The function to use for extracting article information.

    Yields:
        tuple: A tuple containing the extracted article information.
    """
    # Normalize existing titles for comparison
    normalized_existing_titles = set(t.strip().lower() for t in existing_titles)
    for article in elements:
        try:
            article_info = extract_func(article)
            title = article_info[1]
            normalized_title = title.strip().lower()
            # article_info tuple now: (date, title, link, source)
            if normalized_title not in normalized_existing_titles:
                yield article_info
        except Exception as e:
            logger.error(f"Skipping an article due to error: {e}")


def provider_dict(provider_element):
    """
    Returns a dictionary mapping provider names to their corresponding elements and extractor functions.

    Args:
        provider_element (str): The element or class name used to identify articles from the provider.

    Returns:
        dict: A dictionary containing the provider's element and extractor function.
    """
    return {
        "freecodecamp": {
            "element": lambda: provider_element,
            "extractor": extract_fcc_articles,
        },
        "substack": {
            "element": lambda: {"class_": re.compile(provider_element)},
            "extractor": extract_substack_articles,
        },
        "github": {
            "element": lambda: provider_element,
            "extractor": extract_github_articles,
        },
        "shopify": {
            "element": lambda: provider_element,
            "extractor": extract_shopify_articles,
        },
    }
