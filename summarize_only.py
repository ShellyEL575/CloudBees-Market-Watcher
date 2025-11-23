from utils import group_posts_by_topic, write_report
from summarizer import generate_summary, extract_insights_from_social
from scraper.trend_classifier import classify_trends
import json
import os


print("✍️ Generating summary...")


# Load scraped posts
with open("data/posts.json", "r", encoding="utf-8") as f:
posts = json.load(f)


# Re-classify trends (defensive)
for post in posts:
matches = classify_trends([post])
post["is_trend"] = len(matches) > 0


# Group posts
grouped = group_posts_by_topic(posts)


summary_sections = {
"🚀 Product Updates": generate_summary(grouped.get("🚀 Product Updates", [])),
"💬 Social Buzz": generate_summary(grouped.get("💬 Social Buzz", [])),
"📈 Trends": generate_summary(grouped.get("📈 Trends", [])),
}


# Insights section
summary_sections["🧠 Insights"] = extract_insights_from_social(posts)


# Write report
report_path = write_report(summary_sections)
print(f"✅ Report written to {report_path}")
