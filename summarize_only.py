# summarize_only.py
import json
import os
from datetime import datetime
from utils import group_posts_by_topic, write_report
from llm_helpers import summarize_posts, extract_insights, link_insights_to_sources

print("✍️ Starting summarization...")

with open("data/posts.json", "r") as f:
    posts = json.load(f)

print(f"✅ Loaded {len(posts)} posts")

# --- Grouping ---
grouped = group_posts_by_topic(posts)

# --- Summaries ---
product_md = summarize_posts(grouped["🚀 Product Updates"])
buzz_md = summarize_posts(grouped["💬 Social Buzz"])
trends_md = summarize_posts(grouped["📈 Trends"])

# --- Insights ---
print("🧠 Extracting insights...")
raw_insights = extract_insights(grouped["💬 Social Buzz"])

print("🔗 Linking insights to supporting sources...")
linked_insights = link_insights_to_sources(raw_insights, grouped["💬 Social Buzz"])

# --- Write final report ---
sections = {
    "🚀 Product Updates": product_md,
    "💬 Social Buzz": buzz_md,
    "📈 Trends": trends_md,
    "🧠 Insights": linked_insights,
}

path = write_report(sections)
