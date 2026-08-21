from typing import List, Optional
from pydantic import BaseModel, Field


class Experience(BaseModel):
    title: str
    company: Optional[str] = None
    duration: Optional[str] = None
    highlights: List[str] = Field(default_factory=list)


class ParsedCV(BaseModel):
    full_name: Optional[str] = None
    summary: Optional[str] = None
    skills: List[str] = Field(default_factory=list)
    experience: List[Experience] = Field(default_factory=list)
    education: List[str] = Field(default_factory=list)
    years_of_experience: Optional[float] = None
    titles: List[str] = Field(default_factory=list)


class ParsedJD(BaseModel):
    job_title: Optional[str] = None
    company: Optional[str] = None
    required_skills: List[str] = Field(default_factory=list)
    preferred_skills: List[str] = Field(default_factory=list)
    responsibilities: List[str] = Field(default_factory=list)
    seniority_level: Optional[str] = None
    min_years_experience: Optional[float] = None


class SkillMatch(BaseModel):
    matched_skills: List[str] = Field(default_factory=list)
    missing_required_skills: List[str] = Field(default_factory=list)
    missing_preferred_skills: List[str] = Field(default_factory=list)
    extra_skills: List[str] = Field(default_factory=list)


class GapAnalysis(BaseModel):
    experience_gaps: List[str] = Field(default_factory=list)
    seniority_alignment: Optional[str] = None
    notes: Optional[str] = None


class Recommendation(BaseModel):
    suggestion: str
    reason: str


class AnalysisResult(BaseModel):
    compatibility_score: float  # 0-100 combined score
    semantic_similarity: float  # 0-1 raw cosine similarity
    skill_match: SkillMatch
    gap_analysis: GapAnalysis
    recommendations: List[Recommendation]
    parsed_cv: ParsedCV
    parsed_jd: ParsedJD
