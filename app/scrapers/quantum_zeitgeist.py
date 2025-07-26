import requests
from bs4 import BeautifulSoup

def scrape_quantum_zeitgeist(limit=10):
    url = "https://quantumzeitgeist.com/"
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

    posts = soup.select("li.post h3.entry-title a")

    for post in posts[:limit]:
        title = post.get_text(strip=True)
        link = post['href']
        time_tag = post.find_next("time")
        date = time_tag.get('datetime', '') if time_tag else ""
        articles.append({
            "title": title,
            "link": link,
            "summary": "",  # Summary extraction can be added if needed
            "date": date
        })

    return articles
