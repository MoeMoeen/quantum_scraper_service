from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.scrapers.quantum_insider import scrape_quantum_insider
from app.scrapers.testurl import scrape_testurl
from app.scrapers.quantum_zeitgeist import scrape_quantum_zeitgeist

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
    return {"message": "Quantum Scraper API is running."}

@app.get("/quantum-insider")
def get_quantum_insider_articles(limit: int = 10):
    return scrape_quantum_insider(limit=limit)

@app.get("/testurl")
def get_testurl_articles(limit: int = 10):
    return scrape_testurl(limit=limit)

@app.get("/quantum-zeitgeist")
def get_quantum_zeitgeist_articles(limit: int = 10):
    return scrape_quantum_zeitgeist(limit=limit)