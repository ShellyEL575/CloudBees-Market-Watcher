# utils.py
import os
from datetime import datetime


def group_posts_by_topic(posts):
    """
    Group posts into Product Updates, Social Buzz, Trends.
    """
    grouped = {"🚀 Product Updates": [], "💬 Social Buzz": [], "📈 Trends": []}

    for p in posts:
        t = p.get("type")
        if t == "🚀 Product Updates":
            grouped["🚀 Product Updates"].append(p)
        elif t == "📈 Trends":
            grouped["📈 Trends"].append(p)
        else:
            grouped["💬 Social Buzz"].append(p)

    return grouped



def write_report(sections):
    """
    Write a Markdown report containing:
    - product updates
    - social buzz
    - trends
    - insights
    """
    os.makedirs("reports", exist_ok=True)

    report_date = datetime.utcnow().strftime("%Y-%m-%d")
    path = f"reports/{report_date}.md"

    with open(path, "w", encoding="utf-8") as f:
        f.write(f"# 📰 CloudBees Market Watch – {report_date}\n\n")

        # Ordered sections
        order = ["🚀 Product Updates", "💬 Social Buzz", "📈 Trends", "🧠 Insights"]
        for section in order:
            f.write(f"## {section}\n")
            f.write(sections.get(section, "_No content available._"))
            f.write("\n\n")

    print(f"✅ Report written to {path}")

    # Optional: print a preview in logs
    print("\n===== 📝 Report Preview =====\n")
    with open(path, "r") as f:
        print(f.read())

    return path
