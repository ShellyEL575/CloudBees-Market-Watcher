# scraper/competitor.py

import feedparser
import yaml
import requests
from bs4 import BeautifulSoup

def clean_feed_content(content):
    # Attempt to sanitize malformed XML using BeautifulSoup
    soup = BeautifulSoup(content, "xml")
    return str(soup)

def fetch_competitor_updates():
    with open("scraper/competitors.yaml") as f:
        urls = yaml.safe_load(f)

    posts = []
    brand_stats = {}

    for brand, feed_urls in urls.items():
        total_entries = 0
        for url in feed_urls:
            try:
                response = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
                response.encoding = 'utf-8'
                cleaned_content = clean_feed_content(response.text)
                feed = feedparser.parse(cleaned_content)
            except Exception as e:
                print(f"❌ Exception while fetching {brand} feed: {url} - {e}")
                continue

            if feed.bozo:
                print(f"❌ Feed parse error for {brand}: {url} (Error: {feed.bozo_exception})")
                continue

            entry_count = len(feed.entries)
            total_entries += entry_count

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

        brand_stats[brand] = total_entries

    print(f"\n✅ Competitor scraper pulled {len(posts)} posts from {len(urls)} brands.")
    for brand, count in brand_stats.items():
        print(f"   - {brand}: {count} posts")
        if count == 0:
            print(f"⚠️ No posts found for {brand}. Check feed URL or source availability.")

    return posts
