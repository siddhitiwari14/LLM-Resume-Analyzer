from google import genai
from app.core.config import GEMINI_API_KEY, GEMINI_MODEL, EMBEDDING_MODEL

client = genai.Client(api_key=GEMINI_API_KEY)


def generate_response(prompt: str) -> str:
    """Send a prompt to Gemini and return the text response."""
    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt
        )

        if hasattr(response, "text") and response.text:
            return response.text

        if response.candidates:
            return response.candidates[0].content.parts[0].text

        return ""

    except Exception as e:
        return f"Error: {str(e)}"


def generate_embeddings(text: str) -> list[float]:
    """Generate an embedding vector for the given text using Google's embedding model."""
    try:
        response = client.models.embed_content(
            model=EMBEDDING_MODEL,
            contents=text
        )
        # Handle both single and batched response formats
        if hasattr(response, "embeddings") and response.embeddings:
            return response.embeddings[0].values
        if hasattr(response, "embedding"):
            return response.embedding.values
        return []
    except Exception as e:
        print(f"Embedding error: {e}")
        return []