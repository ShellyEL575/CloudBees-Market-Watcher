# summarize_only.py (FINAL)
import json
import os
from datetime import datetime

from utils import group_posts_by_topic, write_report
from llm_helpers import extract_insights_batch_linked
from exec_summary import generate_exec_summary


def load_posts():
    path = "data/posts.json"
    if not os.path.exists(path):
        raise FileNotFoundError("❌ data/posts.json not found. Did scrape_only.py run?")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_curated_source_deck(posts):
    """
    Dedup and produce a list of (title, url) tuples.
    This becomes the PMM/PM 'Source Deck' in exec summary.
    """
    seen = set()
    curated = []
    for p in posts:
        title = p.get("title", "").strip()
        url = p.get("url") or p.get("link") or ""
        if not title or not url:
            continue
        if url in seen:
            continue
        curated.append((title, url))
        seen.add(url)
    return curated


def main():
    print("🧠 Starting summarization...")

    posts = load_posts()
    print(f"✅ Loaded {len(posts)} posts")

    # --- GROUPING ---
    sections = {}
    grouped = group_posts_by_topic(posts)
    print("📝 Generating report summaries...")

    # Generate the 3 sections (these rely on scrapers to provide summaries)
    for section_name in ["🚀 Product Updates", "💬 Social Buzz", "📈 Trends"]:
        items = grouped.get(section_name, [])
        if not items:
            sections[section_name] = "_No updates today._"
        else:
            md_lines = []
            for p in items:
                title = p.get("title", "Untitled")
                url = p.get("url") or p.get("link") or ""
                summary = p.get("summary", "") or "(no summary available)"
                md_lines.append(f"- [{title}]({url}) — {summary}")
            sections[section_name] = "\n".join(md_lines)

    # --- INSIGHTS ---
    print("🚀 Extracting insights...")
    social_posts = grouped.get("💬 Social Buzz", [])

    print(f"🧠 Extracting insights across {len(social_posts)} posts...")
    insights = extract_insights_batch_linked(social_posts)
    sections["🧠 Insights"] = insights

    # --- WRITE MAIN REPORT ---
    write_report(sections)

    # --- EXECUTIVE SUMMARY ---
    print("📊 Creating executive summary artifact...")

    curated_sources = build_curated_source_deck(posts)
    exec_md = generate_exec_summary(insights, curated_sources)

    os.makedirs("reports", exist_ok=True)
    exec_path = f"reports/exec_summary_{datetime.utcnow().strftime('%Y-%m-%d')}.md"

    with open(exec_path, "w", encoding="utf-8") as f:
        f.write(exec_md)

    print(f"✅ Executive summary written to {exec_path}")


if __name__ == "__main__":
    main()
