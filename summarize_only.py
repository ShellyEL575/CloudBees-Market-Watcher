# summarize_only.py

from utils import group_posts_by_type, write_report
from summarizer import generate_summary, extract_insights_from_social
from scraper.trend_classifier import extract_trends
import json
import os

print("✍️ Generating summary...")

# Load previously collected posts
with open("data/posts.json", "r") as f:
    posts = json.load(f)

grouped = group_posts_by_type(posts)

# Generate summaries with links in markdown format
summary_sections = {
    "🚀 Product Updates": generate_summary(grouped.get("🚀 Product Updates", [])),
    "💬 Social Buzz": generate_summary(grouped.get("💬 Social Buzz", [])),
    "📈 Trends": generate_summary(grouped.get("📈 Trends", [])),
}

# Collect useful links for debug output
print("📌 Collected Links:")
for post in posts:
    link = post.get("link") or post.get("url")
    if link:
        print(f"- {post['title']}: {link}")

# Extract trends and insights
summary_sections["📈 Trends"] = generate_summary(extract_trends(posts))
summary_sections["🧠 Insights"] = extract_insights_from_social(posts)

# Write final report
report_path = write_report(summary_sections)
if report_path:
    print(f"✅ Report written to {report_path}")
else:
    print("⚠️ Report path not returned.")

print("\n===== 📰 Final Market Watch Report =====\n")
for section, content in summary_sections.items():
    print(f"## {section}\n{content}\n")

print("✅ Summary report generated!")
