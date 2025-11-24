# llm_helpers.py (PMM-aware version)
from openai import OpenAI
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
            "source": p.get("source", ""),
        }
        for p in posts
        if isinstance(p, dict)
    ]


def llm_extract_insights(batch):
    """
    First pass: extract structured insights as VP PMM,
    separating market reality from vendor positioning.
    """
    text_blob = "\n".join(
        f"Title: {item['title']}\nURL: {item['url']}\nSource: {item['source']}\nSummary: {item['summary']}"
        for item in batch
    )

    prompt = f"""
You are the VP of Product Marketing at CloudBees.

You are reviewing a batch of DevOps / CI/CD related posts pulled from:
- Competitor / vendor domains (e.g., cloudbees.com, about.gitlab.com, github.blog, harness.io,
  aws.amazon.com, devblogs.microsoft.com, azure.com, etc.)
- Community / neutral sources (Hacker News, Reddit, StackOverflow, community forums,
  independent blogs, Q&A, reviews, analyst sites, docs).

Key framing:
- Posts on vendor domains reflect what those vendors WANT the market to believe
  (positioning, roadmap, thought leadership). They are NOT neutral sentiment.
- Community / neutral posts are closer to REAL market signals: practitioner pain, demand,
  skepticism, adoption patterns.

From ONLY the text below, produce an EXECUTIVE-READY summary in Markdown
with EXACTLY these sections:

### Customer & Community Signals (market reality)
- Bullets that describe real customer / practitioner signals and pain
- PRIORITIZE themes coming from non-vendor domains: Reddit, HN, StackOverflow,
  community.jenkins.io, independent blogs, docs, analysts, reviews, etc.
- Focus on what people are struggling with, adopting, or asking for.

### Competitor Narratives (how vendors are trying to shape the market)
- Bullets summarizing the main storylines pushed by GitLab, GitHub, Harness, AWS,
  and other vendors.
- Make it clear these are vendor-driven narratives, not organic sentiment.

### Strategic Implications for CloudBees
- 3–6 bullets suggesting how CloudBees should respond.
- Be concrete and pragmatic (e.g., “lean into safe Jenkins modernization”, “clarify
  stance on AI in pipelines”, “simplify migration story from Jenkins to CloudBees”).
- Do NOT invent product features; stay anchored to what you see.

Guidelines:
- Be concise and specific.
- Do NOT include raw URLs here.
- Do NOT invent facts beyond what could reasonably be inferred from the posts.

BATCH POSTS:
{text_blob}
"""

    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )

    return resp.choices[0].message.content


def llm_link_evidence(insight_markdown, all_posts):
    """
    Second pass: attach evidence links to each bullet.

    For:
    - "Customer & Community Signals": PREFER non-vendor domains:
      - reddit.com, news.ycombinator.com, stackoverflow.com, community.jenkins.io,
        independent blogs, docs, analyst sites, Q&A, reviews, etc.
    - "Competitor Narratives": PREFER vendor domains:
      - cloudbees.com, about.gitlab.com, github.blog, harness.io, aws.amazon.com,
        devblogs.microsoft.com, azure.microsoft.com, etc.
    """
    # Flatten posts into a simple index string the model can scan
    post_index = "\n".join(
        f"TITLE: {p.get('title')}\nURL: {p.get('url') or p.get('link')}\nSUMMARY: {p.get('summary', '')}"
        for p in all_posts
        if isinstance(p, dict)
    )

    prompt = f"""
You are assisting a VP of Product Marketing who already wrote an insight summary.

Your job:
- Attach 1–2 evidence links under EACH bullet point in the insight markdown.
- Use the list of posts (titles + URLs + summaries) as your evidence pool.

VERY IMPORTANT SELECTION RULES:

1) For bullets under "Customer & Community Signals (market reality)":
   - Prefer sources that are NOT vendor-controlled:
     - reddit.com, news.ycombinator.com, stackoverflow.com, community.jenkins.io,
       independent blogs, Q&A, reviews, docs, analyst / research sites, etc.
   - These should reflect real customer/practitioner sentiment and pain.

2) For bullets under "Competitor Narratives (how vendors are trying to shape the market)":
   - Prefer vendor domains such as:
     - cloudbees.com, about.gitlab.com, github.blog, harness.io, aws.amazon.com,
       devblogs.microsoft.com, azure.microsoft.com, etc.
   - These represent vendor positioning and story-shaping.

3) For "Strategic Implications for CloudBees":
   - You may attach a mix of evidence showing both:
     - the underlying pain / demand (community/neutral), and
     - relevant vendor positioning (competitor content)
   - But still follow the domain preferences above when choosing what to attach.

Output format:
- KEEP the original markdown structure and text of INSIGHTS exactly as given.
- Under each bullet, add 1–2 lines like:
  - 🔗 Source: <title> (<url>)
  - 🔗 Source: <title> (<url>)

Do NOT add any commentary outside the markdown.
Do NOT invent URLs or titles — use only the provided posts.

INSIGHTS:
{insight_markdown}

POSTS INDEX:
{post_index}
"""

    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )

    return resp.choices[0].message.content


def extract_insights_batch_linked(posts):
    """
    Main pipeline: batching → VP-PMM-style insights → evidence linking.

    Returns:
        Markdown string with:
        - Customer & Community Signals
        - Competitor Narratives
        - Strategic Implications for CloudBees
        and per-bullet evidence links.
    """
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
        print(f"  📦 Batch {i + 1} ({len(batch)} posts)")

        insight = llm_extract_insights(batch)
        batch_insights.append(insight)

    combined = "\n\n".join(batch_insights)

    print("🔗 Linking insights to sources...")
    linked = llm_link_evidence(combined, blurbs)

    return linked
