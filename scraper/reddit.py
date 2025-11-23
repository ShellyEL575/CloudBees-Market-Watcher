# scraper/reddit.py

import feedparser
import yaml

def fetch_reddit_discussions():
    with open("scraper/reddit.yaml") as f:
        subreddits = yaml.safe_load(f)

    posts = []
    for label, urls in subreddits.items():
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
