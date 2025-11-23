import os
import json
import time
from datetime import datetime

from scraper.hn import fetch_hn_stories
from scraper.competitor import fetch_competitor_updates
from scraper.google_watcher import fetch_google_results
from scraper.trend_classifier import classify_trends


def try_fetch(func, name, retries=2, delay=2):
    """
    Retry-safe wrapper around each scraper function.
    """
    for attempt in range(retries):
        try:
            print(f"➡️  Fetching {name} (attempt {attempt + 1})...")
            return func()
        except Exception as e:
            print(f"❌ {name} failed: {e}")
            time.sleep(delay)

    print(f"⚠️ {name} permanently failed after {retries} attempts.")
    return []


print("\n📥 Collecting posts...\n")
all_posts = []

# === ACTIVE SOURCES ===
all_posts.extend(try_fetch(fetch_hn_stories, "Hacker News"))
all_posts.extend(try_fetch(fetch_competitor_updates, "Competitors"))
all_posts.extend(try_fetch(fetch_google_results, "Google Search (Serper)"))

print(f"\n📌 Total posts collected: {len(all_posts)}")

# === TREND CLASSIFICATION ===
for post in all_posts:
    # classify_trends expects a LIST of posts, not a single string
    result = classify_trends([post])
    post["is_trend"] = len(result) > 0


# === SAVE RESULTS ===
os.makedirs("data", exist_ok=True)
output_path = "data/posts.json"

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(all_posts, f, indent=2)

print(f"\n✅ Saved {len(all_posts)} posts to {output_path}")
