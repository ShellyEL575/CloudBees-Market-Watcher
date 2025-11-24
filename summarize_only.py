# summarize_only.py — Final Batch Evidence Linking Version
import json

from summarizer import (
    generate_summary,
    extract_insights_from_social,
    batch_link_sources,
    format_insights_with_sources
)

from utils import (
    group_posts_by_topic,
    write_report,
    write_sources_file
)

from scraper.trend_classifier import classify_trends

print("✍️ Starting summarization...\n")

# ---------------------------------------------------------
# Load scraped posts
# ---------------------------------------------------------
with open("data/posts.json", "r", encoding="utf-8") as f:
    posts = json.load(f)

print(f"✅ Loaded {len(posts)} posts\n")

# ---------------------------------------------------------
# Defensive trend classification
# ---------------------------------------------------------
for post in posts:
    matches = classify_trends([post])
    post["is_trend"] = len(matches) > 0

# ---------------------------------------------------------
# Group by topic for summaries
# ---------------------------------------------------------
grouped = group_posts_by_topic(posts)

summary_sections = {
    "🚀 Product Updates": generate_summary(grouped.get("🚀 Product Updates", [])),
    "💬 Social Buzz": generate_summary(grouped.get("💬 Social Buzz", [])),
    "📈 Trends": generate_summary(grouped.get("📈 Trends", [])),
}

# ---------------------------------------------------------
# Structured insights (JSON)
# ---------------------------------------------------------
print("🧠 Extracting insights...\n")
insights = extract_insights_from_social(posts)

# ---------------------------------------------------------
# Batch evidence linking (4 GPT calls only)
# ---------------------------------------------------------
print("🔗 Linking insights to supporting sources...\n")
linked_sources = batch_link_sources(insights, posts)

# ---------------------------------------------------------
# Format insights + evidence → Markdown
# ---------------------------------------------------------
insights_markdown = format_insights_with_sources(insights, linked_sources)
summary_sections["🧠 Insights"] = insights_markdown

# ---------------------------------------------------------
# Write main report
# ---------------------------------------------------------
report_path = write_report(summary_sections)

# ---------------------------------------------------------
# Write sources artifact
# ---------------------------------------------------------
sources_path = write_sources_file(posts)

print(f"📄 Summary report written to: {report_path}")
print(f"📚 Evidence sources written to: {sources_path}")
print("\n✨ Summarization complete.\n")
