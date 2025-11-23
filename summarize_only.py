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

# Generate summaries for each category
summary_sections = {
    "🚀 Product Updates": generate_summary(grouped.get("🚀 Product Updates", [])),
    "💬 Social Buzz": generate_summary(grouped.get("💬 Social Buzz", [])),
    "📈 Trends": generate_summary(grouped.get("📈 Trends", [])),
    "🧠 Insights": extract_insights_from_social(grouped.get("💬 Social Buzz", []))
}

# Write markdown report
write_report(summary_sections)

print("✅ Summary report generated!")
