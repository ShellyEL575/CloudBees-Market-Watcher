import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_summary(posts):
    if not posts:
        return "No content available to summarize."

    try:
        text_input = "\n".join(
            f"- {post.get('title', 'No Title')} ({post.get('source', 'Unknown Source')}): {post.get('link', 'No Link')}"
            for post in posts
        )
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes recent DevOps and CI/CD posts."},
                {"role": "user", "content": f"Summarize these items:\n{text_input}"}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Summary generation failed: {e}"

def extract_insights_from_social(posts):
    if not posts:
        return "No social posts to extract insights from."

    try:
        insights_input = "\n".join(
            f"- {post.get('title', 'No Title')} ({post.get('source', 'Unknown')}): {post.get('link', '')}"
            for post in posts
        )
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You're an expert DevOps analyst extracting key trends and sentiment from community discussions."},
                {"role": "user", "content": f"Extract insights and sentiment from the following posts:\n{insights_input}"}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Insight extraction failed: {e}"
