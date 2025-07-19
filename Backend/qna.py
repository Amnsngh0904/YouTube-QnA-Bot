import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def answer_query(question, transcript):
    prompt = f"""
You are a helpful and intelligent assistant fluent in both English and Hindi. 
Use the given transcript (which may contain Hindi in Roman or Devanagari script) to answer the user's question accurately.

Transcript:
{transcript}

Question: {question}

Answer in the same language as the question, and if you cannot find a relevant answer in the transcript, say so.
    """
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": "You are a multilingual assistant, fluent in Hindi and English."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()
