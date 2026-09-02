import os, time
from openai import OpenAI
from google import genai
from dotenv import load_dotenv

load_dotenv()

groq_client   = OpenAI(api_key=os.getenv("GROQ_API_KEY"),
                            base_url="https://api.groq.com/openai/v1")

gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def battle(prompt):
    msgs = [{"role": "user", "content": prompt}]

    try:
        # Model A — Google Gemini
        a = gemini_client.models.generate_content(model="gemini-3.5-flash", contents=prompt)
        gemini_reply = a.text
    except Exception as e:
        gemini_reply = f"Gemini busy(503), retrying... ({e})\n\nBut Groq Model answered!"

    # Model B — Groq model
    b = groq_client.chat.completions.create(model="openai/gpt-oss-20b", messages=msgs)
    groq_reply = b.choices[0].message.content
        

    return gemini_reply, groq_reply