import requests
from bs4 import BeautifulSoup


def get_page(url: str):
    page = requests.get(url).text
    return BeautifulSoup(page, "html.parser")
