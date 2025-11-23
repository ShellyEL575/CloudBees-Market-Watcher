import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_summary(posts):
    valid_posts = [post for post in posts if 'title' in post and 'link' in post]
    if not valid_posts:
        return "No valid posts with links available for summarization."

    text_input = "\n".join(f"- {post['title']}: {post['link']}" for post in valid_posts)

    print("📌 Collected Links:")
    for post in valid_posts:
        print(f"- {post['title']}: {post.get('link', '[No link]')}")

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful market analyst. Summarize the following posts and highlight key developments, pain points, and opportunities."
            },
            {
                "role": "user",
                "content": text_input
            }
        ]
    )
    return response.choices[0].message.content

def extract_insights_from_social(posts):
    valid_posts = [post for post in posts if 'title' in post and 'link' in post]
    if not valid_posts:
        return "No valid social posts to extract insights from."

    text_input = "\n".join(f"- {post['title']}: {post['link']}" for post in valid_posts)

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "You are a DevOps expert. Analyze the following social posts and extract:
1. Key trends
2. Common pain points
3. Opportunities for CloudBees
4. Indicators of DevOps market sentiment."
            },
            {
                "role": "user",
                "content": text_input
            }
        ]
    )
    return response.choices[0].message.content
