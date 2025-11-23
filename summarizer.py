import os
from openai import OpenAI, OpenAIError

def generate_summary(posts):
    api_key = os.environ.get("OPENAI_API_KEY")

    if not api_key:
        raise OpenAIError("OPENAI_API_KEY environment variable is not set")

    client = OpenAI(api_key=api_key)

    prompt = "Summarize the following tech updates grouped by 🚀 Product updates, 💬 Social buzz, and 📈 Trends. Keep it concise and markdown-formatted:\n\n"
    for post in posts:
        prompt += f"- {post['source']}: {post['title']} ({post['link']})\n  {post['summary']}\n\n"

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        max_tokens=1000
    )
    return response.choices[0].message.content
