from bs4 import BeautifulSoup, Tag
import requests
import re
from datetime import datetime

def scrape_techcrunch_quantum(limit=10):
    """
    Scraper for TechCrunch's quantum computing tag page.
    
    Args:
        limit (int): Maximum number of articles to return
        
    Returns:
        list: List of article dictionaries with title, link, date, and summary
    """
    
    url = "https://techcrunch.com/tag/quantum-computing/"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code != 200:
            print(f"HTTP {response.status_code}: Unable to access TechCrunch")
            return []
        
        # Handle encoding properly
        response.encoding = response.apparent_encoding or 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = []
        
        # Find all h3 tags and look for quantum computing articles
        h3_tags = soup.find_all('h3')
        
        for h3 in h3_tags:
            if len(articles) >= limit:
                break
            
            # Check if h3 is a Tag object before using find_all
            if not isinstance(h3, Tag):
                continue
                
            # Find anchor tags within each h3
            a_tags = h3.find_all('a')
            
            for a_tag in a_tags:
                # Check if a_tag is a Tag object
                if not isinstance(a_tag, Tag):
                    continue
                    
                href = str(a_tag.get('href', ''))
                title = str(a_tag.get_text(strip=True))
                
                # Filter for valid TechCrunch quantum articles
                if not href or not title:
                    continue
                    
                if not ('techcrunch.com' in str(href) and '/2025/' in str(href)):
                    continue
                    
                if len(title) < 10:  # Skip very short titles
                    continue
                
                try:
                    # Extract date from URL pattern (e.g., /2025/07/16/)
                    date = ""
                    date_match = re.search(r'/(\d{4})/(\d{2})/(\d{2})/', str(href))
                    if date_match:
                        year, month, day = date_match.groups()
                        try:
                            # Convert to readable format
                            date_obj = datetime(int(year), int(month), int(day))
                            date = date_obj.strftime("%b %d, %Y")  # e.g., "Jul 16, 2025"
                        except ValueError:
                            date = f"{year}-{month}-{day}"
                    
                    # Create article entry
                    articles.append({
                        "title": title,
                        "link": str(href),
                        "date": date,
                        "source": "TechCrunch"
                    })
                    
                    break  # Only take the first valid article from each h3
                    
                except Exception as e:
                    print(f"Error processing article: {e}")
                    continue
        
        return articles
        
    except requests.exceptions.RequestException as e:
        print(f"Network error accessing TechCrunch: {e}")
        return []
    except Exception as e:
        print(f"Error parsing TechCrunch content: {e}")
        return []

def fetch_techcrunch_article_body(url: str) -> str:
    """
    Fetch the full article body from a TechCrunch article URL.
    
    Args:
        url (str): TechCrunch article URL
        
    Returns:
        str: Full article text content
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://techcrunch.com/"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # TechCrunch typically uses .article-content or similar for article body
        content_selectors = [
            '.article-content',
            '.entry-content', 
            '.post-content',
            'article .content',
            '[class*="article-body"]'
        ]
        
        for selector in content_selectors:
            content_div = soup.select_one(selector)
            if content_div:
                # Extract text from paragraphs
                paragraphs = content_div.find_all('p')
                text_blocks = [p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)]
                if text_blocks:
                    return "\\n\\n".join(text_blocks)
        
        # Fallback: look for multiple paragraphs in article
        article = soup.find('article')
        if article and isinstance(article, Tag):
            paragraphs = article.find_all('p')
            text_blocks = [p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)]
            if len(text_blocks) > 2:  # Ensure it's substantial content
                return "\n\n".join(text_blocks)
        
        return ""
        
    except Exception as e:
        print(f"Error fetching TechCrunch article body from {url}: {e}")
        return ""

# For backwards compatibility, create an alias
scrape_techcrunch = scrape_techcrunch_quantum

if __name__ == "__main__":
    # Test the scraper
    print("Testing TechCrunch Quantum Computing scraper...")
    articles = scrape_techcrunch_quantum(limit=5)
    
    print(f"\\nFound {len(articles)} articles:")
    for i, article in enumerate(articles, 1):
        print(f"\\n{i}. {article['title']}")
        print(f"   Date: {article['date']}")
        print(f"   Link: {article['link']}")
        if article['summary']:
            print(f"   Summary: {article['summary'][:100]}...")
