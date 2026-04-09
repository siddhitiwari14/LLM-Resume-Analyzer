from app.core.llm import generate_response
from app.services.parser import truncate_text
from app.utils.prompt import build_prompt
import json
import re


def clean_response(text: str):
    if not text:
        return None

    # Remove markdown
    text = text.replace("```json", "").replace("```", "").strip()

    return text


def extract_json(text: str):
    try:
        text = clean_response(text)

        # Extract JSON block safely
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if not match:
            return None

        json_text = match.group()

        return json.loads(json_text)

    except Exception as e:
        print("JSON ERROR:", e)
        return None


def analyze_resume(resume_text: str, jd: str):
    resume_text = truncate_text(resume_text, 1500)
    jd = truncate_text(jd, 800)

    prompt = build_prompt(resume_text, jd)

    response = generate_response(prompt)

    print("\n===== GEMINI RAW RESPONSE =====\n", response)

    # 🔥 Handle API errors directly
    if not response or "Error" in response or "429" in response:
        return {
            "match_score": 0,
            "missing_skills": [],
            "strengths": [],
            "suggestions": ["⚠️ Gemini API error or quota exceeded"]
        }

    parsed = extract_json(response)

    if parsed:
        return parsed

    # 🔥 FINAL FALLBACK (important)
    return {
        "match_score": 0,
        "missing_skills": [],
        "strengths": [],
        "suggestions": ["⚠️ Could not parse Gemini response"]
    }