import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

from knowledge import SYSTEM_PROMPT
from context_router import detect_required_context
from context_builder import build_context

load_dotenv()

# Active Gemini model specified by your API endpoint
GEMINI_MODEL = "gemini-3.6-flash"


def generate_chat_response(user_id: int, message: str) -> dict:
    """Generate a context-aware chat response for MuveFit AI Coach."""
    # Direct fallback if .env fails to load
    api_key = os.getenv("GEMINI_API_KEY") or "AQ.Ab8RN6L9LBeypsBXhD7xNcdbAVHT88v3fnh2Nfs9z1Hl_p9o7gY"
    if not api_key:
        return {
            "answer": "AI service is not configured yet. Please check GEMINI_API_KEY in .env.",
            "context_used": [],
        }

    required_context = detect_required_context(message)
    context_str = build_context(user_id, required_context)

    if context_str.strip():
        user_prompt = f"USER WORKOUT & SYSTEM CONTEXT:\n{context_str}\n\nUSER QUESTION:\n{message}"
    else:
        user_prompt = message

    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=user_prompt,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=0.4,
            ),
        )

        answer_text = response.text if response and response.text else "I couldn't generate a response for that. Please try asking again."

        return {
            "answer": answer_text,
            "context_used": required_context,
        }

    except Exception as e:
        print("GEMINI ERROR:", repr(e))
        return {
            "answer": "I'm having trouble analyzing your request right now. Please try again in a moment.",
            "context_used": required_context,
        }