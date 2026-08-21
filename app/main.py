from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from app.parsers import extract_text
from app.schemas import AnalysisResult
from app.services.analysis_service import run_full_analysis
from app.services.parsing_service import parse_cv, parse_jd

app = FastAPI(
    title="AI Resume & Job Matching System",
    description="Upload a CV and a job description to get a compatibility analysis.",
    version="0.1.0",
)

# Allow a local frontend (React/Streamlit dev server) to call this API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


async def _read_upload(file: UploadFile) -> str:
    file_bytes = await file.read()
    try:
        return extract_text(file.filename, file_bytes)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/analyze", response_model=AnalysisResult)
async def analyze(
    cv_file: UploadFile = File(..., description="CV/resume file: .pdf, .docx, or .txt"),
    jd_file: UploadFile = File(..., description="Job description file: .pdf, .docx, or .txt"),
):
    """
    Full pipeline in one call:
    1. Extract text from both uploaded files
    2. Structure both into JSON via Mistral
    3. Compute semantic similarity via embeddings
    4. Run LLM gap analysis (matched/missing skills, experience gaps)
    5. Generate improvement recommendations
    """
    cv_text = await _read_upload(cv_file)
    jd_text = await _read_upload(jd_file)

    try:
        parsed_cv = parse_cv(cv_text)
        parsed_jd = parse_jd(jd_text)
        result = run_full_analysis(parsed_cv, parsed_jd)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Analysis failed: {e}")

    return result
