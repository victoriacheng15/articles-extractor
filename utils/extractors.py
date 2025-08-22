import re
import logging
import sys
from datetime import datetime
from utils.format_date import clean_and_convert_date

logger = logging.getLogger(__name__)
# Configure logging to write to stdout for log file capture
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)


def extract_fcc_articles(article):
    """
    Extracts article information from a freeCodeCamp article element.

    Args:
        article (BeautifulSoup element): The article element to extract information from.

    Returns:
        tuple: A tuple containing the date, title, author, link, and source of the article.
    """
    try:
        title = article.find("h2").get_text().strip()
        href = article.find("a").get("href")
        link = f"https://www.freecodecamp.org{href}"
        date = clean_and_convert_date(article.find("time").get("datetime"))
    except Exception as e:
        logger.error(f"Error extracting freeCodeCamp article: {e}")
        raise
    return (date, title, link, "freeCodeCamp")


def extract_substack_articles(article):
    """
    Extracts article information from a Substack article element.

    Args:
        article (BeautifulSoup element): The article element to extract information from.

    Returns:
        tuple: A tuple containing the date, title, author, link, and source of the article.
    """
    try:
        title = (
            article.find(attrs={"data-testid": "post-preview-title"}).get_text().strip()
        )
        link = article.find(attrs={"data-testid": "post-preview-title"}).get("href")
        # Date is assumed to be in a format like "YYYY-MM-DD"
        date = article.find("time").get("datetime").split("T")[0]
    except Exception as e:
        logger.error(f"Error extracting Substack article: {e}")
        raise
    return (date, title, link, "substack")


def extract_github_articles(article):
    """
    Extracts article information from a GitHub article element.

    Args:
        article (BeautifulSoup element): The article element to extract information from.

    Returns:
        tuple: A tuple containing the date, title, author, link, and source of the article.
    """
    try:
        title = article.find("h3").get_text().strip()
        link = article.find(class_="Link--primary").get("href")
        date = article.find("time").get("datetime")
    except Exception as e:
        logger.error(f"Error extracting GitHub article: {e}")
        raise
    return (date, title, link, "github")


def extract_shopify_articles(article):
    """
    Extracts article information from a Shopify article element.

    Args:
        article (BeautifulSoup element): The article element to extract information from.

    Returns:
        tuple: A tuple containing the date, title, author, link, and source of the article.
    """
    try:
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
    except Exception as e:
        logger.error(f"Error extracting Shopify article: {e}")
        raise
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
    for article in elements:
        try:
            article_info = extract_func(article)
            title = article_info[1]
            # article_info tuple now: (date, title, link, source)
            if title not in existing_titles:
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
