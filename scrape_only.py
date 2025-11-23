import os
from scraper.hn import fetch_hn_stories
from scraper.competitor import fetch_competitor_updates
from scraper.reddit import fetch_reddit_posts
from scraper.google_watcher import fetch_google_results
from scraper.linkedin_watcher import fetch_linkedin_results
from scraper.trend_classifier import classify_trends

all_posts = []

print("\n📥 Collecting posts...")

# Collect posts from all sources
try:
    all_posts.extend(fetch_hn_stories())
except Exception as e:
    print(f"❌ Hacker News scraping failed: {e}")

try:
    all_posts.extend(fetch_competitor_updates())
except Exception as e:
    print(f"❌ Competitor scraping failed: {e}")

try:
    all_posts.extend(fetch_reddit_posts())
except Exception as e:
    print(f"❌ Reddit scraping failed: {e}")

try:
    all_posts.extend(fetch_google_results())
except Exception as e:
    print(f"❌ Google scraping failed: {e}")

try:
    all_posts.extend(fetch_linkedin_results())
except Exception as e:
    print(f"❌ LinkedIn scraping failed: {e}")

# Classify trends
for post in all_posts:
    post["is_trend"] = classify_trends(post.get("title", "") + " " + post.get("summary", ""))

# Save scraped posts to a file
import json
from datetime import datetime

os.makedirs("data", exist_ok=True)
date_str = datetime.utcnow().strftime("%Y-%m-%d")
output_path = f"data/posts_{date_str}.json"

with open(output_path, "w") as f:
    json.dump(all_posts, f, indent=2)

print(f"\n✅ Saved {len(all_posts)} posts to {output_path}")
