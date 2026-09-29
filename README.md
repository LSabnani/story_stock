# 📈 Story Stocks

**Story Stocks** is an intelligent web application designed to track, analyze, and summarize stocks driving high momentum due to breaking news, breakthrough product launches, regulatory approvals, or viral market stories.

Powered by a **Python FastAPI** backend and **Yahoo Finance News Feeds**, Story Stocks helps investors instantly understand *why* a stock is trending, evaluate its product/service impact, and group/sort stories by **Sector** and **Industry**.

---

## ✨ Features

- **Live Yahoo Finance Trending Feed**: Dynamically queries Yahoo Finance's live trending tickers feed (`query1.finance.yahoo.com/v1/finance/trending/US`) to automatically display top market-moving stocks.
- **News Feed Integration**: Fetches breaking stock headlines, press releases, and summaries directly from Yahoo Finance.
- **Sector & Industry Grouping & Sorting**: Sort and filter stories by Sector (*Technology, Healthcare, Consumer Cyclical, etc.*) and Industry (*Semiconductors, Biotechnology, Auto Manufacturers, etc.*).
- **Sentiment & Impact Scoring**: Performs NLP-based sentiment analysis (Bullish / Neutral / Bearish) and calculates a narrative score (0–100).
- **On-the-Fly Ticker Lookup**: Search and analyze any ticker symbol in real-time (e.g., `FICO`, `IOVA`, `SDEV`, `CCL`, `NVTS`, `DKNG`, `AAPL`, `AMAT`).
- **Modern Dark UI**: High-aesthetic dashboard built with glassmorphism UI cards, responsive grid layouts, and direct links to full Yahoo Finance articles.

---

## 🛠️ Architecture & Tech Stack

- **Backend**: Python 3.10+, FastAPI, `yfinance`, `pandas`, `httpx`, `pydantic`, `uvicorn`
- **Frontend**: HTML5, Vanilla CSS (Glassmorphism Dark Mode), JavaScript (Async Fetch API)
- **Data Source**: Yahoo Finance API & News Feeds via `yfinance`

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- Python 3.10+ installed
- Virtual environment setup (`.venv`)

### 2. Installation & Setup

```bash
# Activate virtual environment (Windows PowerShell)
.\.venv\Scripts\Activate.ps1

# Install required packages
pip install -r requirements.txt
```

### 3. Running the Server

Start the FastAPI server using Uvicorn:

```bash
python -m uvicorn main:app --reload --port 8000
```

### 4. Access the Dashboard
Open your web browser and navigate to:
```text
http://127.0.0.1:8000/
```

---

## 📡 API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/` | `GET` | Serves the web dashboard UI |
| `/api/v1/stories` | `GET` | Fetch stories (Query params: `sort_by`, `sector`, `industry`) |
| `/api/v1/meta/filters` | `GET` | Retrieve available sector and industry filter choices |
| `/api/v1/stocks/{ticker}` | `GET` | Fetch live story, quote, and sentiment analysis for a specific ticker |

---

## 📂 Project Structure

```text
story_stock/
├── main.py              # FastAPI server routes & app definition
├── services.py          # Yahoo Finance news fetching & NLP sentiment engine
├── requirements.txt     # Python project dependencies
├── static/
│   └── index.html       # Web UI dashboard frontend
└── README.md            # Project documentation
```

---

## 📄 License
MIT License
