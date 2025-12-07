import feedparser
import yaml
from bs4 import BeautifulSoup
from datetime import datetime


# --------------------------
# Main Hacker News Scraper
# --------------------------
def fetch_hn_stories():
    with open("scraper/hn.yaml") as f:
        feeds = yaml.safe_load(f)

    posts = []

    for label, urls in feeds.items():
        for url in urls:
            print(f"📥 Fetching HN feed: {label} - {url}")
            feed = feedparser.parse(url)

            for entry in feed.entries:
                # Strip HTML tags from summary
                raw_summary = entry.get("summary", "")
                clean_summary = BeautifulSoup(raw_summary, "html.parser").get_text()

                posts.append({
                    "source": label,
                    "title": entry.title,
                    "url": entry.link,
                    "summary": clean_summary,
                    "type": "💬 Social Buzz",
                    "timestamp": datetime.utcnow().isoformat()
                })

    return posts
