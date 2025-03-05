import re
from datetime import datetime
from utils.format_date import clean_and_convert_date
from utils.sheet import existing_titles


def format_authors(author_elements):
    """
    Formats a list of author elements into a single string.

    Args:
        author_elements (list): A list of BeautifulSoup elements representing authors.

    Returns:
        str: A formatted string of authors.
    """
    names = [name.get_text() for name in author_elements]

    if len(names) == 0:
        return "No author found"

    return names[0] if len(names) == 1 else f"{', '.join(names[:-1])} and {names[-1]}"


def extract_fcc_articles(article):
    """
    Extracts article information from a freeCodeCamp article element.

    Args:
        article (BeautifulSoup element): The article element to extract information from.

    Returns:
        tuple: A tuple containing the date, title, author, link, and source of the article.
    """
    title = article.find("h2").get_text().strip()
    href = article.find("a").get("href")
    link = f"https://www.freecodecamp.org{href}"
    meta_item = article.find("a", class_="meta-item")
    author = meta_item.get_text().strip() if meta_item is not None else "No Author"
    date = clean_and_convert_date(article.find("time").get("datetime"))
    return (date, title, author, link, "freeCodeCamp")


def extract_substack_articles(article):
    """
    Extracts article information from a Substack article element.

    Args:
        article (BeautifulSoup element): The article element to extract information from.

    Returns:
        tuple: A tuple containing the date, title, author, link, and source of the article.
    """
    title = article.find(attrs={"data-testid": "post-preview-title"}).get_text()
    link = article.find(attrs={"data-testid": "post-preview-title"}).get("href")
    author_elements = article.find_all(class_=re.compile("profile-hover-card-target "))
    author = format_authors(author_elements)
    date = article.find("time").get("datetime").split("T")[0]
    return (date, title, author, link, "substack")


def extract_github_articles(article):
    """
    Extracts article information from a GitHub article element.

    Args:
        article (BeautifulSoup element): The article element to extract information from.

    Returns:
        tuple: A tuple containing the date, title, author, link, and source of the article.
    """
    title = article.find("h3").get_text().strip()
    link = article.find(class_="Link--primary").get("href")
    authors = format_authors(
        article.find_all(class_="d-inline-block Link--primary color-fg-default")
    )
    date = article.find("time").get("datetime")
    return (date, title, authors, link, "github")


def extract_shopify_articles(article):
    """
    Extracts article information from a Shopify article element.

    Args:
        article (BeautifulSoup element): The article element to extract information from.

    Returns:
        tuple: A tuple containing the date, title, author, link, and source of the article.
    """
    title_element = article.find("a", {"class": lambda x: x and "tracking-[-.02em]" in x and "pb-4" in x and "hover:underline" in x,"target": "_self", "rel": ""})
    title = title_element.get_text().strip()
    link=f"https://shopify.engineering{title_element.get("href")}"
    authors="N/A"
    date_element = article.find("p", class_="richtext text-body-sm font-normal text-engineering-dark-author-text font-sans").get_text().strip()
    before_format_date = datetime.strptime(date_element, "%b %d, %Y")
    date = before_format_date.strftime("%Y-%m-%d")

    return (date, title, authors, link, "shopify")


def get_articles(elements, extract_func):
    """
    Extracts articles from a given provider.

    Args:
        elements (list): A list of BeautifulSoup elements representing articles.
        extract_func (function): The function to use for extracting article information.

    Yields:
        tuple: A tuple containing the extracted article information.
    """
    for article in elements:
        extracted_article_info = extract_func(article)
        if extracted_article_info[1] not in existing_titles:
            yield extracted_article_info


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
            "extractor": extract_shopify_articles
        }
    }
