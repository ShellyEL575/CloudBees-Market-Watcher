import os
import json
from datetime import datetime
from dotenv import load_dotenv

from scraper.competitor import fetch_competitor_updates
from scraper.reddit import fetch_reddit_discussions
from scraper.hn import fetch_hn_stories
from scraper.google_watcher import fetch_google_results

load_dotenv()

all_posts = []

print("📥 Collecting posts...")

# Competitor Blog Scraping
try:
    competitor_posts = fetch_competitor_updates()
    if isinstance(competitor_posts, list):
        all_posts.extend(competitor_posts)
    else:
        print("❌ Competitor scraping failed: unexpected format")
except Exception as e:
    print(f"❌ Competitor scraping failed: {e}")

# Reddit Discussions
try:
    reddit_posts = fetch_reddit_discussions()
    if isinstance(reddit_posts, list):
        all_posts.extend(reddit_posts)
    else:
        print("❌ Reddit scraping failed: unexpected format")
except Exception as e:
    print(f"❌ Reddit scraping failed: {e}")

# Hacker News
try:
    hn_posts = fetch_hn_stories()
    if isinstance(hn_posts, list):
        all_posts.extend(hn_posts)
    else:
        print("❌ HN scraping failed: unexpected format")
except Exception as e:
    print(f"❌ HN scraping failed: {e}")

# Google Search
try:
    google_posts = fetch_google_results()
    if isinstance(google_posts, list):
        all_posts.extend(google_posts)
        print(f"✅ Google posts: {len(google_posts)}")
    else:
        print("❌ Google scraping failed: unexpected format")
except Exception as e:
    print(f"❌ Google scraping failed: {e}")

# Save to JSON
os.makedirs("data", exist_ok=True)
timestamp = datetime.utcnow().strftime("%Y-%m-%d")
path = f"data/raw_posts.json"
with open(path, "w") as f:
    json.dump(all_posts, f, indent=2)

print(f"✅ Saved {len(all_posts)} posts to {path}")
