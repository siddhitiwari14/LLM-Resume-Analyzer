def build_prompt(resume_text: str, jd: str) -> str:
    return f"""
You are an AI recruiter.

STRICT RULES:
- Return ONLY JSON
- No explanation
- No markdown
- No text outside JSON

FORMAT:
{{
  "match_score": number,
  "missing_skills": [],
  "strengths": [],
  "suggestions": []
}}

Resume:
{resume_text}

Job Description:
{jd}
"""