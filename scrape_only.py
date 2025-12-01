# scrape_only.py — fully patched version

import json
import os
from datetime import datetime

from scraper.hn import fetch_hn_stories
from scraper.competitor import fetch_competitor_updates
from scraper.google_watcher import fetch_google_results  # ✅ Corrected import

def try_fetch(fetch_func, label):
    print(f"\n➡️  Fetching {label} (attempt 1)...")
    try:
        return fetch_func()
    except Exception as e:
        print(f"❌ Error while fetching {label}: {e}")
        return []

def save_posts(posts):
    os.makedirs("data", exist_ok=True)

    # Keep only the most recent 250 posts
    posts = sorted(posts, key=lambda x: x.get("timestamp", ""), reverse=True)[:250]

    with open("data/posts.json", "w", encoding="utf-8") as f:
        json.dump(posts, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Saved {len(posts)} recent posts to data/posts.json")

    print("\n🔍 Example post timestamps:")
    for p in posts[:5]:
        print(p.get("timestamp"))

def main():
    print("📥 Collecting posts...\n")

    all_posts = []
    all_posts.extend(try_fetch(fetch_hn_stories, "Hacker News"))
    all_posts.extend(try_fetch(fetch_competitor_updates, "Competitor Blogs"))
    all_posts.extend(try_fetch(fetch_google_results, "Google Search"))

    print(f"\n📌 Total posts collected: {len(all_posts)}")

    save_posts(all_posts)

if __name__ == "__main__":
    main()
