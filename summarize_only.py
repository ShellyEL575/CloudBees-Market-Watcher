# summarize_only.py
import json
import os
from datetime import datetime
from summarizer import generate_summary, extract_insights_from_social
from utils import group_posts_by_topic

print("\n🧠 Loading raw posts for summarization...")

with open("data/raw_posts.json") as f:
    all_posts = json.load(f)

print(f"✅ Loaded {len(all_posts)} posts")

print("\n📊 Grouping posts...")
grouped = group_posts_by_topic(all_posts)

print("\n✍️ Generating summary...")
summary = generate_summary(grouped)

print("\n🔍 Extracting insights from social buzz...")
social_insights = extract_insights_from_social(grouped.get("💬 Social Buzz", []))

report_date = datetime.utcnow().strftime("%Y-%m-%d")
os.makedirs("reports", exist_ok=True)
report_path = f"reports/{report_date}.md"

with open(report_path, "w") as f:
    f.write(f"# Market Watch Report – {report_date}\n\n")
    f.write(summary)
    f.write("\n\n===== 📊 Social Buzz Insights =====\n")
    f.write(social_insights)

print(f"\n✅ Report saved to {report_path}")
