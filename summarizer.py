# summarizer.py

import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_summary(posts):
    """
    Produce a clean summary of posts using Markdown links.
    """
    if not posts:
        return "_No posts available for this section._"

    # Markdown-formatted list of posts
    formatted_posts = "\n".join(
        f"- [{post.get('title','Untitled')}]({post.get('link') or post.get('url','')})"
        for post in posts
    )

    prompt = f"""
You are a DevOps market analyst. Summarize the following posts **clearly and concisely**.

Posts:
{formatted_posts}

Your summary should:
- Capture the important themes
- Avoid repeating all items
- Remain objective
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300,
        temperature=0.4,
    )

    return response.choices[0].message.content.strip()



def extract_insights_from_social(posts):
    """
    Extract insights: trends, pain points, opportunities, sentiment.
    """
    if not posts:
        return "_No social buzz posts available for insights._"

    formatted_posts = "\n".join(
        f"- [{post.get('title','Untitled')}]({post.get('link') or post.get('url','')})"
        for post in posts
    )

    prompt = f"""
You are a senior DevOps strategist. Read the following social posts:

{formatted_posts}

Return insights in this structure:

### Key Trends:
- ...

### Pain Points:
- ...

### Opportunities for CloudBees:
- ...

### Indicators of DevOps Market Sentiment:
- ...
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500,
        temperature=0.4,
    )

    return response.choices[0].message.content.strip()
