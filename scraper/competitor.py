# scraper/competitor.py

import feedparser
import yaml

def fetch_competitor_updates():
    with open("scraper/competitors.yaml") as f:
        urls = yaml.safe_load(f)

    posts = []
    for brand, feed_urls in urls.items():
        for url in feed_urls:
            feed = feedparser.parse(url)
            for entry in feed.entries:
                posts.append({
                    "source": brand,
                    "title": entry.title,
                    "url": entry.link,
                    "summary": entry.get("summary", ""),
                    "type": "🚀 Product Updates"
                })
    return posts
