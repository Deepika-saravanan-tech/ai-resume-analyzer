import streamlit as st
import PyPDF2
import plotly.express as px

st.set_page_config(
    page_title="AI Resume Analyzer",
    layout="wide"
)

st.title("AI Resume Analyzer")
st.write("Upload a resume to analyze skills, ATS compatibility, and job role suitability.")

st.sidebar.title("Navigation")
st.sidebar.write("Upload a resume file to start the analysis.")

uploaded_file = st.file_uploader("Upload Resume (PDF)", type="pdf")

if uploaded_file is not None:

    pdf_reader = PyPDF2.PdfReader(uploaded_file)

    text = ""

    for page in pdf_reader.pages:
        text += page.extract_text()

    text_lower = text.lower()

    st.subheader("Extracted Resume Content")
    st.write(text)

    # -----------------------------
    # Resume length analysis
    # -----------------------------
    word_count = len(text.split())

    st.subheader("Resume Length Analysis")
    st.write("Word Count:", word_count)

    if word_count < 200:
        st.warning("Resume length is too short.")
    elif word_count > 800:
        st.warning("Resume length is too long.")
    else:
        st.success("Resume length is appropriate.")

    # -----------------------------
    # Skill detection
    # -----------------------------
    skills = [
        "python","java","javascript","sql",
        "html","css","git","github",
        "machine learning","data analysis"
    ]

    found_skills = []

    for skill in skills:
        if skill in text_lower:
            found_skills.append(skill)

    st.subheader("Detected Skills")
    st.write(found_skills)

    # -----------------------------
    # Resume score
    # -----------------------------
    score = len(found_skills) * 10
    if score > 100:
        score = 100

    # -----------------------------
    # ATS Score
    # -----------------------------
    ats_score = 0

    if "github" in text_lower:
        ats_score += 25

    if "linkedin" in text_lower:
        ats_score += 25

    if "project" in text_lower:
        ats_score += 25

    if len(found_skills) >= 5:
        ats_score += 25

    st.subheader("Resume Dashboard")

    col1, col2, col3 = st.columns(3)

    col1.metric("Resume Score", score)
    col2.metric("ATS Score", ats_score)
    col3.metric("Skills Detected", len(found_skills))

    # -----------------------------
    # Resume strength
    # -----------------------------
    st.subheader("Resume Strength Evaluation")

    if score < 40:
        st.error("Resume strength is low.")
    elif score < 70:
        st.warning("Resume strength is moderate.")
    else:
        st.success("Resume strength is high.")

    # -----------------------------
    # Job role compatibility
    # -----------------------------
    st.subheader("Job Role Compatibility")

    roles = {
        "Software Developer": ["java","python","sql","git"],
        "Web Developer": ["html","css","javascript"],
        "Data Analyst": ["python","sql","data analysis"]
    }

    for role in roles:

        role_skills = roles[role]

        match = 0

        for skill in role_skills:
            if skill in text_lower:
                match += 1

        percentage = int((match / len(role_skills)) * 100)

        st.write(role + " : " + str(percentage) + "% match")

    # -----------------------------
    # Skill gap analysis
    # -----------------------------
    st.subheader("Skill Gap Analysis")

    required_skills = ["python","java","sql","git","github"]

    missing_skills = []

    for skill in required_skills:
        if skill not in text_lower:
            missing_skills.append(skill)

    if missing_skills:
        st.write("Missing Skills:", missing_skills)
    else:
        st.write("No significant skill gaps detected.")

    # -----------------------------
    # Skill chart
    # -----------------------------
    st.subheader("Skill Visualization")

    values = []

    for skill in skills:
        if skill in found_skills:
            values.append(1)
        else:
            values.append(0)

    fig = px.bar(
        x=skills,
        y=values,
        title="Skill Presence",
        labels={"x":"Skills","y":"Presence"}
    )

    st.plotly_chart(fig, use_container_width=True)

    # -----------------------------
    # Resume summary (simple NLP)
    # -----------------------------
    st.subheader("Resume Summary")

    sentences = text.split(".")
    summary = sentences[:3]

    for s in summary:
        st.write(s.strip())

    # -----------------------------
    # Suggestions
    # -----------------------------
    st.subheader("Improvement Suggestions")

    suggestions = []

    if "github" not in text_lower:
        suggestions.append("Include GitHub profile link.")

    if "linkedin" not in text_lower:
        suggestions.append("Include LinkedIn profile.")

    if len(found_skills) < 6:
        suggestions.append("Add additional technical skills.")

    if "project" not in text_lower:
        suggestions.append("Include more project experience.")

    if suggestions:
        for s in suggestions:
            st.write("- " + s)
    else:
        st.write("The resume appears strong.")

    # -----------------------------
    # Download report
    # -----------------------------
    report = f"""
Resume Score: {score}
ATS Score: {ats_score}
Detected Skills: {found_skills}
Missing Skills: {missing_skills}
"""

    st.download_button(
        "Download Resume Analysis Report",
        report
    )

st.markdown("---")
st.write("AI Resume Analyzer | Python, Streamlit")