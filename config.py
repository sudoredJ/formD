"""Application configuration."""

import os

# SEC EDGAR
EDGAR_SEARCH_URL = "https://efts.sec.gov/LATEST/search-index"
EDGAR_FILING_URL = "https://www.sec.gov/Archives/edgar/data"
EDGAR_RATE_LIMIT = 10  # requests per second
EDGAR_USER_AGENT = "Jared Mantell mantell99jr@gmail.com"  # SEC requires this

# RSS Feeds
RSS_FEEDS = {
    "prnewswire": "https://www.prnewswire.com/rss/financial-services-latest-news.rss",
    "businesswire": "https://feed.businesswire.com/rss/home/?rss=G1QFDERJXkJeEFpRWg==",
    "globenewswire": "https://www.globenewswire.com/RssFeed/subjectcode/25-Financing%20Agreements/feedTitle/GlobeNewswire%20-%20Financing%20Agreements",
}

# Database
DATABASE_PATH = os.environ.get("DATABASE_PATH", "osint.db")

# Cache TTL
FIRM_CACHE_HOURS = 24
FILING_CACHE_HOURS = 6

