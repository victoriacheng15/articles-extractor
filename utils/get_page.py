import requests
import logging
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def get_page(url):
    """
    Fetches the HTML content of the given URL and parses it using BeautifulSoup.

    Args:
        url (str): The URL of the page to fetch.

    Returns:
        BeautifulSoup: A BeautifulSoup object containing the parsed HTML content of the page.
    """
    response = requests.get(url)
    if response.status_code != 200:
        logger.error(f"Warning: Status {response.status_code} for {url}")
    # response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")
