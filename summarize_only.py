# summarize_only.py
import json
import os
from datetime import datetime

from summarizer import generate_summary
from utils import write_report
from llm_helpers import extract_insights_batch_linked
from exec_summary import generate_exec_summary


def load_posts():
    path = "data/posts.json"
    if not os.path.exists(path):
        raise FileNotFoundError("❌ data/posts.json not found. Run scrape_only.py first.")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def curate_sources(posts):
    """
    Deduplicate links + keep only valid URLs + preserve titles.
    Output: list of (title, url) tuples
    """
    seen = set()
    curated = []

    for p in posts:
        title = p.get("title") or "Untitled"
        url = p.get("url") or p.get("link")
        if not url or url in seen:
            continue

        curated.append((title, url))
        seen.add(url)

    return curated


def write_exec_summary(insights, curated_sources):
    """Write exec_summary.md alongside the main report."""

    md = generate_exec_summary(insights, curated_sources)
    path = "reports/exec_summary.md"
    with open(path, "w", encoding="utf-8") as f:
        f.write(md)

    print(f"✅ Exec Summary written to {path}")
    return path


def main():
    print("🧠 Starting summarization...")

    posts = load_posts()
    print(f"✅ Loaded {len(posts)} posts")

    # ---- Summaries for full market report ----
    print("📝 Generating report summaries...")
    sections = generate_summary(posts)

    # ---- Insights (LLM, evidence-linked) ----
    print("🚀 Extracting insights...")
    insights = extract_insights_batch_linked(posts)

    sections["🧠 Insights"] = insights

    # ---- Write main market report ----
    report_path = write_report(sections)

    # ---- Exec Summary with curated links ----
    curated_sources = curate_sources(posts)
    write_exec_summary(insights, curated_sources)

    print("\n🎉 All summaries generated successfully!")
    print(f"   - Main report: {report_path}")
    print("   - Exec summary: reports/exec_summary.md")


if __name__ == "__main__":
    main()
