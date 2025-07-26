import requests
from bs4 import BeautifulSoup

def scrape_quantum_insider(limit=10):
    url = "https://quantuminsider.com/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to load page: {response.status_code}")
    
    soup = BeautifulSoup(response.content, 'html.parser')
    articles = []

    posts = soup.select("article")

    for post in posts[:limit]:
        title_a_tag = post.select_one("h2.post-title > a")
        if title_a_tag:
            title_tag = title_a_tag.get_text(strip=True)
            link_tag = title_a_tag['href']
        else:
            title_tag = None
            link_tag = None
        summary_elem = post.select_one("div.post-excerpt")
        summary_tag = summary_elem.get_text(strip=True) if summary_elem else None
        date_tag = post.select_one("time.entry-date")
        if date_tag:
            date = date_tag['datetime']
        else:
            date = None

        if title_tag and link_tag:
            articles.append({
                "title": title_tag,
                "link": link_tag,
                "summary": summary_tag,
                "date": date
            })

    return articles


