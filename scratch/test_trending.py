import requests

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

def get_yahoo_trending_tickers():
    url = "https://query1.finance.yahoo.com/v1/finance/trending/US"
    try:
        r = requests.get(url, headers=headers, timeout=5)
        data = r.json()
        quotes = data['finance']['result'][0]['quotes']
        tickers = [q['symbol'] for q in quotes]
        print("Trending tickers from Yahoo Finance:", tickers)
        return tickers
    except Exception as e:
        print("Error fetching trending tickers:", e)
        return []

if __name__ == "__main__":
    get_yahoo_trending_tickers()
