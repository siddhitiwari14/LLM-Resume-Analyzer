from google import genai
from app.core.config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

def generate_response(prompt: str):
    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )

        # 🔥 FIX: handle different response formats
        if hasattr(response, "text") and response.text:
            return response.text

        # fallback extraction
        if response.candidates:
            return response.candidates[0].content.parts[0].text

        return ""

    except Exception as e:
        return f"Error: {str(e)}"