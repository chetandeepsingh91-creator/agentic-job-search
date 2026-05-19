import os, time
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def call_llm(prompt, retries=3):
    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            return response.choices[0].message.content
            
        except Exception as e:
            if "rate_limit" in str(e).lower():
                wait = (attempt + 1) * 2
                print(f"Rate limit hit. Retrying in {wait}s...")
                time.sleep(wait)
            else:
                raise e

    return "Error: Failed after retries"