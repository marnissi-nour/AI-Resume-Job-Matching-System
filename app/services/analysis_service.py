from app.mistral_client import chat_json
from app.prompts.analysis_prompts import (
    ANALYSIS_SYSTEM,
    RECOMMENDATIONS_SYSTEM,
    build_analysis_prompt,
    build_recommendations_prompt,
)
from app.schemas import (
    AnalysisResult,
    GapAnalysis,
    ParsedCV,
    ParsedJD,
    Recommendation,
    SkillMatch,
)
from app.services.matching_service import (
    compute_compatibility_score,
    semantic_similarity,
    skill_match_ratio,
)


def run_full_analysis(cv: ParsedCV, jd: ParsedJD) -> AnalysisResult:
    cv_json = cv.model_dump()
    jd_json = jd.model_dump()

    # 1. Semantic similarity via embeddings
    sem_sim = semantic_similarity(cv, jd)

    # 2. LLM-based skill matching + gap analysis
    analysis_raw = chat_json(ANALYSIS_SYSTEM, build_analysis_prompt(cv_json, jd_json))
    skill_match = SkillMatch(**analysis_raw["skill_match"])
    gap_analysis = GapAnalysis(**analysis_raw["gap_analysis"])

    # 3. Compute combined compatibility score
    total_required = len(jd.required_skills) or 1
    ratio = skill_match_ratio(len(skill_match.matched_skills), total_required)
    score = compute_compatibility_score(sem_sim, ratio)

    # 4. LLM-based recommendations, informed by the gap analysis above
    rec_raw = chat_json(
        RECOMMENDATIONS_SYSTEM,
        build_recommendations_prompt(
            cv_json, jd_json, skill_match.model_dump(), gap_analysis.model_dump()
        ),
    )
    recommendations = [Recommendation(**r) for r in rec_raw["recommendations"]]

    return AnalysisResult(
        compatibility_score=score,
        semantic_similarity=round(sem_sim, 4),
        skill_match=skill_match,
        gap_analysis=gap_analysis,
        recommendations=recommendations,
        parsed_cv=cv,
        parsed_jd=jd,
    )
