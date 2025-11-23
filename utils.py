import os
from datetime import datetime


def ensure_dirs():
    os.makedirs("data", exist_ok=True)
    os.makedirs("reports", exist_ok=True)


def group_posts_by_topic(posts):
    grouped = {
        "🚀 Product Updates": [],
        "💬 Social Buzz": [],
        "📈 Trends": []
    }
    for post in posts:
        category = post.get("category", "💬 Social Buzz")
        grouped.setdefault(category, []).append(post)
    return grouped


def write_report(sections):
    ensure_dirs()
    today = datetime.today().strftime("%Y-%m-%d")
    filename = f"reports/{today}.md"

    summary_text = f"""## 🚀 Product Updates
{sections.get("🚀 Product Updates", "No product updates found.")}

## 💬 Social Buzz
{sections.get("💬 Social Buzz", "No social buzz found.")}

## 📈 Trends
{sections.get("📈 Trends", "No trends found.")}

## 🧠 Insights
{sections.get("🧠 Insights", "No insights found.")}
"""

    with open(filename, "w") as f:
        f.write(summary_text)

    print(f"\n===== 📰 Final Market Watch Report =====\n\n{summary_text}")
    print(f"✅ Report written to {filename}")
