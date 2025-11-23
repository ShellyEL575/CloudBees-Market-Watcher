import os
import json
from datetime import datetime
from summarizer import generate_summary, extract_insights_from_social
from utils import group_posts_by_topic, write_report

# Load scraped posts
with open("data/raw_posts.json", "r") as f:
    posts = json.load(f)

print("✍️ Generating summary...")

# Filter out Reddit posts if they are malformed or None
posts = [p for p in posts if p and isinstance(p, dict) and p.get("source") != "Reddit"]

# Print all links collected
print("📌 Collected Links:")
for p in posts:
    print(f"- {p.get('title', '[No title]')}: {p.get('link', '[No link]')}")

# Group posts by topic
grouped = group_posts_by_topic(posts)

# Print post counts for each category
for category in grouped:
    print(f"{category}: {len(grouped[category])} posts")

# Generate summaries
summary_sections = {
    "🚀 Product Updates": generate_summary(grouped.get("🚀 Product Updates", [])),
    "💬 Social Buzz": generate_summary(grouped.get("💬 Social Buzz", [])),
    "📈 Trends": generate_summary(grouped.get("📈 Trends", [])),
    "🧠 Insights": extract_insights_from_social(grouped.get("💬 Social Buzz", []))
}

# Write markdown report and print it
report_path = write_report(summary_sections)
if report_path:
    with open(report_path, "r") as f:
        print("\n===== 📰 Final Market Watch Report =====\n")
        print(f.read())

print("✅ Summary report generated!")
