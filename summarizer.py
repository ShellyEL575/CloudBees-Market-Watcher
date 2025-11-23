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

# Log number of posts per section
print(f"🚀 Product Updates: {len(grouped.get('🚀 Product Updates', []))} posts")
print(f"💬 Social Buzz: {len(grouped.get('💬 Social Buzz', []))} posts")
print(f"📈 Trends: {len(grouped.get('📈 Trends', []))} posts")

# Generate summaries for each category
summary_sections = {
    "🚀 Product Updates": generate_summary(grouped.get("🚀 Product Updates", [])),
    "💬 Social Buzz": generate_summary(grouped.get("💬 Social Buzz", [])),
    "📈 Trends": generate_summary(grouped.get("📈 Trends", [])),
    "🧠 Insights": extract_insights_from_social(grouped.get("💬 Social Buzz", []))
}

# Write markdown report and get path
report_path = write_report(summary_sections)

print(f"\n✅ Report written to {report_path}")
print("\n===== 📰 Final Market Watch Report =====\n")

# Print contents of report
if report_path:
    with open(report_path, "r") as f:
        print(f.read())

print("✅ Summary report generated!")
