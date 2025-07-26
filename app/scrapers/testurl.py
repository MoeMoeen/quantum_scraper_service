import requests
from bs4 import BeautifulSoup

def scrape_testurl(limit=10):
    url = "https://www.python.org/blogs/"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    print(response.text[:1000])  # Print the first 1000 characters of the response for debugging

    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    articles = []

    for post in soup.select("ul.list-recent-posts li")[:limit]:
        title_tag = post.find("a")
        date_tag = post.find("time")

        articles.append({
            "title": title_tag.text.strip() if title_tag else "",
            "link": title_tag["href"] if title_tag and title_tag.has_attr("href") else "",
            "summary": "",
            "date": date_tag["datetime"] if date_tag and date_tag.has_attr("datetime") else ""
        })

    return articles