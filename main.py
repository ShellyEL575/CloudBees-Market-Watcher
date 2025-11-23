import os
from datetime import datetime
from scraper.competitor import fetch_competitor_posts
from scraper.hn import fetch_hn_posts
from scraper.google_watcher import fetch_google_results
from summarizer import generate_summary

def main():
    print("📥 Collecting posts...")
    competitor_posts = fetch_competitor_posts()
    hn_posts = fetch_hn_posts()
    google_posts = fetch_google_results()

    all_posts = competitor_posts + hn_posts + google_posts
    print(f"📦 Total posts collected: {len(all_posts)}")

    grouped = {
        "🚀 Product Updates": [],
        "💬 Social Buzz": [],
        "📈 Trends": []
    }

    for post in all_posts:
        url = post.get("link", "").lower()
        source = post.get("source", "").lower()

        if any(domain in url for domain in ["reddit.com", "linkedin.com", "youtube.com", "medium.com"]):
            grouped["💬 Social Buzz"].append(post)
        elif source == "google search" and any(domain in url for domain in ["reddit.com", "linkedin.com", "youtube.com", "medium.com"]):
            grouped["💬 Social Buzz"].append(post)
        elif "blog" in source or "changelog" in source or "devops" in source:
            grouped["🚀 Product Updates"].append(post)
        else:
            grouped["📈 Trends"].append(post)

    print("\n===== 🧪 Social Buzz Posts =====")
    for post in grouped["💬 Social Buzz"]:
        print(f"- {post['title']} ({post['link']})")

    print("\n===== 📄 Market Watch Summary =====")
    summary = generate_summary(all_posts)
    print(summary)

    # Debug breakdown
    social_buzz_debug = [
        "## 🧪 Debug Info",
        f"- Total competitor posts: {len(competitor_posts)}",
        f"- Total HN posts: {len(hn_posts)}",
        f"- Total Google results: {len(google_posts)}",
        f"  - Filtered by recency: YES",
        f"- Total posts passed to summarizer: {len(all_posts)}",
        f"- Final Social Buzz entries: {len(grouped['💬 Social Buzz'])}"
    ]

    # Save to Markdown
    date_str = datetime.utcnow().strftime("%Y-%m-%d")
    report_path = f"reports/{date_str}.md"
    os.makedirs("reports", exist_ok=True)
    with open(report_path, "w") as f:
        f.write(f"# Market Watch Report – {date_str}\n\n")
        f.write(summary)
        f.write("\n\n")
        f.write("\n".join(social_buzz_debug))

    print(f"\n✅ Report saved to {report_path}")

if __name__ == "__main__":
    main()
