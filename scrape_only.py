import os
import json
import time
from datetime import datetime, timedelta

from scraper.hn import fetch_hn_stories
from scraper.competitor import fetch_competitor_updates
from scraper.competitor_html import fetch_competitor_html_updates
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

def is_recent(post, cutoff_time):
    date_str = post.get("timestamp") or post.get("published_at") or post.get("date")
    if not date_str:
        return False
    try:
        post_time = datetime.fromisoformat(date_str)
        return post_time > cutoff_time
    except Exception:
        return False

print("\n📥 Collecting posts...\n")
all_posts = []

# Fetch from all sources
all_posts.extend(try_fetch(fetch_hn_stories, "Hacker News"))
all_posts.extend(try_fetch(fetch_competitor_updates, "Competitor Blogs"))
all_posts.extend(try_fetch(fetch_google_results, "Google Search"))

print(f"\n📌 Total posts collected: {len(all_posts)}")

# Optional: show timestamps for quick debug
print("\n🔍 Example post timestamps:")
for post in all_posts[:5]:  # Show up to 5
    print(post.get("timestamp") or post.get("published_at") or post.get("date"))

# Filter to only recent posts 
cutoff = datetime.now() - timedelta(days=45)
recent_posts = [post for post in all_posts if is_recent(post, cutoff)]

# Trend classification
for post in recent_posts:
    matches = classify_trends([post])
    post["is_trend"] = len(matches) > 0

# Save output
os.makedirs("data", exist_ok=True)
with open("data/posts.json", "w", encoding="utf-8") as f:
    json.dump(recent_posts, f, indent=2)

print(f"\n✅ Saved {len(recent_posts)} recent posts to data/posts.json")
