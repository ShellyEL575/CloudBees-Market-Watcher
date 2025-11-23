import os
from datetime import datetime
from scraper.competitor import fetch_competitor_posts
from scraper.hn import fetch_hn_posts
from scraper.google_watcher import fetch_google_results
from summarizer import generate_summary

def main():
    print("📥 Collecting posts...")
    posts = (
        fetch_competitor_posts() +
        fetch_hn_posts() +
        fetch_google_results()
    )
    print(f"📦 Total posts collected: {len(posts)}")

    grouped = {
        "🚀 Product Updates": [],
        "💬 Social Buzz": [],
        "📈 Trends": []
    }

    for post in posts:
        url = post.get("link", "").lower()
        source = post.get("source", "").lower()

        if any(s in url for s in ["reddit.com", "linkedin.com", "youtube.com", "medium.com"]):
            grouped["💬 Social Buzz"].append(post)
        elif "hacker news" in source or "blog" in source or "changelog" in source or "devops" in source:
            grouped["🚀 Product Updates"].append(post)

    print("\n===== 🧪 Social Buzz Posts =====")
    for post in grouped["💬 Social Buzz"]:
        print(f"- {post['title']} ({post['link']})")

    print("\n===== 📄 Market Watch Summary =====")
    summary = generate_summary(posts)
    print(summary)

    date_str = datetime.utcnow().strftime("%Y-%m-%d")
    report_path = f"reports/{date_str}.md"
    os.makedirs("reports", exist_ok=True)
    with open(report_path, "w") as f:
        f.write(f"# Market Watch Report – {date_str}\n\n")
        f.write(summary)

    print(f"\n✅ Report saved to {report_path}")

if __name__ == "__main__":
    main()
