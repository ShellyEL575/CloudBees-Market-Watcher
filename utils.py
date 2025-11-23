import os
import re
import json
from datetime import datetime
from collections import defaultdict


def group_posts_by_topic(posts):
    topics = defaultdict(list)

    for post in posts:
        title = post.get("title", "").lower()
        content = f"{title} {post.get('content', '').lower()}"

        if any(keyword in content for keyword in ["cloudbees", "jenkins", "ci/cd", "pipeline"]):
            topics["CloudBees & CI/CD"].append(post)
        elif any(keyword in content for keyword in ["copilot", "ai", "openai"]):
            topics["AI & Dev Experience"].append(post)
        elif any(keyword in content for keyword in ["gitlab", "github", "bitbucket", "azure devops"]):
            topics["Competitor Updates"].append(post)
        elif any(keyword in content for keyword in ["devops metrics", "dora", "space metrics", "flow"]):
            topics["Metrics & Analytics"].append(post)
        else:
            topics["General"].append(post)

    return topics


def write_report(summary_text):
    date_str = datetime.now().strftime("%Y-%m-%d")
    os.makedirs("reports", exist_ok=True)
    report_path = f"reports/{date_str}.md"

    with open(report_path, "w") as f:
        f.write(summary_text)

    print(f"✅ Report saved to {report_path}")
