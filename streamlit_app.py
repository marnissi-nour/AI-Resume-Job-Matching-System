import os

import requests
import streamlit as st

API_URL = os.environ.get("RESUME_MATCHER_API_URL", "http://localhost:8000")

st.set_page_config(page_title="AI Resume & Job Matcher", page_icon="🧠", layout="wide")

st.title("🧠 AI Resume & Job Matching System")
st.caption("Upload a CV and a job description to get a compatibility analysis powered by Mistral.")

col1, col2 = st.columns(2)
with col1:
    cv_file = st.file_uploader("CV / Resume", type=["pdf", "docx", "txt"], key="cv")
with col2:
    jd_file = st.file_uploader("Job Description", type=["pdf", "docx", "txt"], key="jd")

analyze_clicked = st.button("Analyze compatibility", type="primary", disabled=not (cv_file and jd_file))

if "result" not in st.session_state:
    st.session_state.result = None

if analyze_clicked:
    with st.spinner("Extracting, structuring, and analyzing... this can take 10-30s"):
        try:
            files = {
                "cv_file": (cv_file.name, cv_file.getvalue()),
                "jd_file": (jd_file.name, jd_file.getvalue()),
            }
            resp = requests.post(f"{API_URL}/analyze", files=files, timeout=120)
            if resp.status_code != 200:
                st.error(f"Analysis failed ({resp.status_code}): {resp.json().get('detail', resp.text)}")
                st.session_state.result = None
            else:
                st.session_state.result = resp.json()
        except requests.exceptions.ConnectionError:
            st.error(f"Could not reach the API at {API_URL}. Is the backend running (`uvicorn app.main:app --reload`)?")
        except Exception as e:
            st.error(f"Unexpected error: {e}")

result = st.session_state.result

if result:
    st.divider()

    # --- Score header ---
    score = result["compatibility_score"]
    sem_sim = result["semantic_similarity"]
    score_col, sem_col, name_col = st.columns([1, 1, 2])
    with score_col:
        st.metric("Compatibility Score", f"{score:.0f} / 100")
    with sem_col:
        st.metric("Semantic Similarity", f"{sem_sim * 100:.0f}%")
    with name_col:
        cv_name = result["parsed_cv"].get("full_name") or "Candidate"
        jd_title = result["parsed_jd"].get("job_title") or "Role"
        jd_company = result["parsed_jd"].get("company")
        subtitle = f"{jd_title} at {jd_company}" if jd_company else jd_title
        st.markdown(f"**{cv_name}** vs **{subtitle}**")

    st.progress(min(1.0, score / 100))

    st.divider()

    # --- Skill match ---
    st.subheader("Skill Match")
    sm = result["skill_match"]
    m_col, mr_col, mp_col, x_col = st.columns(4)

    with m_col:
        st.markdown("✅ **Matched**")
        for s in sm["matched_skills"]:
            st.markdown(f"- {s}")
        if not sm["matched_skills"]:
            st.caption("None found")

    with mr_col:
        st.markdown("❌ **Missing (required)**")
        for s in sm["missing_required_skills"]:
            st.markdown(f"- {s}")
        if not sm["missing_required_skills"]:
            st.caption("None — great fit!")

    with mp_col:
        st.markdown("⚠️ **Missing (preferred)**")
        for s in sm["missing_preferred_skills"]:
            st.markdown(f"- {s}")
        if not sm["missing_preferred_skills"]:
            st.caption("None")

    with x_col:
        st.markdown("➕ **Extra (not in JD)**")
        for s in sm["extra_skills"]:
            st.markdown(f"- {s}")
        if not sm["extra_skills"]:
            st.caption("None")

    st.divider()

    # --- Gap analysis ---
    st.subheader("Experience & Seniority")
    ga = result["gap_analysis"]
    st.markdown(f"**Seniority alignment:** {ga.get('seniority_alignment', 'N/A')}")
    if ga.get("experience_gaps"):
        st.markdown("**Gaps identified:**")
        for gap in ga["experience_gaps"]:
            st.markdown(f"- {gap}")
    if ga.get("notes"):
        st.info(ga["notes"])

    st.divider()

    # --- Recommendations ---
    st.subheader("Recommendations to Improve Your CV")
    for i, rec in enumerate(result["recommendations"], start=1):
        with st.container(border=True):
            st.markdown(f"**{i}. {rec['suggestion']}**")
            st.caption(rec["reason"])

    st.divider()

    # --- Raw structured data (collapsed) ---
    with st.expander("View structured CV data"):
        st.json(result["parsed_cv"])
    with st.expander("View structured job description data"):
        st.json(result["parsed_jd"])

else:
    st.info("Upload a CV and job description, then click **Analyze compatibility**.")
