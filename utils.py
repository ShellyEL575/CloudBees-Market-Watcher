# utils.py — final patched version
import os
from datetime import datetime


def group_posts_by_topic(posts):
    """
    Group posts into Product Updates, Social Buzz, and Trends.
    Classification is based on the `type` assigned by scrapers.
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
    Write a Markdown **summary report** with clean formatting.
    Sections with no content are skipped.
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
                continue  # Skip empty

            f.write(f"## {section}\n")
            f.write(content + "\n\n---\n\n")

    print(f"✅ Report written to {path}")

    # Optional console preview
    print("\n===== 📝 Report Preview =====\n")
    with open(path, "r", encoding="utf-8") as f:
        print(f.read())

    return path


# ---------------------------------------------------------------------
# NEW FUNCTION — generates the “evidence sources” artifact
# ---------------------------------------------------------------------
def write_sources_file(posts):
    """
    Create a clean, GPT-friendly list of all URLs grouped by topic.
    NO HTML. NO SUMMARIES.
    Pure evidence for analysts or GPT deep dive.
    """
    os.makedirs("sources", exist_ok=True)
    date = datetime.utcnow().strftime("%Y-%m-%d")
    path = f"sources/{date}-sources.md"

    # Reuse grouping function for consistency
    grouped = group_posts_by_topic(posts)

    with open(path, "w", encoding="utf-8") as f:
        f.write(f"# CloudBees Market Watch – Evidence Sources ({date})\n\n")

        for section, items in grouped.items():
            f.write(f"## {section}\n")

            if not items:
                f.write("_No sources found._\n\n")
                continue

            # Only keep title + link
            for p in items:
                title = (p.get("title") or "Untitled").strip()
                url = (p.get("url") or p.get("link") or "").strip()
