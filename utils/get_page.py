import requests
from bs4 import BeautifulSoup


def get_page(url):
    """
    Fetches the HTML content of the given URL and parses it using BeautifulSoup.

    Args:
        url (str): The URL of the page to fetch.

    Returns:
        BeautifulSoup: A BeautifulSoup object containing the parsed HTML content of the page.
    """
    page = requests.get(url).text
    return BeautifulSoup(page, "html.parser")
