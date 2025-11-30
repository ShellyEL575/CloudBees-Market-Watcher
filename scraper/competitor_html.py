# scraper/competitor_html.py

import requests
from bs4 import BeautifulSoup

def fetch_competitor_html_updates():
    sources = {
        "GitLabBlog": "https://about.gitlab.com/blog/",
        "CircleCIBlog": "https://circleci.com/blog/",
        "CloudBeesBlog": "https://www.cloudbees.com/blog",
        "HarnessBlog": "https://www.harness.io/blog",
        "AWSDevOpsBlog": "https://aws.amazon.com/blogs/devops/feed/",
        "AzureDevOpsBlog": "https://devblogs.microsoft.com/devops/feed/",
        "AtlassianEngBlog": "https://blog.developer.atlassian.com/feed/",
    }

    posts = []

    for brand, url in sources.items():
        try:
            response = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
            soup = BeautifulSoup(response.text, "html.parser")

            if brand == "GitLabBlog":
                articles = soup.select(".gl-blog-post")
                for a in articles[:10]:
                    title = a.select_one("h2")
                    link = a.select_one("a")
                    if title and link:
                        posts.append({
                            "source": brand,
                            "title": title.get_text(strip=True),
                            "url": link["href"],
                            "type": "🚀 Product Updates"
                        })

            elif brand == "CircleCIBlog":
                articles = soup.select(".post-item")
                for a in articles[:10]:
                    title = a.select_one("h3")
                    link = a.select_one("a")
                    if title and link:
                        posts.append({
                            "source": brand,
                            "title": title.get_text(strip=True),
                            "url": link["href"],
                            "type": "🚀 Product Updates"
                        })

            elif brand == "CloudBeesBlog":
                articles = soup.select(".views-row")
                for a in articles[:10]:
                    title = a.select_one(".field-content")
                    link = a.select_one("a")
                    if title and link:
                        href = link["href"]
                        full_url = href if href.startswith("http") else f"https://www.cloudbees.com{href}"
                        posts.append({
                            "source": brand,
                            "title": title.get_text(strip=True),
                            "url": full_url,
                            "type": "🚀 Product Updates"
                        })

        except Exception as e:
            print(f"❌ Failed to scrape {brand}: {e}")

    print(f"\n✅ HTML scraper pulled {len(posts)} posts from {len(sources)} brands.")
    for brand in sources:
        brand_posts = [p for p in posts if p['source'] == brand]
        print(f"   - {brand}: {len(brand_posts)} posts")

    return posts
