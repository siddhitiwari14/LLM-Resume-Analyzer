from fastapi import APIRouter, UploadFile, File, Form
from app.services.parser import extract_text_from_pdf
from app.services.analyzer import analyze_resume
import tempfile

router = APIRouter()   # ✅ THIS LINE IS CRITICAL

@router.post("/analyze")
async def analyze(file: UploadFile = File(...), jd: str = Form(...)):
    try:
        with tempfile.NamedTemporaryFile(delete=False) as temp:
            temp.write(await file.read())
            temp_path = temp.name

        resume_text = extract_text_from_pdf(temp_path)

        result = analyze_resume(resume_text, jd)

        return {
            "status": "success",
            "analysis": result
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }