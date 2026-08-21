from app.mistral_client import chat_json
from app.prompts.parsing_prompts import (
    CV_PARSE_SYSTEM,
    JD_PARSE_SYSTEM,
    build_cv_parse_prompt,
    build_jd_parse_prompt,
)
from app.schemas import ParsedCV, ParsedJD


def parse_cv(cv_text: str) -> ParsedCV:
    raw = chat_json(CV_PARSE_SYSTEM, build_cv_parse_prompt(cv_text))
    return ParsedCV(**raw)


def parse_jd(jd_text: str) -> ParsedJD:
    raw = chat_json(JD_PARSE_SYSTEM, build_jd_parse_prompt(jd_text))
    return ParsedJD(**raw)
