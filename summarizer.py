import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_summary(posts):
    """
    Summarize grouped posts (product updates, social buzz, trends).
    Safely handles missing fields.
    """
    if not posts:
        return "No content available to summarize."

    text_input = "\n".join(
        f"- {post.get('title', 'No Title')} ({post.get('source', 'Unknown Source')}): {post.get('link', 'No Link')}"
        for post in posts
    )

    prompt = f"""
Summarize the following items into a clean, concise section for a CloudBees Market Watch report.

Items:
{text_input}

Return a markdown-ready summary.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes DevOps updates."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"Summary generation failed: {e}"


def extract_insights_from_social(posts):
    """
    Extract deeper insights from social buzz posts.
    """
    if not posts:
        return "No social posts to extract insights from."

    insights_input = "\n".join(
        f"- {post.get('title', 'No Title')} ({post.get('source', 'Unknown')}): {post.get('link', '')}"
        for post in posts
    )

    prompt = f"""
Analyze the following social posts and extract:

- key trends
- pain points
- opportunities for CloudBees
- indicators of DevOps market sentiment

Posts:
{insights_input}

Respond with 4–8 concise bullet points.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert DevOps market analyst."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"Insight extraction failed: {e}"
