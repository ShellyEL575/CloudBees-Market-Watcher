# summarize_only.py — Final Patched Version
import json

from summarizer import generate_summary, extract_insights_from_social
from utils import group_posts_by_topic, write_report, write_sources_file
from scraper.trend_classifier import classify_trends

print("✍️ Generating summary...\n")

# --------------------------
# Load scraped posts
# --------------------------
with open("data/posts.json", "r", encoding="utf-8") as f:
    posts = json.load(f)

print(f"✅ Loaded {len(posts)} posts\n")

# --------------------------
# Defensive trend classification
# --------------------------
for post in posts:
    matches = classify_trends([post])
    post["is_trend"] = len(matches) > 0

# --------------------------
# Group posts by topic
# --------------------------
grouped = group_posts_by_topic(posts)

# --------------------------
# Build summary sections
# --------------------------
summary_sections = {
    "🚀 Product Updates": generate_summary(grouped.get("🚀 Product Updates", [])),
    "💬 Social Buzz": generate_summary(grouped.get("💬 Social Buzz", [])),
    "📈 Trends": generate_summary(grouped.get("📈 Trends", [])),
}

# --------------------------
# Insights section
# --------------------------
summary_sections["🧠 Insights"] = extract_insights_from_social(posts)

# --------------------------
# Write main report
# --------------------------
report_path = write_report(summary_sections)

# --------------------------
# Write evidence sources artifact
# --------------------------
sources_path = write_sources_file(posts)

print(f"📄 Summary report written to: {report_path}")
print(f"📚 Sources artifact written to: {sources_path}")
