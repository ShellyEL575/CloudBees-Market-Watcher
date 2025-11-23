# scrape_only.py — Hardened + Clean Version

import os
import json
import time
from datetime import datetime

from scraper.hn import fetch_hn_stories
from scraper.competitor import fetch_competitor_updates
from scraper.google_watcher import fetch_google_results
from scraper.trend_classifier import classify_trends


def try_fetch(func, name, retries=3, delay=2):
    for attempt in range(1, retries + 1):
        try:
            print(f"➡️  Fetching {name} (attempt {attempt})...")
            return func()
        except Exception as e:
            print(f"❌ {name} failed: {e}")
            if attempt < retries:
                time.sleep(delay)
    print(f"⚠️ {name} permanently failed after {retries} attempts.")
    return []


print("\n📥 Collecting posts...\n")
all_posts = []


# Fetch from all sources
all_posts.extend(try_fetch(fetch_hn_stories, "Hacker News"))
all_posts.extend(try_fetch(fetch_competitor_updates, "Competitor Blogs"))
all_posts.extend(try_fetch(fetch_google_results, "Google Search"))

print(f"\n📌 Total posts collected: {len(all_posts)}")


# Trend classification
for post in all_posts:
    matches = classify_trends([post])
    post["is_trend"] = len(matches) > 0


# Save output
os.makedirs("data", exist_ok=True)
with open("data/posts.json", "w", encoding="utf-8") as f:
    json.dump(all_posts, f, indent=2)

print("\n✅ Saved posts to data/posts.json")
