from utils.get_page import get_page
from utils.format_date import format_date


def extract_fcc_articles(article):
    obj = {}
    obj["title"] = article.find("h2").get_text().strip()
    href = article.find("a").get("href")
    obj["link"] = f"https://www.freecodecamp.org{href}"
    author_items = article.find("footer")
    obj["author"] = author_items.li.span.a.get_text().strip()
    date = author_items.li.span.time.get("datetime").split(" (")[0]
    obj["date"] = format_date(date)
    obj["category"] = "freeCodeCamp"
    return obj


def get_articles(url, class_name, extract_func, all_articles):
    doc = get_page(url)
    articles = doc.find_all(class_=class_name)
    for article in articles:
        obj = extract_func(article)
        all_articles.append(obj)
