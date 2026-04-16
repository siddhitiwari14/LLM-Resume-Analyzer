from pydantic import BaseModel, Field
from typing import List, Optional


class SkillGapAnalysis(BaseModel):
    present: List[str] = Field(default_factory=list, description="Skills found in both resume and JD")
    absent: List[str] = Field(default_factory=list, description="Skills required by JD but missing in resume")


class AnalysisResult(BaseModel):
    match_score: int = Field(ge=0, le=100, description="Overall match score 0–100")
    faiss_semantic_score: float = Field(ge=0.0, le=100.0, description="FAISS embedding similarity score 0–100")
    verdict: str = Field(description="One of: Excellent, Good, Fair, Poor")
    experience_fit: str = Field(description="Short paragraph on how well experience aligns")
    strengths: List[str] = Field(default_factory=list)
    missing_skills: List[str] = Field(default_factory=list)
    skill_gap_analysis: Optional[SkillGapAnalysis] = None
    suggestions: List[str] = Field(default_factory=list)


class AnalyzeResponse(BaseModel):
    status: str
    analysis: Optional[AnalysisResult] = None
    message: Optional[str] = None
