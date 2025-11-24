# llm_helpers.py
from openai import OpenAI
import math

client = OpenAI()

# -----------------------------------------------------
# Helper: Chunk posts into batches for efficient LLM use
# -----------------------------------------------------
def chunk_list(items, size):
    for i in range(0, len(items), size):
        yield items[i : i + size]


# -----------------------------------------------------
# Main function: Batch-linked insights
# -----------------------------------------------------
def extract_insights_batch_linked(posts):
    """
    1. Summaries → batched into <=40-item chunks
    2. LLM extracts insights per batch
    3. LLM merges + links insights to best supporting URLs
    """

    print(f"🧠 Extracting insights across {len(posts)} posts...")

    # STEP 1 — Convert posts into lightweight text
    summaries = [
        {
            "title": p.get("title", ""),
            "summary": p.get("summary", ""),
            "url": p.get("url") or p.get("link") or "",
        }
        for p in posts
    ]

    # STEP 2 — Batch the post-set for LLM context efficiency
    batch_size = 35
    batch_insights = []

    print(f"🔄 Processing in batches of {batch_size}...")

    for batch_num, batch in enumerate(chunk_list(summaries, batch_size), start=1):
        print(f"  📦 Batch {batch_num} ({len(batch)} posts)")

        batch_prompt = f"""
Extract key insights (trends, concerns, migration patterns, opportunities)
from the following set of DevOps-related posts.

ONLY return Markdown bullet points — no commentary.

Posts:
{batch}
"""

        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": batch_prompt}],
            temperature=0.3,
        )

        batch_insights.append(resp.choices[0].message.content)

    print("🔗 Linking insights to sources...")

    # STEP 3 — Merge insights & link to URLs
    merge_prompt = f"""
You are an expert DevOps analyst.

You will receive:
- A list of insight fragments extracted from multiple batches
- The full list of source posts with URLs

Your task:
1. Merge & deduplicate insights into **clean, crisp executive-ready bullets**
2. For each insight, attach 1–3 supporting URLs from the post list
3. Output in this format:

### Key Trends
- Insight text
  - 🔗 Source: URL
  - 🔗 Source: URL

### Pain Points
(bullets + links)

### Opportunities for CloudBees
(bullets + links)

### Indicators of DevOps Market Sentiment
(bullets + links)

Do NOT add commentary.

Batch insights:
{batch_insights}

All source posts:
{summaries}
"""

    merge_resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": merge_prompt}],
        temperature=0.2,
    )

    return merge_resp.choices[0].message.content
