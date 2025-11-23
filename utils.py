import os
import json
from datetime import datetime
from collections import defaultdict
import re

def save_posts(posts, filename="data/raw_posts.json"):
    if not os.path.exists("data"):
        os.makedirs("data")
    with open(filename, "w") as f:
        json.dump(posts, f, indent=2)
    print(f"✅ Saved {len(posts)} posts to {filename}")

def load_posts(filename="data/raw_posts.json"):
    with open(filename, "r") as f:
        return json.load(f)

def group_posts_by_topic(posts):
    topics = defaultdict(list)
    keywords = {
        "Product Updates": ["release", "update", "feature", "launch"],
        "Social Buzz": ["reddit", "linkedin", "medium", "youtube"],
        "Trends": ["trend", "analysis", "report", "insight", "metrics"],
    }

    for post in posts:
        title = post.get("title", "").lower()
        matched = False
        for topic, kws in keywords.items():
            if any(re.search(rf"\b{k}\b", title) for k in kws):
                topics[topic].append(post)
                matched = True
                break
        if not matched:
            topics["Misc"].append(post)

    return topics

def write_report(summary_sections):
    if not os.path.exists("reports"):
        os.makedirs("reports")

    date_str = datetime.utcnow().strftime("%Y-%m-%d")
    report_path = f"reports/{date_str}.md"

    summary_text = ""
    for section, content in summary_sections.items():
        summary_text += f"## {section}\n{content}\n\n"

    with open(report_path, "w") as f:
        f.write(summary_text)

    print(f"✅ Report written to {report_path}")
