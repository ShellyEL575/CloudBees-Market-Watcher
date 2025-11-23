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
                title = entry.get("title")
                link = entry.get("link")
                if not title or not link:
                    print(f"⚠️ Skipping entry missing title or link in {brand}: {entry}")
                    continue
                posts.append({
                    "source": brand,
                    "title": title,
                    "url": link,
                    "summary": entry.get("summary", ""),
                    "type": "🚀 Product Updates"
                })
    return posts
