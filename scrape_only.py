# scrape_only.py — patched to preserve more competitor posts and log filtering
import json
from datetime import datetime, timedelta
from scraper.hn import fetch_hn_stories
from scraper.google import fetch_google_results
from scraper.competitor import fetch_competitor_updates

def try_fetch(func, label):
    print(f"➡️  Fetching {label} (attempt 1)...")
    try:
        results = func()
        print(f"✅ {label} collected: {len(results)}")
        return results
    except Exception as e:
        print(f"❌ Error fetching {label}: {e}")
        return []

def save_recent_posts(posts, path="data/posts.json", limit_days=7):
    print("\n🔍 Filtering recent posts...")
    now = datetime.utcnow()
    cutoff = now - timedelta(days=limit_days)

    recent_posts = []
    dropped_by_source = {}

    for post in posts:
        ts = post.get("timestamp")
        source = post.get("source", "Unknown")
        try:
            if ts:
                dt = datetime.fromisoformat(ts)
                if dt >= cutoff:
                    recent_posts.append(post)
                else:
                    dropped_by_source[source] = dropped_by_source.get(source, 0) + 1
            else:
                # If no timestamp, still keep the post (better than silently skipping)
                recent_posts.append(post)
        except Exception as e:
            print(f"⚠️ Timestamp parse error for {post.get('title')}: {e}")
            recent_posts.append(post)

    print(f"✅ Saved {len(recent_posts)} recent posts to {path}")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(recent_posts, f, indent=2)

    if dropped_by_source:
        print("\n🚫 Dropped posts due to timestamp cutoff:")
        for src, count in dropped_by_source.items():
            print(f"   - {src}: {count} posts older than {limit_days} days")

    return recent_posts

def main():
    print("📥 Collecting posts...\n")
    all_posts = []

    all_posts.extend(try_fetch(fetch_hn_stories, "Hacker News"))
    all_posts.extend(try_fetch(fetch_competitor_updates, "Competitor Blogs"))
    all_posts.extend(try_fetch(fetch_google_results, "Google Search"))

    print(f"\n📌 Total posts collected: {len(all_posts)}")

    # Assign timestamps to all posts if missing
    now_str = datetime.utcnow().isoformat()
    for post in all_posts:
        if "timestamp" not in post:
            post["timestamp"] = now_str

    save_recent_posts(all_posts)

if __name__ == "__main__":
    main()
