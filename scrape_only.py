import json
from datetime import datetime
from scraper.competitor import fetch_competitor_updates
from scraper.reddit import fetch_reddit_discussions
from scraper.hn import fetch_hn_stories
from scraper.google_watcher import fetch_google_posts

# Output path
RAW_POSTS_PATH = "data/raw_posts.json"

# Collect all posts
all_posts = []

print("\n📥 Collecting posts...")

try:
    competitor_posts = fetch_competitor_updates()
    all_posts.extend(competitor_posts)
except Exception as e:
    print(f"❌ Competitor scraping failed: {e}")

try:
    reddit_posts = fetch_reddit_discussions()
    all_posts.extend(reddit_posts)
except Exception as e:
    print(f"❌ Reddit scraping failed: {e}")

try:
    hn_posts = fetch_hn_stories()
    all_posts.extend(hn_posts)
except Exception as e:
    print(f"❌ HN scraping failed: {e}")

try:
    google_posts = fetch_google_posts(recent_only=True)
    print(f"✅ Google posts: {len(google_posts)}")
    all_posts.extend(google_posts)
except Exception as e:
    print(f"❌ Google scraping failed: {e}")

# Save raw posts
print(f"\n✅ Saved {len(all_posts)} posts to {RAW_POSTS_PATH}")
with open(RAW_POSTS_PATH, "w") as f:
    json.dump(all_posts, f, indent=2)
