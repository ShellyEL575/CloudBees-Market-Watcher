# scraper/hn.py

import feedparser
import yaml

def fetch_hn_links():
    with open("scraper/hn.yaml") as f:
        feeds = yaml.safe_load(f)

    posts = []
    for label, urls in feeds.items():
        for url in urls:
            feed = feedparser.parse(url)
            for entry in feed.entries:
                posts.append({
                    "source": label,
                    "title": entry.title,
                    "url": entry.link,
                    "summary": entry.get("summary", ""),
                    "type": "💬 Social Buzz"
                })
    return posts
