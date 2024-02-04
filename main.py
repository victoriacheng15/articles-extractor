import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import Dict, List


def format_date(date: str) -> str:
    date_object = datetime.strptime(date, "%a %b %d %Y %H:%M:%S GMT%z")
    return date_object.strftime("%Y-%m-%d")


def get_articles() -> List[Dict[str, str]]:
    article_list = []
    url = "https://www.freecodecamp.org/news/"
    page = requests.get(url).text
    doc = BeautifulSoup(page, "html.parser")

    articles = doc.find_all(class_="post-card")
    for article in articles:
        obj = {}
        obj["title"] = article.find("h2").get_text().strip()
        href = article.find("a").get("href")
        obj["link"] = f"{url[:-6:]}{href}"
        author_items = article.find("footer")
        obj["author"] = author_items.li.span.a.get_text().strip()
        date = author_items.li.span.time.get("datetime").split(" (")[0]
        obj["date"] = format_date(date)
        obj["category"] = "freeCodeCamp"
        article_list.append(obj)
    return article_list


def main():
    fcc = get_articles()
    print(fcc[0])


if __name__ == "__main__":
    main()
