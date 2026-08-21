import numpy as np

from app.mistral_client import embed_texts
from app.schemas import ParsedCV, ParsedJD


def _cv_to_text(cv: ParsedCV) -> str:
    parts = [cv.summary or ""]
    parts += cv.skills
    parts += cv.titles
    for exp in cv.experience:
        parts.append(exp.title)
        parts += exp.highlights
    return " ".join(p for p in parts if p)


def _jd_to_text(jd: ParsedJD) -> str:
    parts = [jd.job_title or ""]
    parts += jd.required_skills
    parts += jd.preferred_skills
    parts += jd.responsibilities
    return " ".join(p for p in parts if p)


def cosine_similarity(vec_a: list, vec_b: list) -> float:
    a = np.array(vec_a)
    b = np.array(vec_b)
    denom = np.linalg.norm(a) * np.linalg.norm(b)
    if denom == 0:
        return 0.0
    return float(np.dot(a, b) / denom)


def semantic_similarity(cv: ParsedCV, jd: ParsedJD) -> float:
    """Returns raw cosine similarity in [0, 1] (in practice usually 0.5-1.0 range)."""
    cv_text = _cv_to_text(cv)
    jd_text = _jd_to_text(jd)
    embeddings = embed_texts([cv_text, jd_text])
    sim = cosine_similarity(embeddings[0], embeddings[1])
    # Clip defensively — cosine similarity can be slightly outside [0,1] due to float error
    return max(0.0, min(1.0, sim))


def compute_compatibility_score(semantic_sim: float, skill_match_ratio: float) -> float:
    """
    Combine semantic similarity and hard skill-match ratio into one 0-100 score.
    Weighted toward skill match since that's usually what recruiters/ATS care about most.
    """
    score = (0.4 * semantic_sim + 0.6 * skill_match_ratio) * 100
    return round(score, 1)


def skill_match_ratio(matched: int, required_total: int) -> float:
    if required_total == 0:
        return 1.0
    return min(1.0, matched / required_total)
