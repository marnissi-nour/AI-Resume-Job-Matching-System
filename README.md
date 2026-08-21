<div align="center">

# 🧠 AI Resume & Job Matching System

**Upload a CV and a job description → get a compatibility score, skill gap analysis, and honest, actionable recommendations — powered by Mistral AI.**

[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.38-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Mistral AI](https://img.shields.io/badge/Powered%20by-Mistral%20AI-FA520F)](https://mistral.ai/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

---

## ✨ What it does

Traditional keyword-matching ATS tools miss semantic equivalence (`Postgres` ≈ `PostgreSQL`),
can't reason about experience gaps, and give no actionable feedback. This project combines
**structured LLM extraction** with **embedding-based semantic similarity** to give candidates
a realistic, explainable picture of their fit for a role — and coaches them on how to present
*real* experience better, rather than encouraging resume fabrication.

```
CV file ──┐
          ├─> Extract text ─> Structure via LLM (JSON) ─┐
JD file ──┘                                              ├─> Embedding similarity (semantic score)
                                                           ├─> LLM gap analysis (skills, experience)
                                                           └─> LLM recommendations
                                                           └─> Combined scored report
```

## 🚀 Features

- 📄 Upload CV + job description as **PDF, DOCX, or TXT**
- 📊 **Compatibility score (0-100)** blending semantic similarity + hard skill match
- ✅ Four-way skill breakdown — matched, missing required, missing preferred, extra
- 📈 Experience & seniority alignment analysis with specific gaps called out
- 💡 **3-5 honest, actionable recommendations** — never suggests fabricating experience
- 🔍 Full structured CV/JD data available for transparency
- 🌐 REST API (`POST /analyze`) usable independently of the included UI

## 🖥️ Demo

<div align="center">

*Upload → Analyze → Get your score, skill breakdown, and recommendations in seconds.*

| Score & Skills | Recommendations |
|:---:|:---:|
| Compatibility score, semantic similarity %, matched/missing skills | Numbered, reasoned suggestions to improve your CV |

</div>

## 🏗️ Architecture

**Pipeline stages:**

1. **Ingestion** — parse PDF/DOCX/TXT into clean raw text
2. **Structuring** — an LLM call converts unstructured CV/JD text into typed JSON (skills,
   experience, education, required vs. preferred skills, seniority)
3. **Semantic scoring** — both structured profiles are embedded and compared via cosine
   similarity
4. **Gap analysis** — a second LLM call identifies matched/missing skills and experience
   gaps, normalizing equivalent terms (e.g. `React.js` ↔ `React`)
5. **Recommendations** — a third LLM call generates actionable suggestions, explicitly
   forbidden from recommending fabricated skills or experience
6. **Presentation** — everything is combined into one scored report and rendered in the UI

## 🛠️ Tech stack

| Layer | Technology |
|---|---|
| Backend API | Python, FastAPI |
| LLM & embeddings | [Mistral API](https://mistral.ai/) (`mistral-large-latest` + `mistral-embed`) |
| Document parsing | `pdfplumber`, `python-docx` |
| Data validation | Pydantic |
| Similarity scoring | NumPy (cosine similarity) |
| Frontend | Streamlit |
| Config | `python-dotenv` + `pydantic-settings` |

## 📦 Project structure

```
resume-matcher/
├── app/
│   ├── main.py                 FastAPI app, /analyze endpoint
│   ├── config.py                Settings loader (.env)
│   ├── schemas.py                Pydantic models (ParsedCV, ParsedJD, SkillMatch, ...)
│   ├── parsers.py                PDF/DOCX/TXT text extraction
│   ├── mistral_client.py         Mistral chat (JSON mode) + embeddings wrapper
│   ├── prompts/
│   │   ├── parsing_prompts.py     CV/JD -> structured JSON prompts
│   │   └── analysis_prompts.py    Gap analysis + recommendation prompts
│   └── services/
│       ├── parsing_service.py     Orchestrates structuring calls
│       ├── matching_service.py    Embeddings, cosine similarity, scoring
│       └── analysis_service.py    Orchestrates the full pipeline
├── streamlit_app.py             Frontend UI
├── requirements.txt
├── .env.example
└── README.md
```

## ⚡ Quick start

```bash
# Clone and enter the project
git clone https://github.com/your-username/resume-matcher.git
cd resume-matcher

# Set up a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Configure your API key
cp .env.example .env
# edit .env and set MISTRAL_API_KEY=your_key

# Run the backend
uvicorn app.main:app --reload
```

In a second terminal, launch the UI:

```bash
source venv/bin/activate
streamlit run streamlit_app.py
```

Backend: `http://localhost:8000` (Swagger docs at `/docs`) · Frontend: `http://localhost:8501`

Get a free Mistral API key at [console.mistral.ai/api-keys](https://console.mistral.ai/api-keys).

## 📡 API usage

```bash
curl -X POST http://localhost:8000/analyze \
  -F "cv_file=@/path/to/resume.pdf" \
  -F "jd_file=@/path/to/job_description.txt"
```

<details>
<summary><strong>Example response</strong></summary>

```json
{
  "compatibility_score": 78.4,
  "semantic_similarity": 0.83,
  "skill_match": {
    "matched_skills": ["Python", "FastAPI", "PostgreSQL"],
    "missing_required_skills": ["Kubernetes"],
    "missing_preferred_skills": ["GraphQL"],
    "extra_skills": ["Django"]
  },
  "gap_analysis": {
    "experience_gaps": ["JD asks for 5+ years leading a team; CV shows 2 years as IC"],
    "seniority_alignment": "below requirement",
    "notes": "..."
  },
  "recommendations": [
    {"suggestion": "...", "reason": "..."}
  ],
  "parsed_cv": { "...": "structured CV" },
  "parsed_jd": { "...": "structured JD" }
}
```

</details>

## 🎯 Design decisions

- **Structure before comparing** — raw text is never compared directly; both CV and JD are
  normalized into structured JSON first, which is far more reliable than string matching.
- **Two matching signals, combined** — the compatibility score blends embedding-based
  semantic similarity (40%) with a hard required-skill match ratio (60%), mirroring how
  recruiters and ATS systems actually weight requirements.
- **JSON-mode LLM calls** — every LLM call uses Mistral's structured JSON output mode,
  avoiding brittle regex/markdown parsing of model output.
- **No fabrication, by design** — the recommendation prompt is explicitly constrained to
  suggest better *presentation* of real experience, never invented qualifications.

## 🗺️ Roadmap

- [ ] `/analyze/rewrite` endpoint — generate a full improved CV draft
- [ ] Persist results in Postgres for history/analytics
- [ ] Multi-JD matching (one CV vs. many jobs) via a vector store (Qdrant/Chroma)
- [ ] Auth + rate limiting for public deployment

## 🧑‍💻 Skills demonstrated

NLP-based information extraction · Prompt engineering for structured outputs · Embeddings &
vector similarity · REST API design (FastAPI) · Pydantic data modeling · Multi-stage LLM
pipeline orchestration · Full-stack integration (Python backend + Streamlit frontend)

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

<div align="center">

Built with 🧠 and ☕ using [Mistral AI](https://mistral.ai/)

</div>
