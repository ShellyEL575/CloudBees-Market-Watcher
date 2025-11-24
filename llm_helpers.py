# llm_helpers.py (FINAL)
from openai import OpenAI
import os
import math

client = OpenAI()

BATCH_SIZE = 35  # keep stable + within token limits


def extract_post_blurbs(posts):
    """Turn posts into short, LLM-friendly blurbs."""
    return [
        {
            "title": p.get("title", ""),
            "url": p.get("url") or p.get("link") or "",
            "summary": p.get("summary", "") or "",
            "source": p.get("source", "")
        }
        for p in posts
        if isinstance(p, dict)
    ]


def llm_extract_insights(batch):
    """Ask LLM for insights for a single batch."""
    text_blob = "\n".join(
        f"Title: {item['title']}\nURL: {item['url']}\nSummary: {item['summary']}"
        for item in batch
    )

    prompt = f"""
You are a senior DevOps market analyst. Extract insights ONLY from the data below.

Return EXACTLY these sections in Markdown:

### Key Trends
- ...

### Pain Points
- ...

### Opportunities for CloudBees
- ...

### Indicators of DevOps Market Sentiment
- ...

DATA:
{text_blob}
"""

    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )

    return resp.choices[0].message.content


def llm_link_evidence(insight_markdown, all_posts):
    """
    Adds "(🔗 Source: title — url)" line under each bullet.
    Uses fuzzy text matching.
    """

    text_blob = "\n".join(
        f"{p.get('title')} || {p.get('url')} || {p.get('summary', '')}"
        for p in all_posts
    )

    prompt = f"""
You will take the insight markdown and attach evidence links.

For each bullet:
- Identify 1–2 most relevant posts.
- Append lines like:  
  - 🔗 Source: <title> (<url>)

Return ONLY updated markdown.

INSIGHTS:
{insight_markdown}

POST INDEX:
{text_blob}
"""

    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
    )

    return resp.choices[0].message.content


def extract_insights_batch_linked(posts):
    """Main pipeline: batching → insight extraction → evidence linking."""
    print("🔄 Processing in batches of 35...")

    blurbs = extract_post_blurbs(posts)
    if not blurbs:
        return "No insights."

    total = len(blurbs)
    batches = math.ceil(total / BATCH_SIZE)

    batch_insights = []
    for i in range(batches):
        start = i * BATCH_SIZE
        end = start + BATCH_SIZE
        batch = blurbs[start:end]
        print(f"  📦 Batch {i+1} ({len(batch)} posts)")

        insight = llm_extract_insights(batch)
        batch_insights.append(insight)

    combined = "\n\n".join(batch_insights)

    print("🔗 Linking insights to sources...")
    linked = llm_link_evidence(combined, blurbs)

    return linked
