# main.py — Patched Unified Runner (Optional Convenience Entrypoint)

import os
import json
from datetime import datetime

from scraper.hn import fetch_hn_stories
from scraper.competitor import fetch_competitor_updates
from scraper.google_watcher import fetch_google_results
from scraper.trend_classifier import classify_trends

from summarizer import generate_summary, extract_insights_from_social
from utils import group_posts_by_topic


# -------------------------
# SCRAPER PHASE
# -------------------------
def run_scraper():
    print("\n📥 Collecting posts...\n")
    all_posts = []

    # Hacker News
    try:
        hn_posts = fetch_hn_stories()
        print(f"✅ HN posts: {len(hn_posts)}")
        all_posts.extend(hn_posts)
    except Exception as e:
        print(f"❌ Hacker News scraping failed: {e}")

    # Competitor Blogs
    try:
        competitor_posts = fetch_competitor_updates()
        print(f"✅ Competitor posts: {len(competitor_posts)}")
        all_posts.extend(competitor_posts)
    except Exception as e:
        print(f"❌ Competitor scraping failed: {e}")

    # Google Search (Serper.dev)
    try:
        google_posts = fetch_google_results()
        print(f"✅ Google posts: {len(google_posts)}")
        all_posts.extend(google_posts)
    except Exception as e:
        print(f"❌ Google search failed: {e}")

    print(f"\n📌 Total collected: {len(all_posts)}")

    # Trend classification
    for post in all_posts:
        matches = classify_trends([post])
        post["is_trend"] = len(matches) > 0

    os.makedirs("data", exist_ok=True)
    with open("data/posts.json", "w", encoding="utf-8") as f:
        json.dump(all_posts, f, indent=2)

    print("✅ Saved posts to data/posts.json\n")


# -------------------------
# SUMMARIZATION PHASE
# -------------------------
def run_summarizer():
    print("🧠 Loading posts...\n")

    with open("data/posts.json", "r", encoding="utf-8") as f:
        posts = json.load(f)

    print(f"✅ Loaded {len(posts)} posts\n")

    print("📊 Grouping posts...")
    grouped = group_posts_by_topic(posts)

    print("✍️ Generating summaries...\n")
    summary_sections = {
        "🚀 Product Updates": generate_summary(grouped.get("🚀 Product Updates", [])),
        "💬 Social Buzz": generate_summary(grouped.get("💬 Social Buzz", [])),
        "📈 Trends": generate_summary(grouped.get("📈 Trends", [])),
    }

    print("🔍 Extracting insights...\n")
    summary_sections["🧠 Insights"] = extract_insights_from_social(posts)

    # Output result
    report_date = datetime.utcnow().strftime("%Y-%m-%d")
    os.makedirs("reports", exist_ok=True)
    report_path = f"reports/{report_date}.md"

    with open(report_path, "w", encoding="utf-8") as f:
        f.write(f"# 📰 CloudBees Market Watch – {report_date}\n\n")

        for section, content in summary_sections.items():
            if content.strip():
                f.write(f"## {section}\n{content}\n\n---\n\n")

    print(f"✅ Report saved to {report_path}\n")


# -------------------------
# COMBINED RUNNER
# -------------------------
if __name__ == "__main__":
    run_scraper()
    run_summarizer()
