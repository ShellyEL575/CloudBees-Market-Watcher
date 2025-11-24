# summarize_only.py
import json
from datetime import datetime
from utils import write_report, group_posts_by_topic
from summarizer import generate_summary  # unchanged
from llm_helpers import extract_insights_batch_linked
from exec_summary import generate_exec_summary

def main():
    print("🧠 Starting summarization...")

    # ---------------------------------------------------
    # 1. Load scraped posts
    # ---------------------------------------------------
    with open("data/posts.json", "r", encoding="utf-8") as f:
        posts = json.load(f)

    print(f"✅ Loaded {len(posts)} posts")
    grouped = group_posts_by_topic(posts)

    print("📝 Generating report summaries...")

    # ---------------------------------------------------
    # 2. Build all report sections as a dict
    # ---------------------------------------------------
    sections = {
        "🚀 Product Updates": generate_summary(grouped["🚀 Product Updates"]),
        "💬 Social Buzz": generate_summary(grouped["💬 Social Buzz"]),
        "📈 Trends": generate_summary(grouped["📈 Trends"]),
    }

    # ---------------------------------------------------
    # 3. Extract Insights with LLM + linked sources
    # ---------------------------------------------------
    print("🚀 Extracting insights...")

    social_posts = grouped["💬 Social Buzz"]
    insight_block = extract_insights_batch_linked(social_posts)
    sections["🧠 Insights"] = insight_block  # <-- NOW VALID

    # ---------------------------------------------------
    # 4. Create the Exec Summary artifact
    # ---------------------------------------------------
    curated_sources = [
        (p.get("title", "Untitled"), p.get("url") or p.get("link") or "")
        for p in posts
        if p.get("url") or p.get("link")
    ]

    exec_md = generate_exec_summary(insight_block, curated_sources)

    date = datetime.utcnow().strftime("%Y-%m-%d")
    exec_path = f"reports/exec_summary_{date}.md"
    with open(exec_path, "w", encoding="utf-8") as ef:
        ef.write(exec_md)

    print(f"📄 Exec Summary written to {exec_path}")

    # ---------------------------------------------------
    # 5. Write the main daily report
    # ---------------------------------------------------
    report_path = write_report(sections)
    print(f"🎉 Done. Report at: {report_path}")

if __name__ == "__main__":
    main()
