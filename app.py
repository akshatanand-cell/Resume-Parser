import streamlit as st
import pdfplumber
import spacy
import re

# Load AI model
nlp = spacy.load("en_core_web_sm")

# Page config
st.set_page_config(page_title="AI Resume Parser", page_icon="📄", layout="centered")

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;800&display=swap');
    
    * { font-family: 'Poppins', sans-serif; }
    
    .stApp {
        background: linear-gradient(-45deg, #0a0a2e, #1a0a3e, #0d1b4b, #0a2e1a);
        background-size: 400% 400%;
        animation: gradientBG 10s ease infinite;
    }
    
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .hero {
        text-align: center;
        padding: 40px 20px 20px 20px;
        animation: fadeInDown 1s ease;
    }
    
    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .hero h1 {
        font-size: 3.2em;
        font-weight: 800;
        background: linear-gradient(90deg, #34d399, #60a5fa, #f472b6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        background-size: 200% auto;
        animation: shimmer 3s infinite;
    }
    
    @keyframes shimmer {
        0% { background-position: 0% center; }
        50% { background-position: 100% center; }
        100% { background-position: 0% center; }
    }
    
    .badge {
        display: inline-block;
        background: linear-gradient(135deg, #34d399, #60a5fa);
        color: white;
        padding: 5px 18px;
        border-radius: 50px;
        font-size: 0.85em;
        font-weight: 600;
        margin-bottom: 20px;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(52,211,153,0.5); }
        70% { box-shadow: 0 0 0 12px rgba(52,211,153,0); }
        100% { box-shadow: 0 0 0 0 rgba(52,211,153,0); }
    }
    
    .card {
        background: rgba(255,255,255,0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 20px;
        padding: 25px;
        margin: 15px 0;
        animation: fadeIn 0.8s ease;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .info-item {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 12px;
        padding: 15px 20px;
        margin: 10px 0;
        animation: fadeIn 0.5s ease;
    }

    .info-label {
        font-size: 0.8em;
        font-weight: 600;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 5px;
    }

    .info-value {
        color: white;
        font-size: 1em;
        font-weight: 500;
    }

    .skill-tag {
        display: inline-block;
        background: linear-gradient(135deg, #34d399, #60a5fa);
        color: white;
        padding: 5px 15px;
        border-radius: 50px;
        font-size: 0.85em;
        font-weight: 600;
        margin: 5px;
    }

    .stats-row {
        display: flex;
        gap: 15px;
        margin: 20px 0;
    }
    
    .stat-box {
        flex: 1;
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 15px;
        padding: 20px;
        text-align: center;
    }
    
    .stat-number {
        font-size: 2em;
        font-weight: 800;
        background: linear-gradient(90deg, #34d399, #60a5fa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .stat-label {
        color: #94a3b8;
        font-size: 0.8em;
        margin-top: 5px;
    }

    .stButton button {
        background: linear-gradient(135deg, #34d399, #60a5fa) !important;
        color: white !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 15px 50px !important;
        font-size: 1.1em !important;
        font-weight: 600 !important;
        font-family: 'Poppins', sans-serif !important;
        width: 100% !important;
        transition: all 0.3s ease !important;
        letter-spacing: 1px !important;
    }
    
    .stButton button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 15px 35px rgba(52,211,153,0.4) !important;
    }

    .footer {
        text-align: center;
        padding: 30px;
        color: #475569;
        font-size: 0.85em;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Hero
st.markdown("""
<div class="hero">
    <div class="badge">🤖 Powered by SpaCy AI</div>
    <h1>📄 AI Resume Parser</h1>
    <p style="color:#94a3b8; font-size:1.1em;">Extract key information from resumes instantly using AI</p>
    <p style="color:#34d399; font-size:0.9em; font-weight:600;">
        Akshat Anand &nbsp;|&nbsp; Building intelligent systems that solve real problems
    </p>
</div>
""", unsafe_allow_html=True)

# Common skills list
SKILLS = [
    "python", "java", "javascript", "c++", "c#", "html", "css", "react",
    "node", "sql", "mysql", "mongodb", "tensorflow", "pytorch", "keras",
    "machine learning", "deep learning", "nlp", "computer vision", "ai",
    "data science", "data analysis", "pandas", "numpy", "matplotlib",
    "streamlit", "flask", "django", "fastapi", "git", "github", "docker",
    "kubernetes", "aws", "azure", "gcp", "linux", "excel", "tableau",
    "power bi", "r", "matlab", "opencv", "scikit-learn", "hadoop", "spark"
]

def extract_email(text):
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(pattern, text)
    return emails[0] if emails else "Not found"

def extract_phone(text):
    pattern = r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]'
    phones = re.findall(pattern, text)
    return phones[0] if phones else "Not found"

def extract_name(text):
    doc = nlp(text[:500])
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
    lines = text.strip().split('\n')
    for line in lines[:5]:
        if line.strip() and len(line.strip()) > 2:
            return line.strip()
    return "Not found"

def extract_skills(text):
    text_lower = text.lower()
    found = [skill.title() for skill in SKILLS if skill in text_lower]
    return list(set(found))

def extract_education(text):
    education_keywords = [
        "bachelor", "master", "phd", "b.tech", "m.tech", "bca", "mca",
        "b.sc", "m.sc", "mba", "b.e", "m.e", "degree", "university",
        "college", "institute", "school", "diploma", "engineering"
    ]
    lines = text.split('\n')
    education = []
    for line in lines:
        if any(keyword in line.lower() for keyword in education_keywords):
            if line.strip():
                education.append(line.strip())
    return education[:5] if education else ["Not found"]

def extract_experience(text):
    experience_keywords = [
        "experience", "worked", "working", "engineer", "developer",
        "analyst", "manager", "intern", "internship", "company",
        "organization", "position", "role", "job"
    ]
    lines = text.split('\n')
    experience = []
    for line in lines:
        if any(keyword in line.lower() for keyword in experience_keywords):
            if line.strip() and len(line.strip()) > 10:
                experience.append(line.strip())
    return experience[:5] if experience else ["Not found"]

# Upload
st.markdown('<div class="card">', unsafe_allow_html=True)
uploaded_file = st.file_uploader(
    "📤 Upload Resume (PDF only):",
    type=['pdf'],
    help="Upload a PDF resume to extract information"
)
st.markdown('</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    parse_btn = st.button("🔍 Parse Resume with AI")

if parse_btn:
    if uploaded_file is None:
        st.markdown("""
        <div style="text-align:center; color:#f87171; padding:20px;
        background:rgba(239,68,68,0.1); border-radius:15px; margin-top:20px;">
            ⚠️ Please upload a PDF resume first!
        </div>
        """, unsafe_allow_html=True)
    else:
        with st.spinner('🤖 AI is analyzing your resume...'):
            # Extract text
            with pdfplumber.open(uploaded_file) as pdf:
                text = ""
                for page in pdf.pages:
                    text += page.extract_text() or ""

            # Extract info
            name = extract_name(text)
            email = extract_email(text)
            phone = extract_phone(text)
            skills = extract_skills(text)
            education = extract_education(text)
            experience = extract_experience(text)

            # Stats
            st.markdown(f"""
            <div class="stats-row">
                <div class="stat-box">
                    <div class="stat-number">{len(skills)}</div>
                    <div class="stat-label">Skills Found</div>
                </div>
                <div class="stat-box">
                    <div class="stat-number">{len(education)}</div>
                    <div class="stat-label">Education</div>
                </div>
                <div class="stat-box">
                    <div class="stat-number">{len(text.split())}</div>
                    <div class="stat-label">Words Scanned</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Personal Info
            st.markdown(f"""
            <div class="card">
                <div style="color:#34d399; font-size:0.85em; font-weight:600;
                letter-spacing:2px; text-transform:uppercase; margin-bottom:15px;">
                    👤 Personal Information
                </div>
                <div class="info-item">
                    <div class="info-label" style="color:#34d399;">Name</div>
                    <div class="info-value">{name}</div>
                </div>
                <div class="info-item">
                    <div class="info-label" style="color:#60a5fa;">Email</div>
                    <div class="info-value">{email}</div>
                </div>
                <div class="info-item">
                    <div class="info-label" style="color:#f472b6;">Phone</div>
                    <div class="info-value">{phone}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Skills
            if skills:
                skills_html = "".join([f'<span class="skill-tag">{s}</span>' for s in skills])
                st.markdown(f"""
                <div class="card">
                    <div style="color:#60a5fa; font-size:0.85em; font-weight:600;
                    letter-spacing:2px; text-transform:uppercase; margin-bottom:15px;">
                        💻 Skills Detected
                    </div>
                    {skills_html}
                </div>
                """, unsafe_allow_html=True)

            # Education
            edu_html = "".join([f'<div class="info-item"><div class="info-value">{e}</div></div>' for e in education])
            st.markdown(f"""
            <div class="card">
                <div style="color:#f472b6; font-size:0.85em; font-weight:600;
                letter-spacing:2px; text-transform:uppercase; margin-bottom:15px;">
                    🎓 Education
                </div>
                {edu_html}
            </div>
            """, unsafe_allow_html=True)

            # Experience
            exp_html = "".join([f'<div class="info-item"><div class="info-value">{e}</div></div>' for e in experience])
            st.markdown(f"""
            <div class="card">
                <div style="color:#a78bfa; font-size:0.85em; font-weight:600;
                letter-spacing:2px; text-transform:uppercase; margin-bottom:15px;">
                    💼 Experience
                </div>
                {exp_html}
            </div>
            """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    Built with 🐍 Python & 🤖 SpaCy AI<br>
    <span style="color:#34d399; font-weight:600;">
        Akshat Anand — Building intelligent systems that solve real problems
    </span>
</div>
""", unsafe_allow_html=True)