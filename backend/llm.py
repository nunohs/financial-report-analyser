import time

from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_answer(question: str, relevant_chunks: list[str]) -> str:
    context = "\n\n---\n\n".join(relevant_chunks)

    prompt = f"""You are a financial analyst assistant.
Based ONLY on the following excerpts from a financial report, answer the question below.
Do not use any outside knowledge. If the answer cannot be found in the excerpts, say "I couldn't find that information in the provided report."

Excerpts:
{context}

Question: {question}

Answer:"""

    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model="models/gemini-2.5-flash",
                contents=prompt
            )
            return response.text
        except Exception as e:
            if attempt < max_retries - 1:
                wait_time = 5 * (attempt + 1)
                print(f"Answer generation failed, retrying in {wait_time}s...")
                time.sleep(wait_time)
            else:
                return "I'm having trouble connecting to the AI service. Please try again in a moment."

def generate_summary(chunks: list[str]) -> str:
    sample_text = "\n\n".join(chunks[:20])

    prompt = f"""You are a financial analyst. Based on the following excerpts from a financial report, provide a structured summary with exactly these 5 bullet points:
- Company Overview:
- Financial Highlights:
- Key Risks:
- Growth Strategy:
- Outlook:

Excerpts:
{sample_text}

Summary:"""

    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model="models/gemini-2.5-flash",
                contents=prompt
            )
            return response.text
        except Exception as e:
            if attempt < max_retries - 1:
                wait_time = 5 * (attempt + 1)
                print(f"Summary generation failed, retrying in {wait_time}s...")
                time.sleep(wait_time)
            else:
                return "Summary temporarily unavailable. Please ask questions directly."