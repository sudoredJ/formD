"""RSS feed polling for press releases."""

import feedparser
from datetime import datetime
from dataclasses import dataclass

from config import RSS_FEEDS


@dataclass
class PressRelease:
    source: str
    title: str
    url: str
    published_at: datetime
    summary: str


def fetch_feed(source: str, url: str) -> list[PressRelease]:
    """Fetch and parse a single RSS feed."""
    feed = feedparser.parse(url)
    releases = []
    
    for entry in feed.entries:
        if hasattr(entry, "published_parsed") and entry.published_parsed:
            published = datetime(*entry.published_parsed[:6])
        else:
            published = datetime.now()
        
        releases.append(PressRelease(
            source=source,
            title=entry.get("title", ""),
            url=entry.get("link", ""),
            published_at=published,
            summary=entry.get("summary", ""),
        ))
    
    return releases


def search_releases(firm_name: str) -> list[PressRelease]:
    """Search all RSS feeds for mentions of a firm."""
    all_releases = []
    
    for source, url in RSS_FEEDS.items():
        try:
            releases = fetch_feed(source, url)
            all_releases.extend(releases)
        except Exception as e:
            print(f"Error fetching {source}: {e}")
            continue
    
    firm_lower = firm_name.lower()
    matched = [
        r for r in all_releases 
        if firm_lower in r.title.lower() or firm_lower in r.summary.lower()
    ]
    
    matched.sort(key=lambda x: x.published_at, reverse=True)
    return matched

