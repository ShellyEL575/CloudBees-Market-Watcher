import json
import os
from datetime import datetime
from summarizer import generate_summary, extract_insights_from_social
from utils import group_posts_by_topic, write_report
from exec_summary import generate_exec_summary

def extract_curated_source_list(posts):
    """
    Builds a clean list of unique (title, url) for exec summary.
    Avoids duplicates. Avoids HN comment URLs.
    """
    seen = set()
    curated = []

    for p in posts:
        title = p.get("title", "Untitled")
        url = p.get("url") or p.get("link")
        if not url:
            continue

        key = (title, url)
        if key not in seen:
            curated.append(key)
            seen.add(key)

    return curated


def main():
    print("✍️ Starting summarization...")

    with open("data/posts.json") as f:
        posts = json.load(f)

    print(f"✅ Loaded {len(posts)} posts")

    print("📊 Grouping...")
    grouped = group_posts_by_topic(posts)

    print("🧠 Extracting insights...")
    insights = extract_insights_from_social(grouped.get("💬 Social Buzz", []))

    print("📄 Building report sections...")
    sections = {
        "🚀 Product Updates": generate_summary(grouped["🚀 Product Updates"]),
        "💬 Social Buzz": generate_summary(grouped["💬 Social Buzz"]),
        "📈 Trends": generate_summary(grouped["📈 Trends"]),
        "🧠 Insights": insights,
    }

    print("📝 Writing main report...")
    write_report(sections)

    print("🔍 Building curated source set...")
    curated_sources = extract_curated_source_list(posts)

    print("📘 Generating executive summary...")
    exec_md = generate_exec_summary(insights, curated_sources)

    os.makedirs("reports", exist_ok=True)
    exec_report_path = f"reports/exec_summary_{datetime.utcnow().strftime('%Y-%m-%d')}.md"
    with open(exec_report_path, "w", encoding="utf-8") as f:
        f.write(exec_md)

    print(f"✅ Exec summary written to {exec_report_path}")


if __name__ == "__main__":
    main()
