import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()


def generate_answer(question, context):

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        return "GROQ_API_KEY not found. Please check your .env file."

    client = Groq(api_key=api_key)

    prompt = f"""
You are a document question-answering chatbot.

Answer the user's question using ONLY the information
provided in the document context.

Do not use outside knowledge.

If the answer is not available in the context, say:
"I couldn't find the answer in the document."

DOCUMENT CONTEXT:
{context}

USER QUESTION:
{question}

ANSWER:
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content