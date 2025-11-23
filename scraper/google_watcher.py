# utils.py (patched)
import os
from datetime import datetime

def group_posts_by_topic(posts):
    """
    Group posts into Product Updates, Social Buzz, and Trends.
    Classification is based on the `type` value assigned by scrapers.
    """
    grouped = {
        "🚀 Product Updates": [],
        "💬 Social Buzz": [],
        "📈 Trends": []
    }

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
    Write a Markdown report with clean formatting.
    Sections auto-skip empty content.
    """
    os.makedirs("reports", exist_ok=True)
    report_date = datetime.utcnow().strftime("%Y-%m-%d")
    path = f"reports/{report_date}.md"

    with open(path, "w", encoding="utf-8") as f:
        f.write(f"# 📰 CloudBees Market Watch – {report_date}\n\n")

        order = ["🚀 Product Updates", "💬 Social Buzz", "📈 Trends", "🧠 Insights"]
        for section in order:
            content = sections.get(section, "").strip()
            if not content or content == "No updates found.":
                continue  # skip empty

            f.write(f"## {section}\n")
            f.write(content + "\n")
            f.write("\n---\n\n")

    print(f"✅ Report written to {path}")

    # Optional console preview
    print("\n===== 📝 Report Preview =====\n")
    with open(path, "r", encoding="utf-8") as f:
        print(f.read())

    return path
