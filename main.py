# main.py (optional legacy entrypoint – now split into two phases)
import os
import json
from datetime import datetime
from scraper.competitor import fetch_competitor_updates
from scraper.reddit import fetch_reddit_discussions
from scraper.hn import fetch_hn_stories
from scraper.google_watcher import fetch_google_results
from summarizer import generate_summary, extract_insights_from_social
from utils import group_posts_by_topic


def run_scraper():
    print("\n📥 Collecting posts...")
    all_posts = []

    try:
        competitor_posts = fetch_competitor_updates()
        print(f"✅ Competitor posts: {len(competitor_posts)}")
        all_posts.extend(competitor_posts)
    except Exception as e:
        print("❌ Competitor scraping failed:", e)

    try:
        reddit_posts = fetch_reddit_discussions()
        print(f"✅ Reddit posts: {len(reddit_posts)}")
        all_posts.extend(reddit_posts)
    except Exception as e:
        print("❌ Reddit scraping failed:", e)

    try:
        hn_posts = fetch_hn_stories()
        print(f"✅ HN posts: {len(hn_posts)}")
        all_posts.extend(hn_posts)
    except Exception as e:
        print("❌ HN scraping failed:", e)

    try:
        google_posts = fetch_google_results()
        print(f"✅ Google posts: {len(google_posts)}")
        all_posts.extend(google_posts)
    except Exception as e:
        print("❌ Google search failed:", e)

    os.makedirs("data", exist_ok=True)
    with open("data/raw_posts.json", "w") as f:
        json.dump(all_posts, f, indent=2)

    print(f"\n✅ Saved {len(all_posts)} posts to data/raw_posts.json")


def run_summarizer():
    print("\n🧠 Loading raw posts for summarization...")

    with open("data/raw_posts.json") as f:
        all_posts = json.load(f)

    print(f"✅ Loaded {len(all_posts)} posts")

    print("\n📊 Grouping posts...")
    grouped = group_posts_by_topic(all_posts)

    print("\n✍️ Generating summary...")
    summary = generate_summary(grouped)

    print("\n🔍 Extracting insights from social buzz...")
    social_insights = extract_insights_from_social(grouped.get("💬 Social Buzz", []))

    report_date = datetime.utcnow().strftime("%Y-%m-%d")
    os.makedirs("reports", exist_ok=True)
    report_path = f"reports/{report_date}.md"

    with open(report_path, "w") as f:
        f.write(f"# Market Watch Report – {report_date}\n\n")
        f.write(summary)
        f.write("\n\n===== 📊 Social Buzz Insights =====\n")
        f.write(social_insights)

    print(f"\n✅ Report saved to {report_path}")


if __name__ == "__main__":
    run_scraper()
    run_summarizer()
