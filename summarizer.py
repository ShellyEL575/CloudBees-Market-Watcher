from openai import OpenAI
import os

client = OpenAI()

# --- Summary Generator ---
def generate_summary(posts):
    if not posts:
        return "No updates found.\n"

    lines = []
    for post in posts:
        title = post.get("title", "Untitled")
        summary = post.get("summary", "").strip()
        url = post.get("url") or post.get("link") or ""
        lines.append(f"- [{title}]({url}) — {summary}")

    return "\n".join(lines) + "\n"

# --- Insights Extractor ---
def extract_insights_from_social(posts):
    text_blob = "\n".join([
        f"Title: {p.get('title')}\nSummary: {p.get('summary')}" for p in posts
    ])

    prompt = f"""
    You are an expert DevOps market analyst. Extract the key insights from the following posts.
    Return four sections in clean Markdown:

    ### Key Trends
    - bullets

    ### Pain Points
    - bullets

    ### Opportunities for CloudBees
    - bullets

    ### Indicators of DevOps Market Sentiment
    - bullets

    TEXT:
    {text_blob}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
    )

    return response.choices[0].message["content"]
