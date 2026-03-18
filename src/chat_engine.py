import openai
import pandas as pd

def ask_ai(df, question):

    summary = df.describe().to_string()

    prompt = f"""
You are a procurement intelligence analyst.

Dataset summary:
{summary}

Question:
{question}

Answer clearly with insights and recommendations.
"""

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message["content"]