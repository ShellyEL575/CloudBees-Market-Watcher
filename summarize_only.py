import os
import json
from datetime import datetime
from summarizer import generate_summary, extract_insights_from_social
from utils import group_posts_by_topic, write_report

# Load scraped posts
with open("data/raw_posts.json", "r") as f:
    posts = json.load(f)

# Normalize keys: ensure every post has 'link' and 'category'
for post in posts:
    if "link" not in post and "url" in post:
        post["link"] = post["url"]
    if "category" not in post and "type" in post:
        post["category"] = post["type"]

print("✍️ Generating summary...")

# Group posts by category
grouped = group_posts_by_topic(posts)

# Debug: print how many posts in each category
print(f"🚀 Product Updates: {len(grouped.get('🚀 Product Updates', []))} posts")
print(f"💬 Social Buzz: {len(grouped.get('💬 Social Buzz', []))} posts")
print(f"📈 Trends: {len(grouped.get('📈 Trends', []))} posts")

# Collect and print all post links (for debug)
print("📌 Collected Links:")
for post in posts:
    title = post.get("title", "No title")
    link = post.get("link", "[No link]")
    print(f"- {title}: {link}")

# Generate summaries
summary_sections = {
    "🚀 Product Updates": generate_summary(grouped.get("🚀 Product Updates", [])),
    "💬 Social Buzz": generate_summary(grouped.get("💬 Social Buzz", [])),
    "📈 Trends": generate_summary(grouped.get("📈 Trends", [])),
    "🧠 Insights": extract_insights_from_social(grouped.get("💬 Social Buzz", []))
}

# Write markdown report
report_path = write_report(summary_sections)

# Print the report path and content
if report_path:
    print(f"✅ Report written to {report_path}\n")
    with open(report_path, "r") as f:
        print("===== 📰 Final Market Watch Report =====\n")
        print(f.read())
else:
    print("⚠️ Report path not returned.")

print("✅ Summary report generated!")
