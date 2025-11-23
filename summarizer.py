import os
from openai import OpenAI, OpenAIError

def generate_summary(posts):
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise OpenAIError("OPENAI_API_KEY environment variable is not set")

    client = OpenAI(api_key=api_key)

    prompt = """
You are a DevOps strategy assistant. Summarize the following updates grouped into:

🚀 Product updates  
💬 Social buzz  
📈 Trends

For each entry:
- Include the **source name**
- Include the **title**
- Include a **markdown link** to the article or post
- Keep each bullet clear and helpful for a PM/DevOps strategist
- Avoid fluff. Only summarize real changes or opinions.

---

Example:

## 💬 Social Buzz
- [HN: “We migrated off Jenkins”](https://news.ycombinator.com/item?id=12345): A heated thread about switching from Jenkins to GitHub Actions and CircleCI.

## 📈 Trends
- Teams are investing more in internal developer platforms and self-service CI/CD.
- AI-based CI features are appearing in GitHub, GitLab, and Harness.

---

Now summarize:
"""

    for post in posts:
        prompt += f"- {post['source']}: {post['title']} ({post['link']})\n  {post['summary']}\n\n"

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
        max_tokens=1200
    )

    return response.choices[0].message.content
