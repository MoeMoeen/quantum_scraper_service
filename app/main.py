from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.scrapers.quantum_insider import scrape_quantum_insider
from app.scrapers.testurl import scrape_testurl
from app.scrapers.quantum_zeitgeist import scrape_quantum_zeitgeist, fetch_qz_article_body
from app.scrapers.techcrunch import scrape_techcrunch_quantum, fetch_techcrunch_article_body

app = FastAPI(
    title="Quantum Scraper API",
    description="Serves scraped content from non-RSS quantum news websites",
    version="0.1.0"
)


# Allow all origins for now (for testing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Quantum Scraper API is running on Render."}

@app.get("/quantum-insider")
def get_quantum_insider_articles(limit: int = 10):
    return scrape_quantum_insider(limit=limit)

@app.get("/testurl")
def get_testurl_articles(limit: int = 10):
    return scrape_testurl(limit=limit)

@app.get("/quantum-zeitgeist")
def get_quantum_zeitgeist_articles(limit: int = 10):
    articles = scrape_quantum_zeitgeist(limit=limit)
    for article in articles:
        try:
            article['body'] = fetch_qz_article_body(article['link'])[:1000]  # Fetch and limit body to first 1000 characters
        except Exception as e:
            print(f"Error fetching body for {article['link']}: {e}")
            article['body'] = ""
    
    return articles

@app.get("/techcrunch")
def get_techcrunch_articles(limit: int = 10):
    """Fetch TechCrunch quantum articles and their bodies"""
    articles = scrape_techcrunch_quantum(limit=limit)
    for article in articles:
        try:
            article['body'] = fetch_techcrunch_article_body(article['link'])[:1000]  # Fetch and limit body to first 1000 characters
        except Exception as e:
            print(f"Error fetching body for {article['link']}: {e}")
            article['body'] = ""
    return articles