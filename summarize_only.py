import os
import json
from datetime import datetime
from summarizer import generate_summary, extract_insights_from_social
from utils import group_posts_by_topic, write_report

# Load scraped posts
with open("data/raw_posts.json", "r") as f:
    posts = json.load(f)

print("✍️ Generating summary...")

# Group posts by topic
grouped = group_posts_by_topic(posts)

# Debug print grouped count
for category, items in grouped.items():
    print(f"{category}: {len(items)} posts")

# Fallback: if Product Updates is empty, include all posts
if not grouped.get("🚀 Product Updates"):
    grouped["🚀 Product Updates"] = posts

# Generate summaries for each category
summary_sections = {
    "🚀 Product Updates": generate_summary(grouped.get("🚀 Product Updates", [])),
    "💬 Social Buzz": generate_summary(grouped.get("💬 Social Buzz", [])),
    "📈 Trends": generate_summary(grouped.get("📈 Trends", [])),
    "🧠 Insights": extract_insights_from_social(grouped.get("💬 Social Buzz", []))
}

# Write markdown report and print it
report_path = write_report(summary_sections)

print("\n===== 📰 Final Market Watch Report =====\n")
with open(report_path, "r") as f:
    print(f.read())

print("✅ Summary report generated!")
