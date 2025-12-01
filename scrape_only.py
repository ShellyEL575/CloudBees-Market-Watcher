# scrape_only.py — patched to debug post filtering
import json
import os
from datetime import datetime, timedelta

from scraper.competitor import fetch_competitor_updates
from scraper.hn import fetch_hn_stories
from google_watcher import fetch_google_results

# Optional: set cutoff to recent days only
DAYS_BACK = 7
cutoff_date = datetime.utcnow() - timedelta(days=DAYS_BACK)


def try_fetch(func, name):
    print(f"➡️  Fetching {name} (attempt 1)...")
    try:
        return func()
    except Exception as e:
        print(f"❌ Failed to fetch {name}: {e}")
        return []


def save_recent_posts(all_posts):
    print(f"\n📥 Raw post count before filtering: {len(all_posts)}")

    recent = []
    missing_date = 0
    too_old = 0

    for p in all_posts:
        ts = p.get("timestamp")
        if not ts:
            missing_date += 1
            continue
        try:
            dt = datetime.fromisoformat(ts)
        except Exception:
            continue
        if dt >= cutoff_date:
            recent.append(p)
        else:
            too_old += 1

    print(f"✅ Filtered recent posts: {len(recent)}")
    print(f"🕒 Skipped due to age: {too_old}")
    print(f"⚠️ Skipped due to missing timestamp: {missing_date}")

    os.makedirs("data", exist_ok=True)
    with open("data/posts.json", "w", encoding="utf-8") as f:
        json.dump(recent, f, indent=2, ensure_ascii=False)

    print("✅ Saved recent posts to data/posts.json")


def main():
    print("📥 Collecting posts...")
    all_posts = []

    all_posts.extend(try_fetch(fetch_hn_stories, "Hacker News"))
    all_posts.extend(try_fetch(fetch_competitor_updates, "Competitor Blogs"))
    all_posts.extend(try_fetch(fetch_google_results, "Google Search"))

    print(f"📌 Total posts collected: {len(all_posts)}")

    # Show sample timestamps
    print("\n🔍 Example post timestamps:")
    for p in all_posts[:5]:
        print(p.get("timestamp"))

    save_recent_posts(all_posts)


if __name__ == "__main__":
    main()
