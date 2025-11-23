import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_summary(posts):
    if not posts:
        return "No content available to summarize."

    text_input = "\n".join(f"- {post.get('title', '')}: {post.get('link', '[No link]')}" for post in posts)

    print("📌 Collected Links:")
    for post in posts:
        print(f"- {post.get('title', 'No Title')}: {post.get('link', '[No link]')}")

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a tech industry analyst writing concise summaries."},
            {"role": "user", "content": f"Summarize the following posts with insights, trends, or takeaways:\n{text_input}"}
        ],
        temperature=0.7
    )

    return response.choices[0].message.content.strip()

def extract_insights_from_social(posts):
    if not posts:
        return "No content available to summarize."

    text_input = "\n".join(f"- {post.get('title', '')}: {post.get('text', '')}" for post in posts)

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": """You are a DevOps expert. Analyze the following social posts and extract:
1. Key Trends
2. Pain Points
3. Opportunities for CloudBees
4. Indicators of DevOps Market Sentiment"""
            },
            {"role": "user", "content": text_input}
        ],
        temperature=0.7
    )

    return response.choices[0].message.content.strip()
