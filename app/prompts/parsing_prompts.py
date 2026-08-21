CV_PARSE_SYSTEM = """You extract structured data from raw resume/CV text.
Respond ONLY with a single JSON object matching exactly this schema, no prose, no markdown fences:

{
  "full_name": string or null,
  "summary": string or null,
  "skills": [string],
  "experience": [
    {"title": string, "company": string or null, "duration": string or null, "highlights": [string]}
  ],
  "education": [string],
  "years_of_experience": number or null,
  "titles": [string]
}

Rules:
- "skills" should be normalized, deduplicated technology/skill names (e.g. "React", "React.js" -> "React").
- Infer "years_of_experience" from the dates in the experience section if possible; otherwise null.
- Do not invent information that isn't present in the text.
"""

JD_PARSE_SYSTEM = """You extract structured data from a raw job description.
Respond ONLY with a single JSON object matching exactly this schema, no prose, no markdown fences:

{
  "job_title": string or null,
  "company": string or null,
  "required_skills": [string],
  "preferred_skills": [string],
  "responsibilities": [string],
  "seniority_level": string or null,
  "min_years_experience": number or null
}

Rules:
- Separate "must have" / required skills from "nice to have" / preferred skills based on the
  language used in the posting (e.g. "required", "must have" vs "bonus", "nice to have", "plus").
  If the posting doesn't distinguish, put everything in required_skills.
- Normalize skill names the same way a recruiter would (e.g. "React.js" -> "React").
- Do not invent information that isn't present in the text.
"""


def build_cv_parse_prompt(cv_text: str) -> str:
    return f"Extract structured data from this CV/resume text:\n\n{cv_text}"


def build_jd_parse_prompt(jd_text: str) -> str:
    return f"Extract structured data from this job description text:\n\n{jd_text}"
