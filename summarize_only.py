import os
import json
import time
from datetime import datetime
from scraper.hn import fetch_hn_stories
from scraper.competitor import fetch_competitor_updates
from scraper.google_watcher import fetch_google_results
# from scraper.linkedin_watcher import fetch_linkedin_results  # removed, file not present
from scraper.trend_classifier import classify_trends

def try_fetch(func, name, retries=2, delay=2):
    for attempt in range(retries):
        try:
            print(f"➡️  Fetching {name} (attempt {attempt+1})...")
            return func()
        except Exception as e:
            print(f"❌ {name} failed: {e}")
            time.sleep(delay)
    return []

all_posts = []

print("\n📥 Collecting posts...")

all_posts.extend(try_fetch(fetch_hn_stories, "Hacker News"))
all_posts.extend(try_fetch(fetch_competitor_updates, "Competitors"))
all_posts.extend(try_fetch(fetch_google_results, "Google"))
# LinkedIn disabled because linkedin_watcher.py is missing

print(f"\n📌 Total posts collected: {len(all_posts)}")

# Classify trends
for post in all_posts:
    text = (post.get("title") or "") + " " + (post.get("summary") or "")
    post["is_trend"] = classify_trends(text)

# Save scraped posts
os.makedirs("data", exist_ok=True)
output_path = "data/posts.json"

with open(output_path, "w") as f:
    json.dump(all_posts, f, indent=2)

print(f"\n✅ Saved {len(all_posts)} posts to {output_path}")
