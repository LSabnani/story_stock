from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
from services import get_live_story_stock, get_yahoo_trending_tickers

app = FastAPI(title="Story Stocks API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root():
    return FileResponse("static/index.html")

class StoryStock(BaseModel):
    ticker: str
    company_name: str
    sector: str
    industry: str
    price: float
    change_percent: float
    volume: str
    headline: str
    summary: str
    publisher: Optional[str] = "Yahoo Finance"
    news_url: Optional[str] = "#"
    narrative_category: str
    product_impact: str
    sentiment: str
    sentiment_score: int
    timestamp: str

@app.get("/api/v1/stories", response_model=List[StoryStock])
def get_stories(
    sector: Optional[str] = Query(None, description="Filter by sector"),
    industry: Optional[str] = Query(None, description="Filter by industry"),
    sort_by: Optional[str] = Query("sentiment", description="Sort by: sector, industry, sentiment, change, ticker")
):
    trending_tickers = get_yahoo_trending_tickers()
    stories = []
    
    for ticker in trending_tickers[:12]:
        data = get_live_story_stock(ticker)
        if data:
            stories.append(StoryStock(**data))

    # Filter by sector
    if sector and sector.lower() != "all":
        stories = [s for s in stories if s.sector.lower() == sector.lower()]
        
    # Filter by industry
    if industry and industry.lower() != "all":
        stories = [s for s in stories if s.industry.lower() == industry.lower()]

    # Sort stories
    if sort_by == "sector":
        stories.sort(key=lambda x: (x.sector, x.industry, -x.sentiment_score))
    elif sort_by == "industry":
        stories.sort(key=lambda x: (x.industry, -x.sentiment_score))
    elif sort_by == "change":
        stories.sort(key=lambda x: x.change_percent, reverse=True)
    elif sort_by == "ticker":
        stories.sort(key=lambda x: x.ticker)
    else:  # Default: sentiment score
        stories.sort(key=lambda x: x.sentiment_score, reverse=True)
        
    return stories

@app.get("/api/v1/meta/filters")
def get_filter_options():
    trending_tickers = get_yahoo_trending_tickers()
    stories = []
    for ticker in trending_tickers[:12]:
        data = get_live_story_stock(ticker)
        if data:
            stories.append(data)
            
    sectors = sorted(list(set(s["sector"] for s in stories if s.get("sector"))))
    industries = sorted(list(set(s["industry"] for s in stories if s.get("industry"))))
    return {
        "sectors": ["All"] + sectors,
        "industries": ["All"] + industries
    }

@app.get("/api/v1/stocks/{ticker}")
def get_stock_detail(ticker: str):
    data = get_live_story_stock(ticker)
    if not data:
        return {"error": "Stock ticker not found"}
    return data
