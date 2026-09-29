import requests
import yfinance as yf
import re
from typing import Dict, List, Any

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

BULLISH_KEYWORDS = [
    "breakthrough", "record", "growth", "approval", "surge", "unveils", "expands",
    "profit", "outperform", "buy", "partner", "beat", "rally", "success", "innovative", "gain", "high"
]
BEARISH_KEYWORDS = [
    "decline", "drop", "loss", "investigation", "lawsuit", "delay", "miss",
    "downgrade", "fall", "warning", "risk", "recall", "cut", "plunge", "slash"
]

def get_yahoo_trending_tickers() -> List[str]:
    """Fetch live trending tickers dynamically directly from Yahoo Finance."""
    url = "https://query1.finance.yahoo.com/v1/finance/trending/US"
    try:
        r = requests.get(url, headers=HEADERS, timeout=5)
        if r.status_code == 200:
            data = r.json()
            quotes = data.get('finance', {}).get('result', [{}])[0].get('quotes', [])
            tickers = [q['symbol'] for q in quotes if 'symbol' in q]
            if tickers:
                return tickers
    except Exception as e:
        print(f"Error fetching trending tickers from Yahoo Finance: {e}")
    
    # Fallback to popular market tickers if API rate-limited
    return ["FICO", "IOVA", "SDEV", "CCL", "NVTS", "DKNG", "AAPL", "AMAT", "RXRX", "LULU"]

def fetch_yahoo_news(ticker: str) -> List[Dict[str, Any]]:
    """Fetch news directly from Yahoo Finance via yfinance for a given ticker."""
    try:
        t = yf.Ticker(ticker)
        news_items = t.news
        return news_items if news_items else []
    except Exception as e:
        print(f"Error fetching news for {ticker}: {e}")
        return []

def analyze_sentiment(text: str) -> Dict[str, Any]:
    """Perform NLP sentiment and impact scoring on story summary/headline."""
    text_lower = text.lower()
    bullish_count = sum(1 for word in BULLISH_KEYWORDS if word in text_lower)
    bearish_count = sum(1 for word in BEARISH_KEYWORDS if word in text_lower)
    
    base_score = 65 + (bullish_count * 8) - (bearish_count * 10)
    score = max(15, min(98, base_score))
    
    if score >= 75:
        sentiment = "Bullish"
    elif score <= 45:
        sentiment = "Bearish"
    else:
        sentiment = "Neutral"
        
    return {
        "sentiment": sentiment,
        "sentiment_score": score
    }

def get_live_story_stock(ticker: str) -> Dict[str, Any]:
    """Fetch ticker details, market metrics, sector, industry, and top story from Yahoo Finance."""
    try:
        t = yf.Ticker(ticker)
        info = t.info
        
        company_name = info.get("shortName") or info.get("longName") or ticker
        sector = info.get("sector") or "Technology"
        industry = info.get("industry") or "General"
        price = info.get("regularMarketPrice") or info.get("currentPrice") or 0.0
        prev_close = info.get("regularMarketPreviousClose") or info.get("previousClose") or price
        
        if prev_close and prev_close > 0:
            change_percent = ((price - prev_close) / prev_close) * 100
        else:
            change_percent = 0.0

        volume_num = info.get("regularMarketVolume") or info.get("volume") or 0
        if volume_num >= 1_000_000:
            volume_str = f"{volume_num / 1_000_000:.1f}M"
        elif volume_num >= 1_000:
            volume_str = f"{volume_num / 1_000:.1f}K"
        else:
            volume_str = str(volume_num)

        news = fetch_yahoo_news(ticker)
        if news:
            top_article = news[0]
            title = top_article.get("title") or top_article.get("headline") or f"{ticker} Trending on Yahoo Finance"
            publisher = top_article.get("publisher") or "Yahoo Finance"
            summary = top_article.get("summary") or title
            link = top_article.get("link") or f"https://finance.yahoo.com/quote/{ticker}"
        else:
            title = f"{company_name} Currently Trending on Yahoo Finance"
            publisher = "Yahoo Finance"
            summary = info.get("longBusinessSummary") or f"High momentum and volume activity detected on Yahoo Finance for {company_name}."
            link = f"https://finance.yahoo.com/quote/{ticker}"

        if len(summary) > 220:
            summary = summary[:217] + "..."

        sentiment_res = analyze_sentiment(title + " " + summary)

        return {
            "ticker": ticker.upper(),
            "company_name": company_name,
            "sector": sector,
            "industry": industry,
            "price": float(price),
            "change_percent": round(float(change_percent), 2),
            "volume": volume_str,
            "headline": title,
            "summary": summary,
            "publisher": publisher,
            "news_url": link,
            "narrative_category": f"{sector} Trending",
            "product_impact": f"Trending Yahoo Finance ticker in {industry} due to high volume & news velocity.",
            "sentiment": sentiment_res["sentiment"],
            "sentiment_score": sentiment_res["sentiment_score"],
            "timestamp": "Trending Now"
        }

    except Exception as e:
        print(f"Error fetching live stock data for {ticker}: {e}")
        return None
