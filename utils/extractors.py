from utils.get_page import get_page
from utils.format_date import format_date


def extract_fcc_articles(article):
    title = article.find("h2").get_text().strip()
    href = article.find("a").get("href")
    link = f"https://www.freecodecamp.org{href}"
    author_items = article.find("footer")
    author = author_items.li.span.a.get_text().strip()
    date = author_items.li.span.time.get("datetime").split(" (")[0]
    date = format_date(date)
    return date, title, author, link, "freeCodeCamp"

def extract_substack_articles(article):
    all_element = article.find_all("a")
    title = all_element[0].get_text()
    link = all_element[0].get("href")
    author = all_element[-1].get_text() if len(all_element) == 3 else "Cannot find author name"
    date = article.find("time").get("datetime").split("T")[0]
    return date, title, author, link, "substack"


def get_articles(url, class_name, extract_func, all_articles):
    doc = get_page(url)
    articles = doc.find_all(class_=class_name)
    for article in articles:
        obj = extract_func(article)
        all_articles.append(obj)
