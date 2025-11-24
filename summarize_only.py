# summarize_only.py — Final Version with LLM Evidence Linking
import json

from summarizer import (
    generate_summary,
    extract_insights_from_social,
    link_sources_to_insights,
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
# Group posts by topic
# ---------------------------------------------------------
grouped = group_posts_by_topic(posts)

# ---------------------------------------------------------
# Build topic summaries
# ---------------------------------------------------------
summary_sections = {
    "🚀 Product Updates": generate_summary(grouped.get("🚀 Product Updates", [])),
    "💬 Social Buzz": generate_summary(grouped.get("💬 Social Buzz", [])),
    "📈 Trends": generate_summary(grouped.get("📈 Trends", [])),
}

# ---------------------------------------------------------
# Extract structured insights (JSON with 4 sections)
# ---------------------------------------------------------
print("🧠 Extracting insights...\n")
insights = extract_insights_from_social(posts)

# insights is:
# {
#   "Key Trends": [...],
#   "Pain Points": [...],
#   "Opportunities for CloudBees": [...],
#   "Indicators of DevOps Market Sentiment": [...]
# }

# ---------------------------------------------------------
# Evidence linking per insight
# ---------------------------------------------------------
print("🔗 Linking insights to supporting sources...\n")

linked = {}
for category, insight_list in insights.items():
    linked_sources = link_sources_to_insights(insight_list, posts)
    linked[category] = linked_sources

# ---------------------------------------------------------
# Convert insights + evidence → Markdown
# ---------------------------------------------------------
insights_md = []

for category, insight_list in insights.items():
    insights_md.append(f"### {category}")
    if not insight_list:
        insights_md.append("_No insights found._\n")
        continue

    for insight in insight_list:
        insights_md.append(f"- **{insight}**")

        supporting = linked[category].get(insight, [])
        if supporting:
            for s in supporting:
                insights_md.append(f"  - [{s['title']}]({s['url']})")
        else:
            insights_md.append("  - _No supporting sources detected_")

    insights_md.append("")

summary_sections["🧠 Insights"] = "\n".join(insights_md)

# ---------------------------------------------------------
# Write the main report
# ---------------------------------------------------------
report_path = write_report(summary_sections)

# ---------------------------------------------------------
# Write the evidence sources artifact (full list of URLs)
# ---------------------------------------------------------
sources_path = write_sources_file(posts)

# ---------------------------------------------------------
# Final console messages
# ---------------------------------------------------------
print(f"📄 Summary report written to: {report_path}")
print(f"📚 Evidence sources written to: {sources_path}")
print("\n✨ Summarization complete.\n")
