import os
import json
from datetime import datetime
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_summary(posts):
    text_input = "\n".join(f"- {post['title']}: {post['link']}" for post in posts)
    prompt = f"Summarize the following posts into product updates, social buzz, and key trends:\n{text_input}"

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert tech industry analyst."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5
    )

    return response.choices[0].message.content.strip()

def extract_insights_from_social(posts):
    text_input = "\n".join(f"- {post['title']}: {post['link']}" for post in posts)
    prompt = f"Analyze these social posts and summarize key concerns, sentiments, or insights about developer experience or CI/CD trends:\n{text_input}"

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a DevOps strategist analyzing community sentiment and insights."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5
    )

    return response.choices[0].message.content.strip()
