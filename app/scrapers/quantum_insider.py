import requests
from bs4 import BeautifulSoup

def scrape_quantum_insider(limit=10):
    # url = "https://thequantuminsider.com/"
    url = "https://www.python.org/blogs/"
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Referer": "https://www.google.com/",
    "DNT": "1",  # Do Not Track
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1"
}

    response = requests.get(url, headers=headers, timeout=10)
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


