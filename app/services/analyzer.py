from app.core.llm import generate_response
from app.services.parser import truncate_text
from app.services.embedder import compute_similarity
from app.utils.prompt import build_prompt
import json
import re


def clean_response(text: str) -> str:
    """Strip markdown code fences from Gemini output."""
    if not text:
        return ""
    text = re.sub(r"```json\s*", "", text)
    text = re.sub(r"```\s*", "", text)
    return text.strip()


def extract_json(text: str) -> dict | None:
    """Safely extract the first JSON object from a string."""
    try:
        text = clean_response(text)
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if not match:
            return None
        return json.loads(match.group())
    except Exception as e:
        print(f"[JSON PARSE ERROR] {e}")
        return None


def _fallback_result(faiss_score: float, reason: str) -> dict:
    return {
        "match_score": 0,
        "faiss_semantic_score": faiss_score,
        "verdict": "Poor",
        "experience_fit": "Unable to evaluate.",
        "strengths": [],
        "missing_skills": [],
        "skill_gap_analysis": {"present": [], "absent": []},
        "suggestions": [f"⚠️ {reason}"]
    }


def analyze_resume(resume_text: str, jd: str) -> dict:
    # Truncate inputs for token budget
    resume_text = truncate_text(resume_text, 3000)
    jd = truncate_text(jd, 1500)

    # Step 1: FAISS semantic similarity
    print("[EMBEDDER] Computing FAISS similarity...")
    faiss_score = compute_similarity(resume_text, jd)
    print(f"[EMBEDDER] FAISS Score: {faiss_score}")

    # Step 2: Build prompt with FAISS score embedded
    prompt = build_prompt(resume_text, jd, faiss_score)

    # Step 3: Gemini AI feedback
    print("[GEMINI] Sending prompt...")
    response = generate_response(prompt)
    print(f"\n===== GEMINI RAW RESPONSE =====\n{response}\n")

    # Step 4: Handle API errors
    if not response:
        return _fallback_result(faiss_score, "Empty response from Gemini API")
    if "Error:" in response or "429" in response:
        return _fallback_result(faiss_score, f"Gemini API error: {response[:120]}")

    # Step 5: Parse JSON
    parsed = extract_json(response)
    if parsed:
        # Ensure faiss_semantic_score is always present
        parsed.setdefault("faiss_semantic_score", faiss_score)
        return parsed

    return _fallback_result(faiss_score, "Could not parse Gemini response as JSON")