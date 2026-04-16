from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.services.parser import extract_text_from_pdf
from app.services.analyzer import analyze_resume
from app.models.schema import AnalyzeResponse
import tempfile
import os

router = APIRouter()


@router.get("/health", tags=["System"])
async def health_check():
    """Server health check."""
    return {"status": "ok", "service": "LLM Resume Analyzer"}


@router.post("/analyze", response_model=AnalyzeResponse, tags=["Resume"])
async def analyze(
    file: UploadFile = File(..., description="Resume PDF file"),
    jd: str = Form(..., description="Job description text")
):
    """
    Analyze a resume PDF against a job description.

    - Extracts text from the uploaded PDF
    - Computes FAISS semantic similarity using Google embeddings
    - Sends enriched prompt to Google Gemini for AI feedback
    - Returns match score, skill gap analysis, strengths, and actionable suggestions
    """
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    if not jd.strip():
        raise HTTPException(status_code=400, detail="Job description cannot be empty.")

    temp_path = None
    try:
        # Save uploaded file to a temp location
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp:
            temp.write(await file.read())
            temp_path = temp.name

        resume_text = extract_text_from_pdf(temp_path)

        if not resume_text.strip():
            raise HTTPException(status_code=422, detail="Could not extract text from the PDF. Ensure it is not image-only.")

        result = analyze_resume(resume_text, jd)

        return AnalyzeResponse(status="success", analysis=result)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Always clean up temp file
        if temp_path and os.path.exists(temp_path):
            os.unlink(temp_path)