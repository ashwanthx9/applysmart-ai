import json
import re
import streamlit as st
from pypdf import PdfReader

try:
    import google.generativeai as genai
except ImportError:
    genai = None


# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="ApplySmart AI",
    page_icon="💼",
    layout="wide"
)


# -------------------------------------------------
# CUSTOM BACKGROUND + UI STYLE
# -------------------------------------------------
st.markdown(
    """
    <style>
    .stApp {
        background:
            radial-gradient(circle at top left, rgba(37, 99, 235, 0.25), transparent 35%),
            radial-gradient(circle at top right, rgba(124, 58, 237, 0.22), transparent 35%),
            linear-gradient(135deg, #020617 0%, #0f172a 45%, #111827 100%);
        color: #f8fafc;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }

    .hero-card {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.14);
        border-radius: 24px;
        padding: 32px;
        margin-bottom: 25px;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.35);
        backdrop-filter: blur(14px);
    }

    .main-title {
        font-size: 48px;
        font-weight: 850;
        color: white;
        margin-bottom: 6px;
        letter-spacing: -1px;
    }

    .sub-title {
        font-size: 19px;
        color: #cbd5e1;
        margin-bottom: 18px;
    }

    .tag {
        display: inline-block;
        background: rgba(59, 130, 246, 0.15);
        color: #bfdbfe;
        border: 1px solid rgba(147, 197, 253, 0.28);
        padding: 7px 12px;
        border-radius: 999px;
        font-size: 13px;
        margin-right: 8px;
        margin-bottom: 8px;
    }

    .section-card {
        background: rgba(255, 255, 255, 0.075);
        border: 1px solid rgba(255, 255, 255, 0.13);
        border-radius: 20px;
        padding: 22px;
        margin-bottom: 18px;
        box-shadow: 0 12px 35px rgba(0, 0, 0, 0.25);
        backdrop-filter: blur(12px);
    }

    .section-title {
        font-size: 23px;
        font-weight: 750;
        color: #ffffff;
        margin-bottom: 8px;
    }

    .section-desc {
        font-size: 14px;
        color: #cbd5e1;
        margin-bottom: 12px;
    }

    .success-pill {
        background: rgba(34, 197, 94, 0.13);
        border: 1px solid rgba(34, 197, 94, 0.32);
        color: #bbf7d0;
        padding: 9px 12px;
        border-radius: 12px;
        margin-bottom: 8px;
        font-size: 14px;
    }

    .warning-pill {
        background: rgba(239, 68, 68, 0.13);
        border: 1px solid rgba(248, 113, 113, 0.32);
        color: #fecaca;
        padding: 9px 12px;
        border-radius: 12px;
        margin-bottom: 8px;
        font-size: 14px;
    }

    .info-pill {
        background: rgba(59, 130, 246, 0.13);
        border: 1px solid rgba(96, 165, 250, 0.30);
        color: #bfdbfe;
        padding: 9px 12px;
        border-radius: 12px;
        margin-bottom: 8px;
        font-size: 14px;
    }

    .stButton > button {
        background: linear-gradient(90deg, #2563eb, #7c3aed);
        color: white;
        border: none;
        border-radius: 14px;
        padding: 0.85rem 1.5rem;
        font-size: 17px;
        font-weight: 700;
        width: 100%;
        box-shadow: 0 12px 28px rgba(37, 99, 235, 0.28);
    }

    .stButton > button:hover {
        background: linear-gradient(90deg, #1d4ed8, #6d28d9);
        color: white;
        border: none;
    }

    .stTextArea textarea {
        border-radius: 16px !important;
        border: 1px solid rgba(148, 163, 184, 0.22) !important;
        background-color: rgba(15, 23, 42, 0.72) !important;
        color: #f8fafc !important;
        font-size: 14px !important;
    }

    .stTextInput input {
        border-radius: 12px !important;
        background-color: rgba(15, 23, 42, 0.72) !important;
        color: #f8fafc !important;
    }

    .stFileUploader {
        background: rgba(15, 23, 42, 0.48);
        border: 1px dashed rgba(147, 197, 253, 0.35);
        padding: 14px;
        border-radius: 16px;
    }

    div[data-testid="metric-container"] {
        background: rgba(15, 23, 42, 0.72);
        border: 1px solid rgba(148, 163, 184, 0.18);
        padding: 18px;
        border-radius: 18px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.22);
    }

    section[data-testid="stSidebar"] {
        background: rgba(2, 6, 23, 0.96);
        border-right: 1px solid rgba(148, 163, 184, 0.16);
    }

    .streamlit-expanderHeader {
        font-weight: 700;
    }

    .stCodeBlock {
        border-radius: 14px;
    }

    .footer {
        text-align: center;
        color: #94a3b8;
        font-size: 14px;
        margin-top: 50px;
        padding: 20px;
        border-top: 1px solid rgba(148, 163, 184, 0.20);
    }

    footer {
        visibility: hidden;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# -------------------------------------------------
# SKILLS LIST
# -------------------------------------------------
SKILLS = [
    "python", "sql", "excel", "power bi", "tableau", "pandas", "numpy",
    "machine learning", "nlp", "scikit-learn", "tensorflow", "java",
    "spring boot", "rest api", "api integration", "postman", "git",
    "github", "aws", "azure", "docker", "linux", "javascript", "html",
    "css", "data analysis", "data cleaning", "dashboard", "reporting",
    "kpi", "business insights", "root cause analysis", "troubleshooting",
    "stakeholder communication", "problem solving", "communication",
    "agile", "jira", "technical support", "application support",
    "debugging", "software testing", "documentation", "customer support",
    "analytics", "data visualization", "statistics", "etl", "database",
    "power query", "dax", "stakeholders", "requirements gathering",
    "business analysis", "cloud", "ci/cd", "microservices", "fastapi",
    "streamlit", "mysql", "postgresql", "mongodb", "rest", "api",
    "data validation", "data modelling", "dashboarding", "report automation"
]


# -------------------------------------------------
# HELPER FUNCTIONS
# -------------------------------------------------
def extract_text_from_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text.strip()


def extract_skills(text):
    text = text.lower()
    found_skills = []

    for skill in SKILLS:
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, text):
            found_skills.append(skill.title())

    return sorted(set(found_skills))


def clean_json_response(text):
    text = text.strip()

    if text.startswith("```"):
        text = text.replace("```json", "").replace("```", "").strip()

    start = text.find("{")
    end = text.rfind("}")

    if start != -1 and end != -1:
        text = text[start:end + 1]

    return text


def calculate_basic_match(cv_text, job_text):
    cv_skills = extract_skills(cv_text)
    job_skills = extract_skills(job_text)

    matched_skills = sorted(set(cv_skills).intersection(set(job_skills)))
    missing_skills = sorted(set(job_skills).difference(set(cv_skills)))

    if len(job_skills) == 0:
        score = 0
    else:
        score = round((len(matched_skills) / len(job_skills)) * 100, 2)

    return score, matched_skills, missing_skills, job_skills


def get_ai_analysis(cv_text, job_text, api_key):
    if genai is None:
        raise RuntimeError("google-generativeai is not installed. Run: pip install google-generativeai")

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-2.5-flash")

    prompt = f"""
You are an expert ATS resume reviewer, CV writer, and career coach for Ireland-based job seekers.

Analyse the candidate CV against the job description and return practical resume modifications.

Very important rules:
1. Do NOT give long paragraphs.
2. Use short, copy-paste friendly outputs.
3. Do NOT invent fake experience.
4. Do NOT ask the candidate to add skills unless they genuinely have experience or can prove it through a project.
5. Keep rewritten experience bullets similar in length to the candidate's current resume style.
6. Do not make the resume longer unnecessarily.
7. Use separate blocks for each section.
8. Keep every output concise.
9. Focus only on:
   - Skills match overview
   - Resume profile section
   - Skills section
   - Experience section
   - Projects section
10. For experience and projects, modify existing points. Do not create too many new points.
11. If a current section is already fine, say it is okay and suggest only minor wording improvements.
12. Make the language ATS-friendly, clear, human, and professional.

Return ONLY valid JSON in this exact structure:

{{
  "role_detected": "",
  "overall_match_score": 0,
  "skills_match_overview": {{
    "matching_skills": [],
    "required_skills_for_role": [],
    "missing_or_weak_skills": [],
    "skills_to_learn_or_strengthen": []
  }},
  "profile_section": {{
    "what_to_change": "",
    "copy_paste_profile": ""
  }},
  "skills_section": {{
    "what_to_change": "",
    "copy_paste_skills_section": {{
      "programming_and_querying": "",
      "data_and_reporting": "",
      "software_and_technical": "",
      "tools_and_platforms": "",
      "professional_skills": ""
    }}
  }},
  "experience_section": {{
    "overall_advice": "",
    "experience_changes": [
      {{
        "section_or_role": "",
        "current_issue": "",
        "suggested_modified_points": []
      }}
    ]
  }},
  "projects_section": {{
    "overall_advice": "",
    "project_changes": [
      {{
        "project_name_or_area": "",
        "keep_or_modify": "",
        "current_issue": "",
        "suggested_modified_points": []
      }}
    ]
  }},
  "final_resume_focus": []
}}

CV:
\"\"\"
{cv_text[:14000]}
\"\"\"

JOB DESCRIPTION:
\"\"\"
{job_text[:14000]}
\"\"\"
"""

    response = model.generate_content(prompt)
    cleaned = clean_json_response(response.text)
    return json.loads(cleaned)


# -------------------------------------------------
# UI FUNCTIONS
# -------------------------------------------------
def show_basic_report(score, matched_skills, missing_skills, job_skills):
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📊 Basic Skills Match</div>', unsafe_allow_html=True)
    st.metric("Basic Match Score", f"{score}%")
    st.markdown("</div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title"> Matching Skills</div>', unsafe_allow_html=True)

        if matched_skills:
            for skill in matched_skills:
                st.markdown(f'<div class="success-pill">{skill}</div>', unsafe_allow_html=True)
        else:
            st.info("No clear matching skills found.")

        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">📌 Role Skills</div>', unsafe_allow_html=True)

        if job_skills:
            for skill in job_skills:
                st.markdown(f'<div class="info-pill">{skill}</div>', unsafe_allow_html=True)
        else:
            st.info("No tracked skills found in the job description.")

        st.markdown("</div>", unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">⚠️ Missing Skills</div>', unsafe_allow_html=True)

        if missing_skills:
            for skill in missing_skills:
                st.markdown(f'<div class="warning-pill">{skill}</div>', unsafe_allow_html=True)
        else:
            st.success("No major missing skills found.")

        st.markdown("</div>", unsafe_allow_html=True)


def show_ai_report(report):
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📌 ApplySmart AI Result</div>', unsafe_allow_html=True)

    score = report.get("overall_match_score", 0)
    role = report.get("role_detected", "Not detected")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("AI Match Score", f"{score}%")

    with col2:
        st.metric("Role Detected", role)

    st.markdown("</div>", unsafe_allow_html=True)

    skills = report.get("skills_match_overview", {})

    with st.expander("✅ 1. Skills Match Overview", expanded=True):
        c1, c2, c3 = st.columns(3)

        with c1:
            st.markdown("#### Matching Skills")
            for item in skills.get("matching_skills", []):
                st.markdown(f'<div class="success-pill">{item}</div>', unsafe_allow_html=True)

        with c2:
            st.markdown("#### Required Skills")
            for item in skills.get("required_skills_for_role", []):
                st.markdown(f'<div class="info-pill">{item}</div>', unsafe_allow_html=True)

        with c3:
            st.markdown("#### Missing / Weak Skills")
            for item in skills.get("missing_or_weak_skills", []):
                st.markdown(f'<div class="warning-pill">{item}</div>', unsafe_allow_html=True)

        st.markdown("#### Topics to Strengthen")
        for item in skills.get("skills_to_learn_or_strengthen", []):
            st.write(f"- {item}")

    profile = report.get("profile_section", {})

    with st.expander("🧾 2. Resume Profile Section", expanded=True):
        st.markdown("#### What to change")
        st.info(profile.get("what_to_change", ""))

        st.markdown("#### Copy-paste profile")
        st.code(profile.get("copy_paste_profile", ""), language="text")

    skills_section = report.get("skills_section", {})
    copy_skills = skills_section.get("copy_paste_skills_section", {})

    with st.expander("🛠️ 3. Skills Section", expanded=True):
        st.markdown("#### What to change")
        st.info(skills_section.get("what_to_change", ""))

        skills_text = f"""Programming & Querying: {copy_skills.get("programming_and_querying", "")}

Data & Reporting: {copy_skills.get("data_and_reporting", "")}

Software & Technical: {copy_skills.get("software_and_technical", "")}

Tools & Platforms: {copy_skills.get("tools_and_platforms", "")}

Professional Skills: {copy_skills.get("professional_skills", "")}
"""
        st.markdown("#### Copy-paste skills section")
        st.code(skills_text, language="text")

    experience = report.get("experience_section", {})

    with st.expander("💼 4. Experience Section", expanded=False):
        st.markdown("#### Overall advice")
        st.info(experience.get("overall_advice", ""))

        changes = experience.get("experience_changes", [])

        if changes:
            for idx, item in enumerate(changes, start=1):
                st.markdown(f"#### Change {idx}: {item.get('section_or_role', 'Experience')}")
                st.warning(item.get("current_issue", ""))

                points = item.get("suggested_modified_points", [])
                for point in points:
                    st.code(point, language="text")
        else:
            st.success("No major experience changes suggested.")

    projects = report.get("projects_section", {})

    with st.expander("🚀 5. Projects Section", expanded=False):
        st.markdown("#### Overall advice")
        st.info(projects.get("overall_advice", ""))

        project_changes = projects.get("project_changes", [])

        if project_changes:
            for idx, item in enumerate(project_changes, start=1):
                st.markdown(f"#### Project {idx}: {item.get('project_name_or_area', 'Project')}")
                st.write("**Keep or modify:**", item.get("keep_or_modify", ""))
                st.warning(item.get("current_issue", ""))

                points = item.get("suggested_modified_points", [])
                for point in points:
                    st.code(point, language="text")
        else:
            st.success("No major project changes suggested.")

    with st.expander("🎯 Final Resume Focus", expanded=False):
        for item in report.get("final_resume_focus", []):
            st.markdown(f'<div class="info-pill">{item}</div>', unsafe_allow_html=True)


# -------------------------------------------------
# HERO SECTION
# -------------------------------------------------
st.markdown(
    """
    <div class="hero-card">
        <div class="main-title">💼 ApplySmart AI</div>
        <div class="sub-title">
            Upload your CV and paste a job description to get role-specific resume changes.
        </div>
        <span class="tag">CV Match Score</span>
        <span class="tag">Missing Skills</span>
        <span class="tag">Resume Profile</span>
        <span class="tag">Skills Section</span>
        <span class="tag">Experience Points</span>
        <span class="tag">Project Improvements</span>
    </div>
    """,
    unsafe_allow_html=True
)


# -------------------------------------------------
# SIDEBAR
# -------------------------------------------------
with st.sidebar:
    st.header("⚙️ Settings")

    analysis_mode = st.radio(
        "Choose analysis mode",
        ["AI Analysis with Gemini", "Basic Analysis"]
    )

    api_key = ""

    if analysis_mode == "AI Analysis with Gemini":
        api_key = st.text_input(
            "Paste your Gemini API key",
            type="password",
            help="Your key is used only for this session and is not saved."
        )

    st.info("AI mode gives resume-ready profile, skills, experience and project changes.")


# -------------------------------------------------
# INPUT SECTION
# -------------------------------------------------
left_col, right_col = st.columns(2)

with left_col:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📄 1. Upload Resume / CV</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-desc">Upload your resume as a PDF file.</div>', unsafe_allow_html=True)
    uploaded_cv = st.file_uploader(
        "Upload your CV as PDF",
        type=["pdf"],
        label_visibility="collapsed"
    )
    st.markdown("</div>", unsafe_allow_html=True)

with right_col:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📝 2. Paste Job Description</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-desc">Paste the full job description here.</div>', unsafe_allow_html=True)
    job_text = st.text_area(
        "Paste the full job description here",
        height=290,
        label_visibility="collapsed"
    )
    st.markdown("</div>", unsafe_allow_html=True)


analyse_button = st.button("🚀 Analyse Resume", use_container_width=True)


# -------------------------------------------------
# ANALYSIS LOGIC
# -------------------------------------------------
if analyse_button:
    if uploaded_cv is None:
        st.warning("Please upload your CV as a PDF.")
    elif job_text.strip() == "":
        st.warning("Please paste the job description.")
    elif analysis_mode == "AI Analysis with Gemini" and api_key.strip() == "":
        st.warning("Please paste your Gemini API key in the sidebar.")
    else:
        with st.spinner("Reading CV and analysing against the job role..."):
            cv_text = extract_text_from_pdf(uploaded_cv)

        if not cv_text:
            st.error("Could not extract text from this PDF. Try a text-based PDF instead of a scanned image PDF.")
        else:
            score, matched_skills, missing_skills, job_skills = calculate_basic_match(cv_text, job_text)

            if analysis_mode == "Basic Analysis":
                show_basic_report(score, matched_skills, missing_skills, job_skills)

            else:
                try:
                    with st.spinner("Generating resume-ready improvement sections..."):
                        ai_report = get_ai_analysis(cv_text, job_text, api_key)

                    show_ai_report(ai_report)

                    with st.expander("Backup Basic Skill Match", expanded=False):
                        show_basic_report(score, matched_skills, missing_skills, job_skills)

                except Exception as e:
                    st.error("AI analysis failed. Showing basic report instead.")
                    st.write("Error details:", str(e))
                    show_basic_report(score, matched_skills, missing_skills, job_skills)

            with st.expander("View Extracted CV Text", expanded=False):
                st.write(cv_text)


# -------------------------------------------------
# FOOTER
# -------------------------------------------------
st.markdown('<div class="footer">Created by Ashwanth</div>', unsafe_allow_html=True)