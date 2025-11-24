# summarize_only.py
import json
import os
from datetime import datetime, timedelta

from summarizer import generate_summary
from utils import write_report, group_posts_by_topic
from llm_helpers import extract_insights_batch_linked
from exec_summary import generate_exec_summary


# ---------------------------------------
# Load posts
# ---------------------------------------
def load_posts():
    path = "data/posts.json"
    if not os.path.exists(path):
        raise FileNotFoundError("❌ data/posts.json not found. Run scrape_only.py first.")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------
# Weekly rollup helper (simple summary aggregation)
# ---------------------------------------
def load_weekly_posts():
    weekly_posts = []
    now = datetime.utcnow()

    for fname in os.listdir("data"):
        if not fname.endswith(".json"):
            continue
        fpath = os.path.join("data", fname)

        try:
            date_str = fname.replace(".json", "")
            file_date = datetime.strptime(date_str, "%Y-%m-%d")
        except Exception:
            continue

        if now - file_date <= timedelta(days=7):
            with open(fpath, "r", encoding="utf-8") as f:
                weekly_posts.extend(json.load(f))

    return weekly_posts


# ---------------------------------------
# Curated source list helper
# ---------------------------------------
def extract_curated_sources(posts):
    curated = []
    for p in posts:
        if isinstance(p, dict):
            url = p.get("url") or p.get("link")
            title = p.get("title", "Untitled")
            if url:
                curated.append((title, url))
    return curated


# ---------------------------------------
# Main summarization
# ---------------------------------------
def main():
    print("\n🧠 Starting summarization...")

    posts = load_posts()
    print(f"✅ Loaded {len(posts)} posts")

    print("📝 Generating report summaries...")

    grouped = group_posts_by_topic(posts)

    sections = {
        "🚀 Product Updates": generate_summary(grouped.get("🚀 Product Updates", [])),
        "💬 Social Buzz": generate_summary(grouped.get("💬 Social Buzz", [])),
        "📈 Trends": generate_summary(grouped.get("📈 Trends", [])),
    }

    # ---------------------------------------
    # Extract insights
    # ---------------------------------------
    print("🚀 Extracting insights...")

    social_posts = grouped.get("💬 Social Buzz", [])
    print(f"🧠 Extracting insights across {len(social_posts)} posts...")

    insight_block = extract_insights_batch_linked(social_posts)
    sections["🧠 Insights"] = insight_block

    # ---------------------------------------
    # Write daily report (full)
    # ---------------------------------------
    print("📝 Writing Daily Report...")
    report_path = write_report(sections)

    # ---------------------------------------
    # Exec Summary
    # ---------------------------------------
    print("🧠 Generating Executive Summary...")

    curated_sources = extract_curated_sources(posts)
    exec_md = generate_exec_summary(insight_block, curated_sources)

    exec_dir = "reports/exec"
    os.makedirs(exec_dir, exist_ok=True)

    exec_path = os.path.join(exec_dir, f"{datetime.utcnow().strftime('%Y-%m-%d')}.md")
    with open(exec_path, "w", encoding="utf-8") as f:
        f.write(exec_md)

    print(f"📄 Executive summary written: {exec_path}")

    # ---------------------------------------
    # Weekly Rollup Placeholder (optional)
    # ---------------------------------------
    # To activate weekly rollups later, call load_weekly_posts()
    # and generate weekly summaries similarly.

    print("\n🎉 Done! Summaries generated successfully.")


if __name__ == "__main__":
    main()
