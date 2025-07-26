import requests
from bs4 import BeautifulSoup, Tag
import re

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
        
        # Look for the date in the entry-meta div
        parent_li = post.find_parent('li')
        date = ""
        if parent_li and hasattr(parent_li, 'select_one'):
            entry_meta = parent_li.select_one('div.entry-meta')
            if entry_meta:
                meta_text = entry_meta.get_text(strip=True)
                # Extract date using regex pattern
                date_match = re.search(r'(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+\d{4}', meta_text)
                if date_match:
                    date = date_match.group(0)
        
        articles.append({
            "title": title,
            "link": link,
            "date": date
        })

    return articles

def fetch_qz_article_body(url: str) -> str:
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Select all <p> tags inside <div class="entry-content">
        content_div = soup.select_one('div.entry-content')
        if not content_div:
            return ""

        paragraphs = content_div.find_all('p')
        text_blocks = [p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)]
        full_text = "\n\n".join(text_blocks)
        return full_text

    except Exception as e:
        print(f"Error fetching body from {url}: {e}")
        return ""