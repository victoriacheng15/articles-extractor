from utils.get_page import get_page
from utils.format_date import format_date
from utils.sheet import existing_titles


def format_authors(author_elements):
    names = [name.get_text() for name in author_elements]

    if len(names) == 0:
        return "No author found"

    return names[0] if len(names) == 1 else f"{', '.join(names[:-1])} and {names[-1]}"


def extract_fcc_articles(article):
    title = article.find("h2").get_text().strip()
    href = article.find("a").get("href")
    link = f"https://www.freecodecamp.org{href}"
    author = article.find(class_="meta-content").a.get_text().strip()
    date = format_date(article.find("time").get("datetime").split(" (")[0])
    return date, title, author, link, "freeCodeCamp"


def extract_substack_articles(article):
    title = article.find(attrs={"data-testid": "post-preview-title"}).get_text()
    link = article.find(attrs={"data-testid": "post-preview-title"}).get("href")
    author_elements = article.find_all(class_="_link_1o9b1_39")
    author = format_authors(author_elements)
    date = article.find("time").get("datetime").split("T")[0]
    return date, title, author, link, "substack"


def extract_github_articles(article):
    title = article.find("h2").get_text().strip()
    link = article.find(class_="Link--primary").get("href")
    authors = format_authors(
        article.find_all(class_="d-inline-block Link--primary color-fg-default")
    )
    date = article.find("time").get("datetime")
    return date, title, authors, link, "github"


def get_articles(elements, extract_func):
    for article in elements:
        extracted_article_info = extract_func(article)
        if extracted_article_info[1] not in existing_titles:
            yield extracted_article_info
