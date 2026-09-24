import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date, datetime, timedelta
import textwrap
import re
import random
import html as html_lib
import hashlib
import json
from pathlib import Path

import os

PDF_CACHE_FILE = "study_pdf_cache.json"


def save_pdf_cache(text, filename, pages=None):
    """Save the uploaded PDF text so it can be reused across pages/sessions."""
    try:
        data = {
            "text": text,
            "filename": filename,
            "pages": pages or []
        }

        with open(PDF_CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)

        return True
    except Exception:
        return False


def load_pdf_cache():
    """Load the last uploaded PDF for Important Questions, Quiz and Chatbot."""
    try:
        if not os.path.exists(PDF_CACHE_FILE):
            return None

        with open(PDF_CACHE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not data.get("text"):
            return None

        return data

    except Exception:
        return None
# ============================================================
# PURPLE + CREAM THEME — STUDY PLANNER
# ============================================================

st.set_page_config(
    page_title="Study Planner",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>

/* =========================
   MAIN BACKGROUND
   ========================= */

.stApp {
    background-color: #FFF8E7;
    color: #4B2E6D;
}

/* Main content area */
.main .block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1200px;
}

/* =========================
   HEADINGS
   ========================= */

h1, h2, h3 {
    color: #4B2E6D !important;
    font-weight: 700;
}

h1 {
    font-size: 2.3rem;
}

h2 {
    font-size: 1.7rem;
}

h3 {
    font-size: 1.3rem;
}

/* Normal text */
p, label, span {
    color: #4B2E6D;
}

/* =========================
   SIDEBAR
   ========================= */

section[data-testid="stSidebar"] {
    background-color: #EDE4F7;
    border-right: 2px solid #D8C8EA;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #4B2E6D !important;
}

/* Sidebar text */
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] label {
    color: #4B2E6D !important;
}

/* =========================
   BUTTONS
   ========================= */

.stButton > button {
    background-color: #7B5CB8;
    color: white;
    border: none;
    border-radius: 10px;
    padding: 0.55rem 1.2rem;
    font-weight: 600;
    transition: 0.2s ease;
}

.stButton > button:hover {
    background-color: #4B2E6D;
    color: white;
    border: none;
}

/* =========================
   INPUT BOXES
   ========================= */

.stTextInput input,
.stTextArea textarea,
.stNumberInput input,
.stDateInput input,
.stTimeInput input,
.stSelectbox div[data-baseweb="select"] {
    background-color: #FFFDF5 !important;
    border: 1.5px solid #C9B4DD !important;
    border-radius: 9px !important;
    color: #4B2E6D !important;
}

/* Input focus */
.stTextInput input:focus,
.stTextArea textarea:focus,
.stNumberInput input:focus {
    border-color: #7B5CB8 !important;
    box-shadow: 0 0 0 1px #7B5CB8 !important;
}

/* =========================
   CARDS
   ========================= */

.study-card {
    background-color: #FFFDF5;
    border: 1px solid #E1D4EC;
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 18px;
    box-shadow: 0 4px 12px rgba(75, 46, 109, 0.08);
}

.study-card:hover {
    box-shadow: 0 6px 18px rgba(75, 46, 109, 0.13);
}

/* =========================
   METRIC CARDS
   ========================= */

div[data-testid="stMetric"] {
    background-color: #FFFDF5;
    border: 1px solid #E1D4EC;
    border-radius: 14px;
    padding: 15px;
    box-shadow: 0 3px 10px rgba(75, 46, 109, 0.08);
}

div[data-testid="stMetricLabel"] {
    color: #6E5487 !important;
}

div[data-testid="stMetricValue"] {
    color: #4B2E6D !important;
}

/* =========================
   TABS
   ========================= */

button[data-baseweb="tab"] {
    color: #6E5487 !important;
    font-weight: 600;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #7B5CB8 !important;
}

/* =========================
   CHECKBOX
   ========================= */

.stCheckbox label {
    color: #4B2E6D !important;
}

/* =========================
   PROGRESS BAR
   ========================= */

.stProgress > div > div > div > div {
    background-color: #7B5CB8;
}

.stProgress > div > div {
    background-color: #E1D4EC;
}

/* =========================
   EXPANDER
   ========================= */

.streamlit-expanderHeader {
    background-color: #F3EAF9 !important;
    color: #4B2E6D !important;
    border-radius: 10px;
    font-weight: 600;
}

details {
    background-color: #FFFDF5;
    border: 1px solid #E1D4EC;
    border-radius: 10px;
}

/* =========================
   ALERT / INFO BOX
   ========================= */

div[data-testid="stAlert"] {
    background-color: #F3EAF9;
    border-radius: 10px;
}

/* =========================
   DIVIDERS
   ========================= */

hr {
    border-color: #DCCCE9;
}

/* =========================
   CUSTOM TITLE
   ========================= */

.study-title {
    color: #4B2E6D;
    font-size: 36px;
    font-weight: 800;
    margin-bottom: 5px;
}

.study-subtitle {
    color: #7B5CB8;
    font-size: 17px;
    margin-bottom: 25px;
}

/* =========================
   CUSTOM BADGES
   ========================= */

.badge {
    display: inline-block;
    background-color: #EDE4F7;
    color: #4B2E6D;
    padding: 6px 12px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 600;
}

</style>
""", unsafe_allow_html=True)
# ============================================================
# HELPERS
# ============================================================

def html(content):
    """Render HTML without Streamlit treating indented HTML as code."""
    content = textwrap.dedent(content).strip()

    # st.html() renders HTML directly in modern Streamlit versions.
    # Keep a fallback for older Streamlit versions.
    if hasattr(st, "html"):
        st.html(content)
    else:
        st.markdown(content, unsafe_allow_html=True)
def inject_css():
    html("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    * {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
    background: #FFF8E7 !important;
    color: #4B2E6D !important;
}

    #MainMenu, footer {
        visibility: hidden;
    }

    /* Force the application UI to stay light */
    [data-testid="stAppViewContainer"],
    [data-testid="stHeader"] {
        background-color: #FFF8E7 !important;
}
    [data-testid="stSidebar"] {
        background-color: #ffffff !important;
    }

    .block-container {
        padding-top: 1.2rem;
        padding-bottom: 2rem;
        max-width: 1450px;
    }
    /* ===== CUSTOM HAMBURGER BUTTON ===== */

[data-testid="collapsedControl"] {
    position: fixed !important;
    top: 8px !important;
    left: 8px !important;
    width: 45px !important;
    height: 45px !important;
    z-index: 999999 !important;
}

[data-testid="collapsedControl"] button {
    width: 45px !important;
    height: 45px !important;
    min-width: 45px !important;
    padding: 0 !important;
    margin: 0 !important;
    border: 0 !important;
    background: transparent !important;
    box-shadow: none !important;
    color: transparent !important;
    font-size: 0 !important;
    position: relative !important;
}

/* Hide Streamlit's original >> icon */
[data-testid="collapsedControl"] button > * {
    display: none !important;
}

/* Our three lines */
[data-testid="collapsedControl"] button::after {
    content: "☰" !important;
    display: block !important;
    color: #111111 !important;
    font-size: 27px !important;
    font-weight: 900 !important;
    line-height: 45px !important;
    text-align: center !important;
}
/* HAMBURGER MENU */

[data-testid="stSidebarCollapsedControl"] {
    position: fixed !important;
    top: 8px !important;
    left: 8px !important;
    z-index: 999999 !important;
}

[data-testid="stSidebarCollapsedControl"] svg {
    display: none !important;
}

[data-testid="stSidebarCollapsedControl"] button {
    width: 45px !important;
    height: 45px !important;
    border: none !important;
    background: white !important;
    border-radius: 10px !important;
    padding: 0 !important;
}

[data-testid="stSidebarCollapsedControl"] button::after {
    content: "☰" !important;
    color: #111 !important;
    font-size: 27px !important;
    font-weight: 900 !important;
}    

    /* ========================================================
       LOGIN THEME
       ======================================================== */

    .auth-page {
        min-height: 92vh;
        position: relative;
        padding: 28px 20px 35px;
        overflow: hidden;
    }

    .auth-page:before,
    .auth-page:after {
        content: "";
        position: absolute;
        border-radius: 50%;
        filter: blur(2px);
        pointer-events: none;
    }

    .auth-page:before {
        width: 360px;
        height: 360px;
        left: -120px;
        top: -100px;
        background: rgba(163,139,255,.35);
    }

    .auth-page:after {
        width: 420px;
        height: 420px;
        right: -130px;
        bottom: -160px;
        background: rgba(106,205,255,.32);
    }

    .auth-heading {
        text-align: center;
        position: relative;
        z-index: 2;
        margin-bottom: 20px;
    }

    .auth-brand {
        color: #28266e;
        font-size: 30px;
        font-weight: 800;
        letter-spacing: -.5px;
    }

    .auth-brand span {
        color: #6855ed;
    }

    .auth-caption {
        color: #7475a2;
        font-size: 13px;
        margin-top: 4px;
    }

    .auth-grid {
        position: relative;
        z-index: 2;
        display: grid;
        grid-template-columns: repeat(2, minmax(310px, 430px));
        justify-content: center;
        gap: 48px;
        align-items: stretch;
    }

    .auth-panel {
        position: relative;
        min-height: 650px;
        overflow: hidden;
        border-radius: 42px;
        background: rgba(255,255,255,.90);
        border: 10px solid rgba(255,255,255,.42);
        box-shadow:
            0 35px 80px rgba(78,67,170,.20),
            0 8px 25px rgba(79,70,229,.10);
        backdrop-filter: blur(12px);
    }

    .auth-panel:before {
        content: "";
        position: absolute;
        width: 120%;
        height: 145px;
        left: -10%;
        top: -62px;
        background: linear-gradient(145deg, #ffffff 20%, #e5dcff 55%, #5b46ed 100%);
        border-radius: 0 0 65% 55%;
        transform: rotate(-2deg);
    }

    .auth-panel:after {
        content: "";
        position: absolute;
        width: 120%;
        height: 150px;
        left: -10%;
        bottom: -80px;
        background: linear-gradient(145deg, #6247ed, #9c8cff, #ffffff);
        border-radius: 55% 55% 0 0;
        transform: rotate(-2deg);
    }

    .auth-panel-inner {
        position: relative;
        z-index: 3;
        padding: 32px 36px 42px;
        min-height: 650px;
    }

    .social-row {
        display: flex;
        gap: 10px;
        margin-bottom: 54px;
    }

    .social-pill {
        flex: 1;
        background: rgba(255,255,255,.82);
        border: 1px solid #e5e4f6;
        border-radius: 25px;
        padding: 9px 10px;
        text-align: center;
        color: #5d5d91;
        font-size: 11px;
        font-weight: 700;
        box-shadow: 0 5px 14px rgba(70,60,160,.06);
    }

    .social-pill.google {
        color: #4285f4;
    }

    .social-pill.facebook {
        color: #1877f2;
    }

    .auth-top-title {
        font-size: 25px;
        font-weight: 800;
        color: #252452;
        margin-bottom: 3px;
    }

    .auth-top-title span {
        color: #6651e9;
    }

    .auth-small {
        color: #8585a7;
        font-size: 11px;
        margin-bottom: 18px;
    }

    .robot-wrap {
        text-align: center;
        margin: 12px 0 24px;
    }

    .robot {
        display: inline-flex;
        width: 100px;
        height: 78px;
        align-items: center;
        justify-content: center;
        border-radius: 45% 45% 38% 38%;
        background: linear-gradient(145deg, #ffffff, #d9d3ff);
        box-shadow: 0 14px 25px rgba(84,69,210,.18);
        font-size: 45px;
        position: relative;
    }

    .robot:before {
        content: "";
        position: absolute;
        width: 4px;
        height: 15px;
        top: -12px;
        left: 48px;
        background: #6855ed;
        border-radius: 5px;
    }

    .robot:after {
        content: "✦";
        position: absolute;
        top: -27px;
        left: 43px;
        color: #6855ed;
        font-size: 15px;
    }

    .hello-bubble {
        display: inline-block;
        position: relative;
        top: -20px;
        margin-left: -8px;
        padding: 6px 10px;
        border-radius: 12px;
        background: #eeeaff;
        color: #6651e9;
        font-size: 11px;
        font-weight: 800;
    }

    .auth-input-label {
        color: #a1a1bd;
        font-size: 10px;
        margin-top: 13px;
        margin-bottom: 3px;
    }

    .auth-note {
        text-align: right;
        color: #8c86bd;
        font-size: 10px;
        margin-top: -2px;
        margin-bottom: 10px;
    }

    .arrow-button > button {
        display: block;
        width: 55px !important;
        height: 55px !important;
        min-height: 55px !important;
        margin: 12px auto 15px !important;
        border-radius: 50% !important;
        border: 7px solid #f0efff !important;
        background: linear-gradient(145deg, #513be5, #7857ff) !important;
        color: white !important;
        font-size: 22px !important;
        box-shadow: 0 10px 24px rgba(87,66,224,.35) !important;
        padding: 0 !important;
    }

    .arrow-button > button:hover {
        transform: translateY(-2px);
    }

    .auth-bottom-text {
        position: absolute;
        z-index: 4;
        left: 36px;
        bottom: 34px;
    }

    .auth-bottom-title {
        font-size: 19px;
        color: #24224f;
        font-weight: 800;
    }

    .auth-bottom-sub {
        color: #756eaa;
        font-size: 10px;
        margin-top: 3px;
    }

    .bottom-social {
        position: absolute;
        z-index: 5;
        left: 34px;
        right: 34px;
        bottom: 26px;
        display: flex;
        gap: 10px;
    }

    .bottom-social .social-pill {
        background: rgba(255,255,255,.88);
    }

    /* Streamlit form inputs */
    .auth-panel .stTextInput input {
        border: none !important;
        border-bottom: 1px solid #dedff0 !important;
        border-radius: 0 !important;
        background: transparent !important;
        padding-left: 2px !important;
        font-size: 12px !important;
        color: #292754 !important;
        box-shadow: none !important;
    }

    .auth-panel .stTextInput label {
        font-size: 10px !important;
        color: #a0a0ba !important;
    }

    .auth-panel .stTextInput input:focus {
        border-bottom: 2px solid #6955ed !important;
    }

    /* ========================================================
       APP THEME
       ======================================================== */

    .app-shell {
        background: rgba(255,255,255,.40);
        border-radius: 30px;
        padding: 18px;
    }

    .topbar {
        background: rgba(255,255,255,.88);
        border-radius: 24px;
        padding: 15px 22px;
        box-shadow: 0 10px 30px rgba(71,64,150,.08);
        border: 1px solid rgba(255,255,255,.8);
        margin-bottom: 20px;
    }

    .brand {
        font-size: 22px;
        font-weight: 800;
        color: #28265e;
    }

    .brand span {
        color: #6855ed;
    }

    .hero {
        border-radius: 28px;
        padding: 28px;
        background:
            radial-gradient(circle at 80% 0%, rgba(255,255,255,.30), transparent 28%),
            linear-gradient(135deg, #5942e8, #7955ee 55%, #9c79f5);
        color: white;
        box-shadow: 0 20px 40px rgba(91,66,224,.23);
        margin-bottom: 20px;
    }

    .hero h1 {
        margin: 0;
        font-size: 30px;
        font-weight: 800;
    }

    .hero p {
        margin: 7px 0 0;
        opacity: .88;
        font-size: 13px;
    }

    .stat-card {
        background: #FFFDF5;
        border-radius: 22px;
        padding: 19px;
        border: 1px solid rgba(220,220,242,.85);
        box-shadow: 0 12px 28px rgba(62,55,145,.08);
        min-height: 125px;
    }

    .stat-icon {
        font-size: 25px;
    }

    .stat-label {
        color: #8888a7;
        font-size: 11px;
        margin-top: 7px;
    }

    .stat-value {
        color: #29275b;
        font-size: 25px;
        font-weight: 800;
        margin-top: 3px;
    }

    .section-heading {
        font-size: 20px;
        color: #28265b;
        font-weight: 800;
        margin: 24px 0 12px;
    }

    .glass-card {
        background: rgba(255,255,255,.90);
        border-radius: 20px;
        padding: 18px;
        border: 1px solid #e6e5f2;
        box-shadow: 0 10px 24px rgba(62,55,145,.06);
        margin-bottom: 12px;
    }

    .card-title {
        font-size: 16px;
        font-weight: 800;
        color: #302e62;
    }

    .card-text {
        color: #8888a6;
        font-size: 12px;
        margin-top: 5px;
    }

    .card-meta {
        color: #6755e8;
        font-size: 11px;
        font-weight: 700;
        margin-top: 9px;
    }

    .chat-user {
        max-width: 78%;
        margin: 10px 0 10px auto;
        padding: 13px 17px;
        border-radius: 18px 18px 5px 18px;
        color: white;
        background: linear-gradient(135deg, #5942e8, #7955ee);
        box-shadow: 0 8px 18px rgba(89,66,232,.15);
    }

    .chat-bot {
        max-width: 82%;
        margin: 10px 0;
        padding: 14px 17px;
        border-radius: 18px 18px 18px 5px;
        color: #3d3b69;
        
        border: 1px solid #e3e2ef;
        box-shadow: 0 8px 18px rgba(62,55,145,.06);
    }

    .stButton > button {
        border-radius: 13px;
        font-weight: 700;
        border: 1px solid #deddf0;
    }

    .stButton > button:hover {
        border-color: #7560ef;
        color: #5d48dd;
    }

    [data-testid="stMetric"] {
        background: rgba(255,255,255,.88);
        padding: 15px;
        border-radius: 18px;
        border: 1px solid #e5e4f0;
    }

    /* ========================================================
       DASHBOARD CARDS
       ======================================================== */

    .page-title {
        font-size: 25px;
        font-weight: 800;
        color: #28265e;
        margin-top: 5px;
    }

    .page-subtitle {
        color: #77779b;
        font-size: 12px;
        margin-bottom: 18px;
    }

    .welcome-box {
        background: rgba(255,255,255,.90);
        border-radius: 22px;
        padding: 22px 26px;
        border: 1px solid #e5e4f0;
        box-shadow: 0 10px 25px rgba(62,55,145,.06);
        margin-bottom: 12px;
    }

    .welcome-box h2 {
        margin: 0;
        color: #29265f;
        font-size: 21px;
        font-weight: 800;
    }

    .welcome-box p {
        margin: 8px 0 0;
        color: #8888a6;
        font-size: 12px;
    }

    .metric-card {
        background: #FFFDF5;
        border-radius: 18px;
        padding: 17px;
        border: 1px solid #e5e4f0;
        box-shadow: 0 10px 24px rgba(62,55,145,.07);
        min-height: 105px;
        margin-bottom: 10px;
    }

    .metric-icon {
        font-size: 21px;
    }

    .metric-title {
        color: #8888a7;
        font-size: 11px;
        margin-top: 5px;
    }

    .metric-value {
        color: #29275b;
        font-size: 22px;
        font-weight: 800;
        margin-top: 3px;
    }

    .section-title {
        color: #302e62;
        font-size: 17px;
        font-weight: 800;
        margin: 20px 0 10px;
    }

    .session-card {
        background: rgba(255,255,255,.90);
        border-radius: 18px;
        padding: 16px 18px;
        border: 1px solid #e5e4f0;
        box-shadow: 0 8px 20px rgba(62,55,145,.06);
        margin-bottom: 10px;
    }

    .session-subject {
        color: #302e62;
        font-size: 15px;
        font-weight: 800;
    }

    .session-topic {
        color: #77779b;
        font-size: 12px;
        margin-top: 5px;
    }

    .session-meta {
        color: #6755e8;
        font-size: 11px;
        font-weight: 700;
        margin-top: 8px;
    }

    .subject-card {
        background: rgba(255,255,255,.90);
        border-radius: 18px;
        padding: 16px 18px;
        border: 1px solid #e5e4f0;
        box-shadow: 0 8px 20px rgba(62,55,145,.06);
        margin-bottom: 6px;
    }

    .subject-name {
        color: #302e62;
        font-size: 15px;
        font-weight: 800;
    }

    .subject-info {
        color: #8888a6;
        font-size: 11px;
        margin-top: 5px;
    }

    /* ========================================================
       MOBILE
       ======================================================== */

    @media (max-width: 900px) {
        .auth-grid {
            grid-template-columns: minmax(280px, 430px);
            gap: 25px;
        }

        .auth-panel {
            min-height: 600px;
        }

        .auth-panel-inner {
            min-height: 600px;
        }
    }
    </style>
    """)


# ============================================================
# LATEST STUDY FEATURES - LOCAL / NO API

def init_feature_state():
    defaults={
        "pdf_text":"","pdf_name":"","pdf_pages":[],"pdf_summary":"","pdf_quiz":[],
        "quiz_answers":{},"quiz_submitted":False,"quiz_score":0,
        "achievements":[],"notes":[],"important_questions":[],"saved_important":[],"ai_mode":"Explain",
        "pomodoro_count":0,"pomodoro_minutes":0,"study_goals":[],"mistake_review":[],
        "smart_schedule":[],"daily_goal_minutes":120,"goal_date":date.today(),
        "last_pdf_quiz_name":"",
        "quiz_id":0,"pdf_sig":"","quiz_source":"","important_source":"","important_offset":0
    }
    for k,v in defaults.items():
        if k not in st.session_state: st.session_state[k]=v

def award(name,icon,description):
    if name not in [a["name"] for a in st.session_state.achievements]: st.session_state.achievements.append({"name":name,"icon":icon,"description":description})

def create_pdf_summary(text, max_points=12):
    """Create a clean offline summary from meaningful PDF content."""

    if not text:
        return ""

    raw_lines = re.split(r"\n+", text)

    cleaned_lines = []

    for raw in raw_lines:

        line = re.sub(
            r"\s+",
            " ",
            raw
        ).strip()

        if not line:
            continue

        # Remove file-system paths
        if re.search(
            r"(/Users/|/home/|C:\\|D:\\|site-packages|python3\.\d+)",
            line,
            re.IGNORECASE
        ):
            continue

        # Remove obvious PDF extraction noise
        if re.search(
            r"miniconda|site-packages|IPython/extensions",
            line,
            re.IGNORECASE
        ):
            continue

        # Remove broken bullet-only lines
        if re.fullmatch(
            r"[•●▪\-–—\s]+",
            line
        ):
            continue

        # Remove very short headings
        if len(line.split()) < 6:
            continue

        cleaned_lines.append(line)

    if not cleaned_lines:
        return ""

    # Join lines and split into sentences.
    cleaned_text = " ".join(cleaned_lines)

    sentences = re.split(
        r"(?<=[.!?])\s+",
        cleaned_text
    )

    sentences = [
        re.sub(r"\s+", " ", s).strip()
        for s in sentences
        if len(s.split()) >= 8
    ]

    if not sentences:
        return ""

    # Remove duplicates.
    unique = []
    seen = set()

    for sentence in sentences:

        key = re.sub(
            r"[^a-z0-9]+",
            " ",
            sentence.lower()
        ).strip()

        if key in seen:
            continue

        seen.add(key)
        unique.append(sentence)

    # Select useful study sentences.
    study_words = {
        "python",
        "function",
        "variable",
        "list",
        "tuple",
        "dictionary",
        "class",
        "object",
        "loop",
        "string",
        "exception",
        "file",
        "module",
        "regular",
        "expression",
        "programming",
        "method",
        "data",
        "type"
    }

    scored = []

    for i, sentence in enumerate(unique):

        words = re.findall(
            r"[A-Za-z][A-Za-z0-9_]*",
            sentence.lower()
        )

        score = sum(
            1
            for word in words
            if word in study_words
        )

        # Prefer informative sentences.
        score += min(len(words) / 20, 2)

        scored.append(
            (score, i, sentence)
        )

    scored.sort(
        key=lambda x: x[0],
        reverse=True
    )

    selected = scored[:max_points]

    # Restore PDF/source order.
    selected.sort(
        key=lambda x: x[1]
    )

    return "\n".join(
        f"• {sentence}"
        for _, _, sentence in selected
    )

    # Score sentences by useful study terms and length, then preserve source order.
    stop = {"this","that","these","those","there","their","about","which","where","when","what","from","with","into","have","has","been","were","will","would","could","should","than","then","they","them","also","such","using","used","each","more","most","some","many","very","only","other","over","under"}
    scored=[]
    for i, sent in enumerate(sentences):
        words=re.findall(r"[A-Za-z][A-Za-z0-9_-]{2,}", sent.lower())
        freq={w:words.count(w) for w in set(words) if w not in stop}
        score=sum(freq.values()) + min(len(words), 35)*0.08
        scored.append((score,i,sent))
    # Keep a larger pool so the Regenerate button can produce another
    # valid source-grounded summary instead of returning the exact same text.
    pool_size = min(len(scored), max_points * 2)
    ranked = sorted(scored, reverse=True)[:pool_size]
    if len(ranked) > max_points:
        chosen = random.sample(ranked, max_points)
    else:
        chosen = ranked
    chosen = sorted(chosen, key=lambda z:z[1])
    return "\n".join(f"• {sent}" for _,_,sent in chosen)


# ============================================================
# PDF STUDY ENGINE  (Important Questions + Quiz)
# ------------------------------------------------------------
# One shared parser turns the PDF text into sections and "facts"
# (question + answer + source). Both the Important Questions page
# and the Quiz page are built from the same facts, so an answer
# shown on one page always agrees with the other.
#
# Rules that keep answers correct:
#   * an answer is always copied from the PDF (never invented)
#   * a question is dropped if no well-matched answer is found
#   * code, exercises, page headers and question lists are never
#     used as answers
# ============================================================
import math
import unicodedata
from functools import lru_cache

_SG_KW = {
    "if", "for", "while", "else", "elif", "try", "except", "finally", "with",
    "import", "return", "def", "class", "lambda", "break", "continue", "pass",
}
_SG_KW_NOUN = {"loop", "loops", "statement", "statements", "block", "blocks",
               "keyword", "keywords", "clause", "expression", "expressions"}

_SG_STOP = set("""
a an the of in on at to and or but then so as by from into onto over under about after before
is are was were be been being am do does did done have has had will would can could should shall
may might must this that these those it its they them their there here we you your i he she his
her our not no nor also just very more most some any each every all both either neither such than
which who whom whose what when where why how
""".split())

# words that carry no meaning inside a *question*
_SG_Q_DROP = _SG_STOP | set("""
difference differences between purpose main important key basic briefly short following one two
three four five six seven eight nine ten example examples use uses used using work works meaning role
""".split())

_SG_SMALL = {"a", "an", "the", "of", "in", "on", "at", "to", "for", "and", "or",
             "with", "vs", "by", "from", "as", "&"}

_SG_VERBISH = {
    "is", "are", "was", "were", "be", "been", "can", "could", "will", "would",
    "should", "must", "may", "might", "has", "have", "had", "does", "do", "did",
    "uses", "use", "used", "using", "allows", "helps", "means", "contains",
    "stores", "returns", "makes", "lets", "gets", "gives", "give", "takes",
}

_SG_BAD_SUBJ_FIRST = {
    "this", "that", "it", "these", "those", "there", "here", "they", "we", "you", "i", "he",
    "she", "in", "on", "at", "for", "to", "of", "by", "with", "if", "when", "because",
    "however", "also", "then", "so", "but", "and", "or", "note", "since", "as", "after",
    "before", "each", "every", "some", "any", "most", "many", "all", "both", "either",
    "neither", "such", "which", "who", "what", "how", "why", "where", "not", "no", "can",
    "will", "should", "must", "may", "while", "using", "use", "example", "for-example",
    "first", "second", "third", "next", "finally", "another", "other", "our", "your", "its",
    "their", "his", "her", "one", "two", "three", "four", "five", "whenever", "unless",
    "although", "though", "once", "until", "like", "unlike",
}
_SG_BAD_SUBJ_TOKENS = {
    "of", "in", "on", "at", "by", "with", "between", "or", "to", "from", "when", "if", "that",
    "which", "because", "while", "can", "will", "should", "must", "may", "also", "only", "not",
    "you", "we", "your", "our", "i", "it", "they", "there", "then", "than", "so", "but", "how",
    "what", "why", "who", "where", "do", "does", "did", "has", "have", "had", "was", "were",
    "be", "been", "using", "used", "use", "uses",
}
_SG_BAD_REST_FIRST = {
    "not", "also", "only", "often", "usually", "sometimes", "always", "very", "then", "case",
    "shown", "given", "listed", "written", "below", "above", "here", "there", "stored",
    "printed", "displayed", "followed", "called", "named", "true", "false", "used", "because",
    "when", "if", "either", "neither", "both", "just", "still", "even", "now", "again",
}

_SG_LABEL = re.compile(
    r"^(?:example|examples|output|input|syntax|note|tip|tips|result|results|code|program|"
    r"solution|sample|sample output|expected output|explanation|remember|warning|hint)"
    r"\s*[:\-]?\s*(.*)$", re.I)

_SG_SKIP_HEAD = re.compile(
    r"challenge|exercise|try (?:these|it|this)|testing|test (?:case|question)|"
    r"table of contents|^contents$|^index$|homework|assignment|"
    r"practice (?:question|problem|exercise|set)|bibliograph|^references?$|"
    r"acknowledg|answer key|mini project|lab work|quiz feature|chatbot",
    re.I)
_SG_QSEC_HEAD = re.compile(r"question|q\s*&\s*a|viva|faq|revision", re.I)

_SG_GENERIC_HEAD = {
    "introduction", "overview", "summary", "conclusion", "contents", "basics", "notes",
    "references", "example", "examples", "appendix", "preface", "chapter", "unit", "part",
    "topic", "lesson", "agenda", "objectives", "objective", "study guide", "getting started",
    "title", "abstract", "about", "welcome", "recap", "revision",
}
_SG_IMPERATIVE_HEAD = {
    "install", "open", "create", "run", "write", "use", "print", "enter", "click", "type",
    "save", "add", "define", "import", "call", "try", "make", "build", "set", "check",
    "read", "download", "start", "select", "follow", "remember", "learn", "practice",
}

_SG_BULLET = re.compile(
    r"^\s*(?:[\u2022\u25cf\u25aa\u25e6\u2023\u25b6\u25ba\u25a0\u25a1\u25cb\uf0b7\uf0a7\uf076"
    r"\-\u2013\u2014*])\s+")

_SG_QWORD = (r"what|why|how|when|where|who|which|explain|define|describe|list|compare|"
             r"differentiate|distinguish|name|state|identify|discuss|mention|give|outline|"
             r"enumerate|justify|illustrate|summari[sz]e")
_SG_IMPERATIVES = {"explain", "define", "describe", "list", "compare", "differentiate",
                   "distinguish", "name", "state", "identify", "discuss", "mention", "give",
                   "outline", "enumerate", "justify", "illustrate", "summarize", "summarise"}

_SG_DEF_RE = re.compile(
    r"^(?P<subj>[A-Za-z_][A-Za-z0-9_'\-/ ]{0,48}?)\s+"
    r"(?P<verb>is defined as|are defined as|refers to|refer to|means|is used to|is used for|"
    r"are used to|are used for|is|are|stores|store|holds|hold|contains|contain|returns|"
    r"represents|represent|provides|provide|allows|allow|helps|help|creates|create|defines|"
    r"handles|handle)\s+(?P<rest>\S.*)$")

_SG_TERM_RE = re.compile(
    r"^(?P<term>[A-Za-z_][A-Za-z0-9_ /'\-]{0,38}?)\s*(?::|\u2013|\u2014|\s-\s)\s*"
    r"(?P<defn>\S.{1,})$")


# ------------------------------------------------------------
# small text helpers
# ------------------------------------------------------------
def _sg_stem(word):
    w = word.lower().strip("'-_")
    if len(w) > 4 and w.endswith("ies"):
        w = w[:-3] + "y"
    elif len(w) > 4 and w.endswith("es") and w[-3] in "sxz":
        w = w[:-2]
    elif len(w) > 3 and w.endswith("s") and not w.endswith("ss"):
        w = w[:-1]
    if len(w) > 5 and w.endswith("ing"):
        w = w[:-3]
        if len(w) >= 3 and w[-1] == w[-2] and w[-1] not in "lsz":
            w = w[:-1]
    elif len(w) > 4 and w.endswith("ied"):
        w = w[:-3] + "y"
    elif len(w) > 4 and w.endswith("ed"):
        w = w[:-2]
        if len(w) >= 3 and w[-1] == w[-2] and w[-1] not in "lsz":
            w = w[:-1]
    if len(w) > 3 and w.endswith("e"):
        w = w[:-1]
    return w


def _sg_words(text):
    return re.findall(r"[A-Za-z][A-Za-z0-9_'\-]*", text or "")


def _sg_keys(text, drop=_SG_Q_DROP):
    out = []
    for w in _sg_words(text):
        lw = w.lower()
        if lw in _SG_KW or (lw not in drop and len(lw) > 1):
            out.append(_sg_stem(lw))
    return out


def _sg_sentences(text):
    text = re.sub(r"\b(e\.g|i\.e|etc|vs|fig|mr|mrs|dr|approx|no)\.",
                  lambda m: m.group(0).replace(".", "\u00a7"), text, flags=re.I)
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9\"'(])", text)
    return [p.replace("\u00a7", ".").strip() for p in parts if p.strip()]


def _sg_cap(text):
    text = (text or "").strip()
    return text[:1].upper() + text[1:] if text else text


def _sg_trim_end(text):
    return re.sub(r"[\s.;:,]+$", "", (text or "").strip())


def _sg_wc(text):
    return len((text or "").split())


def _sg_jaccard(a, b):
    sa, sb = set(_sg_keys(a, _SG_STOP)), set(_sg_keys(b, _SG_STOP))
    if not sa or not sb:
        return 0.0
    return len(sa & sb) / len(sa | sb)


# ------------------------------------------------------------
# line classification
# ------------------------------------------------------------
def _sg_is_code(line):
    s = line.strip()
    if not s:
        return False
    if re.match(r"^(>>>|\.\.\.|\$\s|#|//|/\*|\*/|@\w+)", s):
        return True
    if re.match(r"^import\s+[\w.]+(?:\s+as\s+\w+)?(?:\s*,\s*[\w.]+)*$", s):
        return True
    if re.match(r"^from\s+[\w.]+\s+import\s+.+$", s):
        return True
    if re.match(r"^(?:for|while|if|elif|else|try|except|finally|def|class|with)\b.*:\s*$", s):
        return True
    if re.match(r"^(?:else|try|finally)\s*:$", s):
        return True
    if re.match(r"^(?:return|raise|assert|break|continue|pass|del|yield|global|lambda)\b(?!\s+[a-z]+\s+[a-z]+\s+[a-z]+)", s):
        return True
    if re.match(r"^[A-Za-z_][\w.]*\(.*\)\s*$", s):
        return True
    if re.match(r"^[A-Za-z_][\w.\[\]\"']*\s*(?:[+\-*/%]|//|\*\*)?=(?!=)\s*\S", s):
        return True
    if re.match(r"^[\[\{(].*[\]\})]$", s) and len(s.split()) < 12:
        return True
    if re.match(r"^[\]\}\)]+,?$", s):
        return True
    if re.match(r"^f[\"']", s):
        return True
    if re.search(r"\S\s*(?:==|!=|<=|>=)\s*\S", s) and _sg_wc(s) < 8:
        return True
    symbols = sum(1 for c in s if c in "{}[]()=<>_;\\|`")
    if len(s) > 3 and symbols / len(s) > 0.18 and _sg_wc(s) < 9:
        return True
    return False


def _sg_question_from_line(line, in_qsection):
    """Return (question, inline_answer) when the line is a question, else None."""
    s = _SG_BULLET.sub("", line.strip())
    numbered = False
    m = re.match(r"^(?:q(?:uestion)?\s*)?\d{1,3}\s*[.):\-]\s*(.*)$", s, re.I)
    if m:
        numbered, s = True, m.group(1)
    else:
        m = re.match(r"^q(?:uestion)?\s*[:\-]\s*(.*)$", s, re.I)
        if m:
            numbered, s = True, m.group(1)
    core = s.strip()
    if not core:
        return None
    m = re.match(r"^(" + _SG_QWORD + r")\b", core, re.I)
    if not m:
        if (in_qsection and 3 <= _sg_wc(core) <= 18
                and re.match(r"^differences?\s+between\b", core, re.I)):
            return ("What is the " + core[0].lower() + core[1:].rstrip(".?") + "?", "")
        return None
    if re.search(r"[A-Za-z_]\w*\s*=(?!=)", core):
        return None
    first = m.group(1).lower()
    if "?" in core:
        q, _, tail = core.partition("?")
        q = q.strip() + "?"
        if _sg_wc(q) < 3:
            return None
        tail = tail.strip()
        return (q, tail if _sg_wc(tail) >= 5 else "")
    if first in _SG_IMPERATIVES and (in_qsection or (numbered and not core.endswith("."))):
        if 3 <= _sg_wc(core) <= 25:
            return (core.rstrip(".") + ".", "")
    if in_qsection and 3 <= _sg_wc(core) <= 25 and not core.endswith("."):
        return (core.rstrip(".") + "?", "")
    return None


def _sg_heading_text(line, prev_kind, prev_text, nxt):
    t = line.strip()
    if len(t) > 80 or len(t) < 2 or _SG_BULLET.match(t):
        return None
    m = re.match(r"^(\d{1,2}(?:\.\d{1,2}){0,2})[.)]?\s+(.+)$", t)
    numbered = bool(m)
    core = (m.group(2) if m else t).strip()
    core = re.sub(r"\s*:\s*$", "", core)
    if not core or re.search(r"[.!?;,]$", core):
        return None
    words = core.split()
    if not 1 <= len(words) <= 9:
        return None
    if not (core[0].isupper() or core[0].isdigit()):
        return None
    if re.match(r"^(" + _SG_QWORD + r")\b", core, re.I):
        return None
    if re.search(r"[=(){}\[\]<>]", core):
        return None
    lw = [w.lower().strip("(),") for w in words]
    if any(w in _SG_VERBISH for w in lw):
        return None
    mid_sentence = prev_kind == "prose" and not re.search(r"[.!?:]$", prev_text or "")
    if mid_sentence and _sg_wc(prev_text) > 10:
        return None                      # previous prose line is still mid-sentence
    big = [w for w in words if w.lower() not in _SG_SMALL]
    ratio = sum(1 for w in big if w[0].isupper() or w[0].isdigit() or w.isupper()) / max(1, len(big))
    if mid_sentence:
        return core if (ratio >= 0.99 and len(words) >= 2) or _SG_SKIP_HEAD.search(core) else None
    if ratio >= 0.6 or numbered or (_SG_SKIP_HEAD.search(core) and len(words) <= 7):
        return core
    if len(words) <= 4 and nxt and _sg_wc(nxt) >= 5 and nxt[0].isupper():
        return core
    return None


# ------------------------------------------------------------
# PDF text -> clean lines
# ------------------------------------------------------------
_SG_PAGE_TAIL = re.compile(
    r"(?:^|\s)[\-\u2013\u2014\u2022|\u00b7]?\s*(?:page|pg\.?|p\.)\s*\d+(?:\s*(?:of|/)\s*\d+)?\s*$", re.I)


def _sg_clean_lines(text):
    text = unicodedata.normalize("NFKC", text or "")
    text = text.replace("\r", "\n").replace("\x0c", "\n").replace("\u00ad", "")
    # bullet glyphs often come out of PDFs as control / private-use characters
    _junk = "[\x00-\x08\x0b-\x1f\x7f\ue000-\uf8ff\ufffd]+"
    text = "\n".join(re.sub(_junk, " ", re.sub(r"^\s*" + _junk + r"\s*", "\u2022 ", l))
                     for l in text.split("\n"))
    raw = [re.sub(r"[ \t\u00a0]+", " ", l).strip() for l in text.split("\n")]
    raw = [l for l in raw if l]

    merged, i = [], 0
    while i < len(raw):
        if re.fullmatch(r"[\u2022\u25cf\u25aa\u25e6\u2023\uf0b7\uf0a7*]", raw[i]) and i + 1 < len(raw):
            merged.append("\u2022 " + raw[i + 1])
            i += 2
        else:
            merged.append(raw[i])
            i += 1
    raw = merged

    stripped = []
    for l in raw:
        base = _SG_PAGE_TAIL.sub("", l).strip()
        stripped.append(base if base else l)

    counts = {}
    for l in stripped:
        if _sg_wc(l) <= 8:
            counts[l.lower()] = counts.get(l.lower(), 0) + 1
    headers = {k for k, v in counts.items()
               if v >= 3 and not _SG_LABEL.match(k) and not _SG_BULLET.match(k) and not _sg_is_code(k)
               and not re.search(r"[.!?]$", k)}
    if stripped and _sg_wc(stripped[0]) <= 8 and counts.get(stripped[0].lower(), 0) >= 2:
        headers.add(stripped[0].lower())

    out = []
    for orig, l in zip(raw, stripped):
        low = l.lower()
        if low in headers:
            continue
        for h in headers:
            if _sg_wc(h) >= 2 and h in low and low != h:
                l = re.sub(r"\s*[\u2022\-\u2013\u2014|\u00b7]?\s*" + re.escape(h) + r"\s*", " ", l,
                           flags=re.I).strip()
                low = l.lower()
        if not l or re.fullmatch(r"(?:page\s*)?\d{1,4}(?:\s*of\s*\d{1,4})?", l, re.I):
            continue
        if re.fullmatch(r"[\-\u2013\u2014_=\u2022.\s]{2,}", l):
            continue
        out.append(l)
    return out


# ------------------------------------------------------------
# lines -> sections -> blocks
# ------------------------------------------------------------
def _sg_parse(text):
    lines = _sg_clean_lines(text)
    n = len(lines)
    sections = []
    cur = {"heading": "", "skip": False, "qsec": False, "blocks": []}
    state = {"open": None, "prev": "start", "prev_text": ""}

    def new_section(h):
        nonlocal cur
        if cur["blocks"]:
            sections.append(cur)
        cur = {"heading": h, "skip": bool(_SG_SKIP_HEAD.search(h)),
               "qsec": bool(_SG_QSEC_HEAD.search(h)), "blocks": []}
        state["open"] = None

    def add_block(btype, txt, **extra):
        b = {"type": btype, "text": txt}
        b.update(extra)
        cur["blocks"].append(b)
        state["open"] = b
        return b

    for i, line in enumerate(lines):
        nxt = lines[i + 1] if i + 1 < n else ""
        state["prev_text"] = lines[i - 1] if i else ""

        m = _SG_LABEL.match(line)
        if m and (not m.group(1) or len(line.split()) <= 3 or line.lower().startswith(
                ("example", "output", "input", "syntax", "sample", "expected"))):
            state["open"], state["prev"] = None, "label"
            continue

        if _sg_is_code(line):
            state["open"], state["prev"] = None, "code"
            continue

        am = re.match(r"^(?:answer|ans)\s*[:\-.]\s*(.*)$", line, re.I)
        if am:
            if not cur["skip"]:
                add_block("answer", am.group(1).strip())
            state["prev"] = "answer"
            continue

        q = _sg_question_from_line(line, cur["qsec"])
        if q:
            if not cur["skip"]:
                add_block("question", q[0], inline=q[1])
            state["open"], state["prev"] = None, "question"
            continue

        h = _sg_heading_text(line, state["prev"], state["prev_text"], nxt)
        if h:
            new_section(h)
            state["prev"] = "heading"
            continue

        if cur["skip"]:
            state["prev"] = "prose"
            continue

        if _SG_BULLET.match(line):
            add_block("bullet", _SG_BULLET.sub("", line).strip())
            state["prev"] = "bullet"
            continue

        # "term - meaning" lines are list items even when the PDF lost the bullet symbol
        if _sg_wc(line) <= 16 and _SG_TERM_RE.match(line) and _sg_term_fact(line, min_words=1):
            add_block("bullet", line)
            state["prev"] = "bullet"
            continue

        open_b = state["open"]
        ends = bool(open_b) and bool(re.search(r"[.!?:]$", open_b["text"]))
        if open_b and open_b["type"] in ("prose", "bullet", "answer") and (
                not ends and (open_b["type"] != "bullet" or line[:1].islower()
                              or open_b["text"].endswith((",", "-", " and", " or")))
                or line[:1].islower()):
            if open_b["text"].endswith("-") and line[:1].islower():
                open_b["text"] += line
            else:
                open_b["text"] += " " + line
        else:
            add_block("prose", line)
        state["prev"] = "prose"

    if cur["blocks"]:
        sections.append(cur)
    return sections


# ------------------------------------------------------------
# fact extraction
# ------------------------------------------------------------
def _sg_clean_subject(subj, lower_vocab, first_in_block, sentence_upper):
    toks = subj.strip().split()
    if not 1 <= len(toks) <= 5:
        return None
    article = ""
    if toks[0].lower() in ("a", "an", "the"):
        article = toks[0].lower()
        toks = toks[1:]
    if not toks:
        return None
    low = [t.lower() for t in toks]
    if low[0] in _SG_BAD_SUBJ_FIRST:
        kw_ok = (low[0] in _SG_KW and len(low) >= 2 and low[-1] in _SG_KW_NOUN)
        if not kw_ok:
            return None
    for t in low[1:] if low[0] in _SG_KW else low:
        if t in _SG_BAD_SUBJ_TOKENS:
            return None
    if any(t.endswith("ly") for t in low) or re.fullmatch(r"[\d\W_]+", " ".join(toks)):
        return None
    if len(toks) == 1 and len(toks[0]) < 2:
        return None
    if not sentence_upper and not first_in_block:
        return None
    if toks[0][0].isupper() and not article and low[0] in lower_vocab and not toks[0].isupper():
        toks[0] = toks[0][0].lower() + toks[0][1:]
    core = " ".join(toks)
    return (article + " " + core).strip(), core


def _sg_definition(sentence, lower_vocab, first_in_block):
    sentence = sentence.strip()
    if _sg_wc(sentence) < 6 or _sg_wc(sentence) > 45 or "?" in sentence:
        return None
    if _sg_is_code(sentence) or re.search(r"[A-Za-z_]\w*\s*=(?!=)", sentence):
        return None
    m = _SG_DEF_RE.match(sentence)
    if not m:
        return None
    subj = _sg_clean_subject(m.group("subj"), lower_vocab, first_in_block, sentence[0].isupper())
    if not subj:
        return None
    disp, core = subj
    verb, rest = m.group("verb"), _sg_trim_end(m.group("rest"))
    if _sg_wc(rest) < 3 or re.match(r"^(?:%s)\b" % "|".join(_SG_BAD_REST_FIRST), rest, re.I):
        return None
    plural = verb in ("are", "are defined as", "store", "hold", "contain", "represent", "provide",
                      "allow", "help", "handle", "refer to") or verb.startswith("are ")
    if verb in ("is", "are", "is defined as", "are defined as"):
        q, qtype, pred = ("What %s %s?" % ("are" if plural else "is", disp)), "is", _sg_cap(rest)
    elif verb == "means":
        q, qtype, pred = "What does %s mean?" % disp, "is", _sg_cap(rest)
    elif verb in ("refers to", "refer to"):
        q, qtype, pred = "What does %s refer to?" % disp, "is", "Refers to " + rest
    elif verb.endswith(("used to", "used for")):
        q, qtype = "What %s %s used for?" % ("are" if verb.startswith("are") else "is", disp), "used"
        pred = _sg_cap("used " + verb.split()[-1] + " " + rest)
    else:
        q, qtype = "What does %s do?" % disp, "does"
        pred = _sg_cap(verb + " " + rest)
    return {"question": q, "answer": sentence, "pred": pred, "subject": core, "qtype": qtype,
            "kind": "def"}


def _sg_term_fact(text, min_words=2):
    m = _SG_TERM_RE.match(text.strip())
    if not m:
        return None
    term, defn = m.group("term").strip(), _sg_trim_end(m.group("defn"))
    toks = term.split()
    if not 1 <= len(toks) <= 4 or _SG_LABEL.match(term) or _sg_wc(defn) < min_words:
        return None
    if toks[0].lower() in _SG_BAD_SUBJ_FIRST and toks[0].lower() not in _SG_KW:
        return None
    if any(t.lower() in _SG_VERBISH for t in toks) or re.search(r"[=()]", term):
        return None
    if _sg_is_code(text):
        return None
    return {"question": "What is %s?" % term, "answer": "%s \u2013 %s" % (term, defn),
            "pred": _sg_cap(defn), "subject": term, "qtype": "is", "kind": "term"}


def _sg_intent(question):
    q = question.lower()
    if re.search(r"\b(difference|differ|compare|differentiate|distinguish|versus|vs)\b", q):
        return "compare"
    if re.match(r"^(name|list|mention|enumerate|give|state|identify)\b", q):
        return "list"
    if q.startswith("why"):
        return "why"
    if q.startswith("how"):
        return "how"
    return "what"


def _sg_qkeys(question):
    q = re.sub(r"\b(?:used|use)\s+(?:for|to)\b.*$", "", question.strip(), flags=re.I)
    q = re.sub(r"^\s*(?:" + _SG_QWORD + r")\b(?:\s+(?:is|are|does|do|was|were|can|the|a|an))*", "",
               q, flags=re.I)
    return list(dict.fromkeys(_sg_keys(q)))


def _sg_units(section):
    units = []
    for bi, b in enumerate(section["blocks"]):
        if b["type"] == "bullet":
            units.append({"text": b["text"], "bi": bi, "bullet": True})
        elif b["type"] in ("prose", "answer"):
            for s in _sg_sentences(b["text"]):
                units.append({"text": s, "bi": bi, "bullet": False})
    return units


def _sg_build_corpus(sections):
    corpus, df = [], {}
    for sec in sections:
        if sec["skip"] or sec["qsec"]:
            continue
        units = [u for u in _sg_units(sec) if _sg_wc(u["text"]) >= 2 and not _sg_is_code(u["text"])]
        if not units:
            continue
        hk = set(_sg_keys(sec["heading"]))
        bk = set()
        for u in units:
            bk.update(_sg_keys(u["text"]))
        corpus.append({"heading": sec["heading"], "units": units, "hkeys": hk, "bkeys": bk})
        for k in hk | bk:
            df[k] = df.get(k, 0) + 1
    total = max(1, len(corpus))
    idf = {k: math.log(1 + total / v) for k, v in df.items()}
    return corpus, idf


_SG_CUES = {
    "why": re.compile(r"\b(because|helps?|allows?|enables?|useful|important|benefits?|easier|"
                      r"simpler|readable|so that|prevents?|reason|popular)\b", re.I),
    "how": re.compile(r"\b(steps?|by|uses?|works?|syntax|first|then|returns?|starts?|stops?)\b", re.I),
    "what": re.compile(r"\b(is|are|means|refers? to|defined as|consists? of|contains?|used)\b", re.I),
}


def _sg_retrieve(question, corpus, idf):
    """Find the passage in the PDF that answers the question, or None."""
    qkeys = _sg_qkeys(question)
    if not qkeys or not corpus:
        return None
    w = lambda k: idf.get(k, 1.0)
    total = sum(w(k) for k in qkeys)
    intent = _sg_intent(question)

    best = None
    for sec in corpus:
        cov = sum(w(k) for k in qkeys if k in sec["hkeys"] or k in sec["bkeys"])
        head = sum(w(k) for k in qkeys if k in sec["hkeys"])
        score = cov + head
        if best is None or score > best[0]:
            best = (score, cov / total, sec)
    if best is None or best[1] < 0.6:
        return None
    sec = best[2]
    units = sec["units"]
    heading_keys = sec["hkeys"]

    def uscore(u):
        uk = set(_sg_keys(u["text"]))
        s = sum(w(k) for k in qkeys if k in uk)
        cue = _SG_CUES.get(intent)
        if cue and cue.search(u["text"]):
            s += 0.6
        return s

    scores = [uscore(u) for u in units]

    def words_of(sel):
        return sum(_sg_wc(units[i]["text"]) for i in sel)

    chosen = []
    if intent == "list":
        run, runs = [], []
        for i, u in enumerate(units):
            if u["bullet"]:
                run.append(i)
            else:
                if run:
                    runs.append(run)
                run = []
        if run:
            runs.append(run)
        if runs:
            chosen = max(runs, key=len)[:8]
            if len(chosen) < 2:
                chosen = []
    if not chosen and intent == "compare":
        m = re.search(r"between\s+(.+?)\s+(?:and|vs\.?|versus)\s+(.+?)[?.]?$", question, re.I)
        sides = [set(_sg_keys(m.group(1), _SG_STOP)), set(_sg_keys(m.group(2), _SG_STOP))] if m else []
        picked = []
        for i, u in enumerate(units):
            uk = set(_sg_keys(u["text"]))
            if any(side & uk for side in sides if side):
                picked.append(i)
        if picked and all(any(side & set(_sg_keys(units[i]["text"])) for i in picked)
                          for side in sides if side):
            for i in picked:
                if words_of(chosen + [i]) > 70 and chosen:
                    break
                chosen.append(i)
    if not chosen:
        top = max(range(len(units)), key=lambda i: (scores[i], -i))
        if scores[top] <= 0:
            return None
        start = top
        if start > 0 and re.match(r"^(it|this|they|these|those|such|that|he|she)\b",
                                  units[top]["text"], re.I):
            start = top - 1
        chosen = [start]
        j = start + 1
        while j < len(units) and len(chosen) < 3 and words_of(chosen + [j]) <= 60:
            chosen.append(j)
            j += 1

    joined = [units[i]["text"] for i in chosen]
    answer = "; ".join(_sg_trim_end(t) for t in joined) + "." if units[chosen[0]]["bullet"] \
        else " ".join(joined)
    answer = re.sub(r"\s+", " ", answer).strip()

    ans_keys = set(_sg_keys(answer))
    got = sum(w(k) for k in qkeys if k in ans_keys or k in heading_keys)
    if got / total < 0.6 or not 4 <= _sg_wc(answer) <= 95 or "?" in answer:
        return None
    return answer, sec["heading"]


def _sg_heading_question(heading):
    words = heading.split()
    low = [x.lower() for x in words]
    if not 1 <= len(words) <= 4:
        return None
    if heading.lower() in _SG_GENERIC_HEAD or low[0] in _SG_GENERIC_HEAD:
        return None
    if low[0] in _SG_IMPERATIVE_HEAD or low[0].endswith("ing"):
        return None
    if any(t in _SG_SMALL - {"and"} for t in low) or any(t in _SG_BAD_SUBJ_TOKENS - {"or"} for t in low):
        return None
    if re.search(r"[^A-Za-z0-9 \-/&']", heading):
        return None
    return "Explain %s." % heading


def _sg_first_words(sentences, limit=60):
    out = []
    for s in sentences:
        if out and _sg_wc(" ".join(out + [s])) > limit:
            break
        out.append(s)
        if len(out) >= 3:
            break
    return " ".join(out)


def _sg_extract_facts(text):
    sections = _sg_parse(text)
    corpus, idf = _sg_build_corpus(sections)
    lower_vocab = set(re.findall(r"(?<![A-Za-z])([a-z][a-z]+)", text or ""))
    facts = []
    pos = 0

    def add(f, section, base):
        nonlocal pos
        f.setdefault("subject", "")
        f.setdefault("pred", "")
        f.setdefault("qtype", "qa")
        f["section"] = section or ""
        f["score"] = base
        f["pos"] = pos
        pos += 1
        facts.append(f)

    body_words = re.findall(r"[A-Za-z][A-Za-z0-9_]+", (text or "").lower())
    freq = {}
    for wd in body_words:
        freq[_sg_stem(wd)] = freq.get(_sg_stem(wd), 0) + 1

    def freq_bonus(term):
        toks = [_sg_stem(t) for t in _sg_words(term)]
        if not toks:
            return 0.0
        return min(10.0, math.log(1 + max(freq.get(t, 0) for t in toks)) * 2.5)

    def_subjects = set()

    for sec in sections:
        if sec["skip"]:
            continue
        blocks = sec["blocks"]

        # 1) explicit questions (inline answer, following answer, or retrieved)
        for bi, b in enumerate(blocks):
            if b["type"] != "question":
                continue
            ans, src = "", sec["heading"]
            if b.get("inline"):
                ans = b["inline"]
            else:
                parts, prev_is_q = [], bi > 0 and blocks[bi - 1]["type"] == "question"
                for nb in blocks[bi + 1:]:
                    if nb["type"] == "question":
                        break
                    if nb["type"] not in ("answer", "prose", "bullet") or not nb["text"]:
                        continue
                    if _SG_SKIP_HEAD.search(nb["text"][:60]):
                        break
                    if nb["type"] == "bullet" and (sec["qsec"] or not parts):
                        break            # a bullet list is not a per-question answer here
                    parts.append(nb["text"])
                    if _sg_wc(" ".join(parts)) >= 70:
                        break
                ans = " ".join(parts).strip()
                if ans and not re.search(r"[.!?)]$", ans):
                    ans = ""             # unfinished text / a label such as "Try these:"
                if ans and prev_is_q and not (set(_sg_qkeys(b["text"])) & set(_sg_keys(ans))):
                    ans = ""             # inside a question list: must actually relate
            score = 100
            src = ""
            if not ans or _sg_wc(ans) < 5:
                found = _sg_retrieve(b["text"], corpus, idf)
                if not found:
                    continue
                ans, src = found
                score = 95
            ans = re.sub(r"\s+", " ", ans).strip()
            if "?" in ans or _sg_wc(ans) < 4:
                continue
            add({"question": b["text"], "answer": ans, "kind": "qa"}, src, score)

        if sec["qsec"]:
            continue

        # 2) definitions / "term - meaning" lines
        first_block_done = False
        for bi, b in enumerate(blocks):
            if b["type"] not in ("prose", "bullet"):
                continue
            if b["type"] == "bullet" or (b["type"] == "prose" and _SG_TERM_RE.match(b["text"])):
                tf = _sg_term_fact(b["text"])
                if tf and _sg_stem(tf["subject"]) not in def_subjects:
                    def_subjects.add(_sg_stem(tf["subject"]))
                    add(tf, sec["heading"], 68 + freq_bonus(tf["subject"]))
                    continue
            for si, sent in enumerate(_sg_sentences(b["text"])):
                d = _sg_definition(sent, lower_vocab, first_in_block=(si == 0))
                if not d:
                    continue
                key = " ".join(_sg_stem(t) for t in d["subject"].split())
                if key in def_subjects:
                    continue
                def_subjects.add(key)
                bonus = 5 if not first_block_done and si == 0 else 0
                add(d, sec["heading"], 72 + bonus + freq_bonus(d["subject"]))
            first_block_done = True

        # 3) heading question, only when no definition already covers it
        hq = _sg_heading_question(sec["heading"]) if sec["heading"] else None
        if hq:
            hkey = " ".join(_sg_stem(t) for t in re.sub(r"^\d+[.)]?\s*", "", sec["heading"]).split())
            if hkey not in def_subjects:
                sents = []
                bullets = [b["text"] for b in blocks if b["type"] == "bullet"]
                prose = [s for b in blocks if b["type"] == "prose" for s in _sg_sentences(b["text"])
                         if not _sg_is_code(s) and "?" not in s]
                if prose:
                    sents = prose
                    ans = _sg_first_words(sents)
                elif len(bullets) >= 2:
                    ans = "; ".join(_sg_trim_end(x) for x in bullets[:6]) + "."
                else:
                    ans = ""
                if _sg_wc(ans) >= 6:
                    def_subjects.add(hkey)
                    add({"question": hq, "answer": ans, "kind": "head", "subject": sec["heading"]},
                        sec["heading"], 55 + freq_bonus(sec["heading"]))
    return facts


@lru_cache(maxsize=4)
def _sg_facts_cached(text_hash, text):
    return tuple(tuple(sorted(f.items())) for f in _sg_rank(_sg_extract_facts(text)))


def _sg_rank(facts):
    seen, out = [], []
    for f in sorted(facts, key=lambda f: (-f["score"], f["pos"])):
        qk = frozenset(_sg_qkeys(f["question"]))
        if not qk:
            continue
        ak = frozenset(_sg_keys(f["answer"], _SG_STOP))
        dup = False
        for gq, ga, gkind in seen:
            if qk == gq or len(qk & gq) / len(qk | gq) >= 0.8:
                dup = True
                break
            if f["kind"] != "qa" and ak and ga and len(ak & ga) / len(ak | ga) >= 0.85:
                dup = True
                break
        if not dup:
            seen.append((qk, ak, f["kind"]))
            out.append(f)
    return out


def _sg_get_facts(text):
    h = hashlib.md5((text or "").encode("utf-8", "ignore")).hexdigest()
    return [dict(t) for t in _sg_facts_cached(h, text or "")]


# ------------------------------------------------------------
# PUBLIC: Important Questions
# ------------------------------------------------------------
def generate_important_questions(text, limit=10, offset=0):
    """Question + answer pairs taken from the PDF. `offset` rotates through the pool."""
    if not text or not str(text).strip():
        return []
    facts = _sg_get_facts(str(text))
    facts = [f for f in facts if 4 <= _sg_wc(f["answer"]) <= 110]
    if not facts:
        return []
    if offset and len(facts) > limit:
        start = offset % len(facts)
        facts = facts[start:] + facts[:start]
    return [{"question": f["question"], "answer": f["answer"], "section": f.get("section", "")}
            for f in facts[:limit]]


# ------------------------------------------------------------
# PUBLIC: Quiz
# ------------------------------------------------------------
def _sg_qa_option(fact):
    """Text of the correct option for a question whose answer is a passage."""
    ans = _sg_trim_end(fact["answer"])
    if _sg_wc(ans) <= 45:
        return ans
    qk = set(_sg_qkeys(fact["question"]))
    sents = _sg_sentences(fact["answer"])
    if not sents:
        return ""
    best = max(sents, key=lambda x: len(qk & set(_sg_keys(x))))
    best = _sg_trim_end(best)
    return best if _sg_wc(best) <= 45 else ""


def generate_pdf_quiz(text, limit=10):
    """Multiple-choice questions. Every correct option is copied from the PDF."""
    if not text or not str(text).strip():
        return []
    facts = [f for f in _sg_get_facts(str(text)) if f["kind"] != "head"]
    if len(facts) < 4:
        return []

    for f in facts:
        # "pred": short description that fits after the question ("A name that stores a value")
        # "sent": the whole source sentence/passage
        f["pred_opt"] = _sg_trim_end(f["pred"]) if f.get("pred") else ""
        if f.get("pred"):
            whole = _sg_trim_end(f["answer"])
            f["sent_opt"] = whole if _sg_wc(whole) <= 45 else ""
        else:
            f["sent_opt"] = _sg_qa_option(f)
    usable = [f for f in facts if f["pred_opt"] or f["sent_opt"]]
    if len(usable) < 4:
        return []

    def pick_distractors(f, form, need=3):
        key = form + "_opt"
        correct = f[key]
        subj_keys = set(_sg_keys(f["subject"])) if f.get("subject") else set()
        qkeys = set(_sg_qkeys(f["question"])) | subj_keys
        for lo, hi in ((0.5, 2.2), (0.3, 4.0)):
            same, other = [], []
            for g in usable:
                if g is f or g["question"] == f["question"]:
                    continue
                cand = g[key]
                if not cand or cand.lower() == correct.lower():
                    continue
                if qkeys & set(_sg_keys(cand)):
                    continue                   # could also look like a right answer
                if _sg_jaccard(cand, correct) > 0.4:
                    continue
                ratio = max(1, _sg_wc(cand)) / max(1, _sg_wc(correct))
                if not lo <= ratio <= hi:
                    continue
                (same if g.get("qtype") == f.get("qtype") else other).append(cand)
            random.shuffle(same)
            random.shuffle(other)
            chosen = []
            for cand in same + other:
                if cand not in chosen and all(_sg_jaccard(cand, c) <= 0.5 for c in chosen):
                    chosen.append(cand)
                if len(chosen) == need:
                    return chosen
        return None

    pool = usable[:]
    pool.sort(key=lambda f: -f["score"] + random.uniform(0, 12))

    quiz, used_subjects = [], set()
    for f in pool:
        if len(quiz) >= limit:
            break
        skey = _sg_stem(f.get("subject", "") or f["question"])
        if skey in used_subjects:
            continue

        made = None
        reverse_ok = (f["kind"] in ("def", "term") and f["qtype"] in ("is", "used", "does")
                      and f.get("subject") and f["pred_opt"] and 2 <= _sg_wc(f["pred_opt"]) <= 30)
        if reverse_ok and random.random() < 0.4:
            subj = f["subject"]
            others = []
            for g in usable:
                if g is f or g["kind"] not in ("def", "term") or not g.get("subject"):
                    continue
                gs = g["subject"]
                if set(_sg_keys(gs)) & (set(_sg_keys(subj)) | set(_sg_keys(f["pred_opt"], _SG_STOP))):
                    continue
                if g["pred_opt"] and _sg_jaccard(g["pred_opt"], f["pred_opt"]) > 0.4:
                    continue
                if gs not in others and gs.lower() != subj.lower():
                    others.append(gs)
            if len(others) >= 3:
                random.shuffle(others)
                opts = [subj] + others[:3]
                random.shuffle(opts)
                made = {"question": 'Which term matches this description: "%s"?' % f["pred_opt"],
                        "options": opts, "answer": subj}

        if made is None:
            for form in (("pred", "sent") if f["pred_opt"] else ("sent",)):
                if not f[form + "_opt"]:
                    continue
                ds = pick_distractors(f, form)
                if ds:
                    opts = [f[form + "_opt"]] + ds
                    random.shuffle(opts)
                    made = {"question": f["question"], "options": opts, "answer": f[form + "_opt"]}
                    break
        if made is None:
            continue

        made["explanation"] = f["answer"]
        made["section"] = f.get("section", "")
        quiz.append(made)
        used_subjects.add(skey)
    return quiz



def load_pdf(uploaded_file):
    """Read a PDF locally and prepare all PDF study features."""
    if not uploaded_file:
        return False, "No PDF selected."
    try:
        try:
            from pypdf import PdfReader
        except ImportError:
            from PyPDF2 import PdfReader

        reader = PdfReader(uploaded_file)
        pages = [p.extract_text() or "" for p in reader.pages]
        text = "\n".join(pages).strip()

        if not text:
            return False, "The PDF does not contain extractable text. Try a text-based PDF."

        st.session_state.pdf_pages = pages
        st.session_state.pdf_text = text
        st.session_state.pdf_name = uploaded_file.name
        st.session_state.pdf_summary = create_pdf_summary(text)
        st.session_state.pdf_quiz = generate_pdf_quiz(text, limit=10)
        st.session_state.last_pdf_quiz_name = uploaded_file.name
        st.session_state.quiz_answers = {}
        st.session_state.quiz_submitted = False
        st.session_state.quiz_score = 0
        st.session_state.important_questions = generate_important_questions(text)
        st.session_state.important_offset = 0
        st.session_state.quiz_id = st.session_state.get("quiz_id", 0) + 1
        st.session_state.quiz_source = hashlib.md5(text.encode("utf-8", "ignore")).hexdigest()
        st.session_state.important_source = st.session_state.quiz_source

        save_pdf_cache(
    text,
    uploaded_file.name,
    pages
)

        award("First PDF", "📄", "Uploaded your first study PDF")
        return True, ""
    except ImportError:
        return False, "PDF support is not installed. Run: pip install pypdf"
    except Exception as e:
        return False, f"Could not read the PDF: {e}"


def _md_safe(value):
    """Escape characters that Streamlit would otherwise treat as Markdown."""
    return re.sub(r"([\\`*_~$])", r"\\\1", str(value or ""))


def handle_pdf_upload(uploaded_file):
    """Read an uploaded PDF ONCE.

    Streamlit re-runs the whole script on every click. The old pages called
    load_pdf() on every re-run while the file was still in the uploader, so the
    quiz was regenerated and re-shuffled each time the student picked an option
    or pressed Submit. The answers were then checked against a different quiz.
    """
    if not uploaded_file:
        return True, ""
    try:
        sig = hashlib.md5(uploaded_file.getvalue()).hexdigest() + ":" + uploaded_file.name
    except Exception:
        sig = "%s:%s" % (uploaded_file.name, getattr(uploaded_file, "size", 0))
    if st.session_state.get("pdf_sig") == sig and st.session_state.get("pdf_text"):
        return True, ""
    ok, msg = load_pdf(uploaded_file)
    if ok:
        st.session_state.pdf_sig = sig
    return ok, msg


def ensure_pdf_ready():
    """Make sure the PDF text, quiz and important questions are in session state.

    Reloads the last PDF from the cache file when the session has none, and
    builds the quiz / questions only when the PDF text has changed.
    """
    if not st.session_state.get("pdf_text"):
        cached = load_pdf_cache()
        if not cached:
            return False
        st.session_state.pdf_text = cached.get("text", "")
        st.session_state.pdf_name = cached.get("filename", "Uploaded PDF")
        st.session_state.pdf_pages = cached.get("pages", [])
        st.session_state.pdf_quiz = []
        st.session_state.important_questions = []
        st.session_state.quiz_source = ""
        st.session_state.important_source = ""
        st.session_state.quiz_answers = {}
        st.session_state.quiz_submitted = False
        st.session_state.quiz_score = 0

    pdf_text = st.session_state.pdf_text
    key = hashlib.md5(pdf_text.encode("utf-8", "ignore")).hexdigest()
    if st.session_state.get("quiz_source") != key:
        st.session_state.pdf_quiz = generate_pdf_quiz(pdf_text, limit=10)
        st.session_state.quiz_source = key
        st.session_state.quiz_id = st.session_state.get("quiz_id", 0) + 1
        st.session_state.quiz_answers = {}
        st.session_state.quiz_submitted = False
        st.session_state.quiz_score = 0
    if st.session_state.get("important_source") != key:
        st.session_state.important_questions = generate_important_questions(pdf_text, limit=10)
        st.session_state.important_source = key
        st.session_state.important_offset = 0
    return True


def answer_from_pdf(question,text):
    if not text: return "Please upload a study PDF first."
    stop={"what","is","are","the","a","an","of","in","on","to","for","and","or","how","why","who","when","where","does","do","can","i","you","explain","tell","me"}
    q={w for w in re.findall(r"[a-zA-Z0-9]+",question.lower()) if len(w)>2 and w not in stop}; scored=[]
    for x in re.split(r"\n+|(?<=[.!?])\s+",text):
        x=re.sub(r"\s+"," ",x).strip(); score=len(q & set(re.findall(r"[a-zA-Z0-9]+",x.lower())))
        if score: scored.append((score,x))
    if not scored: return "I couldn't find a matching answer in the uploaded PDF. Try an exact topic or keyword from the PDF."
    scored.sort(key=lambda z:z[0],reverse=True); return "\n\n".join(x[1] for x in scored[:4])

def speak_text(text):
    safe=html_lib.escape(text).replace("\n"," "); html("<script>if('speechSynthesis' in window){speechSynthesis.cancel();speechSynthesis.speak(new SpeechSynthesisUtterance("+repr(safe)+"));}</script>")


def add_completed_study_minutes(minutes, subject="General", topic="Pomodoro Session"):
    """Record a completed study block in the existing planner data."""
    minutes = int(minutes)
    if minutes <= 0:
        return
    st.session_state.sessions.append({
        "subject": subject,
        "date": date.today(),
        "time": datetime.now().strftime("%H:%M"),
        "duration": minutes,
        "topic": topic,
        "completed": True
    })
    st.session_state.completed_days.add(date.today())


def generate_smart_schedule(subjects, total_minutes, start_time, session_minutes, break_minutes):
    """Create a simple balanced timetable from the user's subjects and available time."""
    subjects = [s for s in subjects if s.strip()]
    if not subjects or total_minutes <= 0:
        return []

    slots = []
    current = datetime.combine(date.today(), start_time)
    remaining = int(total_minutes)
    index = 0

    while remaining >= min(15, session_minutes):
        study_for = min(session_minutes, remaining)
        subject = subjects[index % len(subjects)]
        slots.append({
            "time": current.strftime("%I:%M %p"),
            "subject": subject,
            "duration": study_for,
            "type": "Study"
        })
        current += timedelta(minutes=study_for)
        remaining -= study_for
        index += 1

        if remaining >= 15 and break_minutes > 0:
            current += timedelta(minutes=break_minutes)
            remaining -= min(break_minutes, remaining)

    return slots


def render_pomodoro_timer():
    st.markdown("### ⏱️ Pomodoro Study Timer")
    st.caption("Use a focused study block, take a short break, then log the completed block.")

    c1, c2, c3 = st.columns(3)
    with c1:
        focus = st.number_input("Focus minutes", min_value=5, max_value=120, value=25, step=5, key="pom_focus")
    with c2:
        break_min = st.number_input("Break minutes", min_value=1, max_value=30, value=5, step=1, key="pom_break")
    with c3:
        subject = st.selectbox("Subject", st.session_state.subjects, key="pom_subject")

    # Browser-side timer keeps counting without requiring Streamlit reruns.
    st.components.v1.html(
        f"""
        <div style="font-family:Arial,sans-serif;background:#FFFDF5;border:1px solid #E1D4EC;
                    border-radius:16px;padding:22px;text-align:center;color:#4B2E6D;">
            <div id="timer" style="font-size:42px;font-weight:800;">{int(focus):02d}:00</div>
            <div id="mode" style="margin:8px 0 14px;font-weight:600;">Focus</div>
            <button id="start" style="padding:9px 18px;border:0;border-radius:9px;background:#7B5CB8;color:white;">Start</button>
            <button id="pause" style="padding:9px 18px;border:0;border-radius:9px;background:#6E5487;color:white;margin-left:6px;">Pause</button>
            <button id="reset" style="padding:9px 18px;border:0;border-radius:9px;background:#D8C8EA;color:#4B2E6D;margin-left:6px;">Reset</button>
            <script>
            (() => {{
                const timer=document.getElementById("timer"), mode=document.getElementById("mode");
                const start=document.getElementById("start"), pause=document.getElementById("pause"), reset=document.getElementById("reset");
                const focus={int(focus)}*60, rest={int(break_min)}*60;
                let left=focus, running=false, phase="Focus", id=null;
                function draw() {{
                    const m=Math.floor(left/60), s=left%60;
                    timer.textContent=String(m).padStart(2,"0")+":"+String(s).padStart(2,"0");
                    mode.textContent=phase;
                }}
                function tick() {{
                    if(!running) return;
                    left--;
                    if(left<=0) {{
                        if(phase==="Focus") {{ phase="Break"; left=rest; }}
                        else {{ phase="Focus"; left=focus; }}
                    }}
                    draw();
                }}
                start.onclick=()=>{{ if(!running) {{ running=true; id=setInterval(tick,1000); }} }};
                pause.onclick=()=>{{ running=false; if(id) clearInterval(id); }};
                reset.onclick=()=>{{ running=false; if(id) clearInterval(id); phase="Focus"; left=focus; draw(); }};
                draw();
            }})();
            </script>
        </div>
        """,
        height=180
    )

    if st.button("✅ Log Completed Pomodoro", use_container_width=True, key="log_pomodoro"):
        add_completed_study_minutes(focus, subject, "Pomodoro Focus Session")
        st.session_state.pomodoro_count += 1
        st.session_state.pomodoro_minutes += int(focus)
        award("Pomodoro Starter", "⏱️", "Completed your first focused Pomodoro session")
        st.success(f"Logged {focus} minutes for {subject}. Great work! 🎉")
        st.rerun()


def render_daily_goals():
    st.markdown("### 🎯 Daily Study Goal")
    c1, c2 = st.columns(2)
    with c1:
        goal = st.number_input("Goal (minutes)", min_value=15, max_value=1440,
                               value=int(st.session_state.daily_goal_minutes), step=15,
                               key="daily_goal_input")
    with c2:
        today_minutes = sum(
            int(s.get("duration", 0)) for s in st.session_state.sessions
            if s.get("date") == date.today()
        )
        st.metric("Today", f"{today_minutes} min", f"{today_minutes-goal:+d} min")

    st.session_state.daily_goal_minutes = int(goal)
    progress = min(today_minutes / goal, 1.0) if goal else 0
    st.progress(progress)
    if today_minutes >= goal:
        award("Daily Goal", "🎯", "Reached a daily study goal")
        st.success("Daily goal completed! 🌟")
    else:
        st.info(f"{goal - today_minutes} minutes remaining today.")


def render_mistake_review():
    st.markdown("### 🔁 Mistake Review")
    mistakes = st.session_state.mistake_review
    if not mistakes:
        st.info("Complete a PDF Quiz and submit it. Your incorrect answers will appear here for revision.")
        return

    st.caption(f"{len(mistakes)} saved mistake(s) from your PDF quizzes.")
    for i, item in enumerate(mistakes, 1):
        with st.expander(f"Question {i}: {item['question']}"):
            st.write(f"**Your answer:** {item['selected'] or 'Not answered'}")
            st.write(f"**Correct answer:** {item['answer']}")
            st.caption(item.get("pdf", "PDF Quiz"))
    if st.button("🗑️ Clear Mistake Review", use_container_width=True):
        st.session_state.mistake_review = []
        st.rerun()


def render_analytics():
    st.markdown("### 📊 Study Analytics")
    sessions = st.session_state.sessions
    if not sessions:
        st.info("Complete a study session or Pomodoro block to see analytics.")
        return

    df = pd.DataFrame(sessions)
    df["date"] = pd.to_datetime(df["date"])
    df["duration"] = pd.to_numeric(df["duration"], errors="coerce").fillna(0)

    total = int(df["duration"].sum())
    completed = int(df["completed"].fillna(False).sum()) if "completed" in df else 0
    avg = round(df["duration"].mean()) if len(df) else 0
    streak = calculate_streak()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Study", f"{total} min")
    c2.metric("Completed Sessions", completed)
    c3.metric("Average Session", f"{avg} min")
    c4.metric("Current Streak", f"{streak} day(s)")

    by_subject = df.groupby("subject", as_index=False)["duration"].sum().sort_values("duration", ascending=False)
    fig = px.bar(by_subject, x="subject", y="duration", title="Study Time by Subject",
                 labels={"duration":"Minutes", "subject":"Subject"})
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

    by_day = df.groupby("date", as_index=False)["duration"].sum()
    fig2 = px.line(by_day, x="date", y="duration", markers=True, title="Daily Study Trend",
                   labels={"duration":"Minutes", "date":"Date"})
    fig2.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig2, use_container_width=True)


def render_smart_schedule():
    st.markdown("### 📅 Smart Study Schedule")
    st.caption("Create a balanced study plan from your current subjects and available study time.")

    c1, c2 = st.columns(2)
    with c1:
        selected = st.multiselect("Subjects", st.session_state.subjects,
                                  default=st.session_state.subjects[:min(3, len(st.session_state.subjects))],
                                  key="smart_subjects")
        total = st.number_input("Available study minutes", min_value=15, max_value=720,
                                value=120, step=15, key="smart_total")
    with c2:
        start = st.time_input("Start time", value=datetime.strptime("18:00", "%H:%M").time(), key="smart_start")
        session_len = st.number_input("Each study block (minutes)", min_value=15, max_value=120,
                                      value=30, step=5, key="smart_session")
        break_len = st.number_input("Break (minutes)", min_value=0, max_value=30,
                                    value=5, step=1, key="smart_break")

    if st.button("✨ Generate Smart Schedule", use_container_width=True):
        schedule = generate_smart_schedule(selected, int(total), start, int(session_len), int(break_len))
        st.session_state.smart_schedule = schedule
        if schedule:
            award("Smart Scheduler", "📅", "Generated a personalized study schedule")
        st.rerun()

    if st.session_state.smart_schedule:
        st.markdown("#### Today's Suggested Plan")
        for i, slot in enumerate(st.session_state.smart_schedule, 1):
            st.write(f"**{slot['time']}** — {slot['subject']} · {slot['duration']} min")
        if st.button("➕ Add Schedule to Calendar", use_container_width=True):
            for slot in st.session_state.smart_schedule:
                h, m = map(int, datetime.strptime(slot["time"], "%I:%M %p").strftime("%H:%M").split(":"))
                st.session_state.sessions.append({
                    "subject": slot["subject"],
                    "date": date.today(),
                    "time": f"{h:02d}:{m:02d}",
                    "duration": slot["duration"],
                    "topic": "Smart Schedule",
                    "completed": False
                })
            st.success("Smart schedule added to your Calendar.")
            st.rerun()


def feature_sidebar_pages():
    return [
        "🏠 Dashboard","📅 Calendar","📚 Subjects","📊 Progress",
        "🤖 Study Chatbot","📄 PDF Summary","🧠 PDF Quiz",
        "⏱️ Pomodoro Timer","🎯 Daily Goals","📈 Study Analytics",
        "📅 Smart Schedule","🔁 Mistake Review",
        "🏆 Achievements","📝 Personal Notes","⭐ Important Questions"
    ]

# SESSION STATE
# ============================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = ""

if "subjects" not in st.session_state:
    st.session_state.subjects = [
        "Organic Chemistry",
        "US History",
        "Python"
    ]

if "sessions" not in st.session_state:
    st.session_state.sessions = []

if "completed_days" not in st.session_state:
    st.session_state.completed_days = set()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
init_feature_state()


# ============================================================
# LOGIN PAGE
# ============================================================

def _account_file():
    return Path(__file__).with_name("study_accounts.json")

def load_accounts():
    path = _account_file()
    try:
        if path.exists():
            data = json.loads(path.read_text(encoding="utf-8"))
            return data if isinstance(data, dict) else {}
    except Exception:
        pass
    return {}

def save_accounts(accounts):
    _account_file().write_text(
        json.dumps(accounts, indent=2), encoding="utf-8"
    )

def password_hash(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def login_page():
    """Reference-style torn-paper login page."""

    html("""
    <style>
    /* =========================================================
       LOGIN PAGE
       ========================================================= */

    /* Soft blurred background */
    .stApp {
        background:
            linear-gradient(rgba(216,222,226,.70), rgba(216,222,226,.70)),
            repeating-linear-gradient(
                90deg,
                #d5dce0 0px, #d5dce0 85px,
                #c9d1d6 85px, #c9d1d6 145px,
                #dde2e5 145px, #dde2e5 235px
            ) !important;
    }

    .block-container {
        padding-top: 0.8rem !important;
        padding-bottom: 1rem !important;
    }

    /* Hide normal Streamlit chrome on login */
    #MainMenu, footer {
        visibility: hidden;
    }

    /* Force the application UI to stay light */
    [data-testid="stAppViewContainer"],
    [data-testid="stHeader"] {
        background-color: #f7f8fc !important;
    }

   [data-testid="stSidebar"] {
    background-color: #EDE4F7 !important;
}
    /* The actual Streamlit container becomes the paper */
    [class*="st-key-login_paper"] {
        width: 430px !important;
        max-width: 92vw !important;
        min-height: 400px !important;
        margin: 35px auto 0 auto !important;
        padding: 32px 55px 40px !important;
        box-sizing: border-box !important;

        background:
            radial-gradient(circle at 20% 25%, rgba(110,110,100,.06) 0 2px, transparent 3px),
            radial-gradient(circle at 70% 75%, rgba(110,110,100,.05) 0 2px, transparent 3px),
            linear-gradient(145deg, #fff 0%, #f8faf8 100%) !important;

        background-size: 90px 80px, 115px 100px, auto !important;

        /* torn-paper outline */
        clip-path: polygon(
            2% 4%, 10% 2%, 19% 5%, 29% 2%, 39% 5%,
            49% 2%, 60% 5%, 70% 2%, 81% 5%, 91% 2%, 98% 6%,
            96% 17%, 99% 28%, 96% 39%, 99% 50%, 96% 61%,
            99% 73%, 96% 84%, 98% 95%, 88% 93%, 78% 97%,
            68% 94%, 58% 98%, 48% 94%, 38% 97%, 28% 94%,
            18% 98%, 8% 94%, 3% 96%, 5% 84%, 2% 73%,
            5% 61%, 2% 50%, 5% 39%, 2% 28%, 5% 17%
        ) !important;

        filter: drop-shadow(0 20px 24px rgba(65,72,78,.30)) !important;
        position: relative !important;
    }

    /* Wing/logo */
    .paper-wing {
        text-align: center;
        height: 58px;
        margin-bottom: 2px;
        color: #626079;
        font-size: 46px;
        line-height: 58px;
        transform: rotate(-8deg);
        filter: grayscale(25%);
    }

    .paper-login-title {
        text-align: center;
        font-family: Georgia, "Times New Roman", serif;
        font-size: 26px;
        font-weight: 500;
        color: #4e5160;
        margin-bottom: 13px;
    }

    /* Labels */
    [class*="st-key-login_paper"] .stTextInput label {
        font-family: Georgia, "Times New Roman", serif !important;
        font-size: 12px !important;
        color: #6e707b !important;
    }

    /* Inputs */
    [class*="st-key-login_paper"] .stTextInput input {
        height: 31px !important;
        background: rgba(255,255,255,.18) !important;
        border: 0 !important;
        border-bottom: 1px solid #9c9da4 !important;
        border-radius: 0 !important;
        box-shadow: none !important;
        color: #4e5160 !important;
        font-family: Georgia, "Times New Roman", serif !important;
        font-size: 12px !important;
        padding: 3px 5px !important;
    }

    [class*="st-key-login_paper"] .stTextInput input:focus {
        border: 0 !important;
        border-bottom: 1.5px solid #686a76 !important;
        box-shadow: none !important;
    }

    [class*="st-key-login_paper"] .stTextInput input::placeholder {
        color: #b1b2b7 !important;
    }

    /* Forgotten password */
    .paper-forgot {
        text-align: center;
        font-family: Georgia, "Times New Roman", serif;
        font-size: 11px;
        color: #777983;
        margin: 9px 0 8px;
    }

    /* Login button */
    [class*="st-key-login_paper"] .stButton {
        display: flex !important;
        justify-content: center !important;
    }

    [class*="st-key-login_paper"] .stButton > button {
        width: 78px !important;
        min-height: 31px !important;
        height: 31px !important;
        padding: 2px 10px !important;
        margin: 5px auto 0 !important;
        border-radius: 5px !important;
        border: 1px solid #b4b5bb !important;
        background: rgba(255,255,255,.65) !important;
        color: #565966 !important;
        font-family: Georgia, "Times New Roman", serif !important;
        font-size: 11px !important;
        font-weight: 500 !important;
        box-shadow: 0 2px 5px rgba(70,70,70,.12) !important;
    }

    [class*="st-key-login_paper"] .stButton > button:hover {
        background: #eef0ef !important;
        border-color: #747681 !important;
        color: #383b47 !important;
    }

    /* Create account stays below the paper */
    .create-account-wrap {
        text-align: center;
        margin-top: 10px;
    }

    .create-account-wrap button {
        font-size: 11px !important;
    }

    /* Registration panel */
    .register-panel {
        max-width: 700px;
        margin: 18px auto;
        padding: 20px;
        background: rgba(255,255,255,.90);
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(60,65,70,.16);
    }

    @media (max-width: 600px) {
        [class*="st-key-login_paper"] {
            width: 390px !important;
            padding-left: 48px !important;
            padding-right: 48px !important;
            margin-top: 20px !important;
        }
    }
    </style>
    """)

    if "show_register" not in st.session_state:
        st.session_state.show_register = False

    # Everything below is inside ONE real Streamlit container.
    # This prevents the username/password fields from escaping the paper.
    with st.container(key="login_paper", border=False):

        html("""
        <div class="paper-wing">🪽</div>
        <div class="paper-login-title">Log In</div>
        """)

        login_username = st.text_input(
            "username:",
            key="paper_login_username",
            placeholder=""
        )

        login_password = st.text_input(
            "password:",
            type="password",
            key="paper_login_password",
            placeholder=""
        )

        html('<div class="paper-forgot">forgotten password?</div>')

        login = st.button("Log In", key="paper_login_button")

        if login:
            email = login_username.strip().lower()
            password = login_password
            accounts = load_accounts()

            if not email or not password:
                st.warning("⚠️ Please enter your email and password.")
            elif email not in accounts:
                st.warning("⚠️ Account not found. Please create an account first.")
            elif accounts[email].get("password") != password_hash(password):
                st.warning("⚠️ Incorrect email or password. Please create an account if you do not have an account.")
            else:
                st.session_state.logged_in = True
                st.session_state.user = accounts[email].get("name", email.split("@")[0])
                st.success("Login successful!")
                st.rerun()

    # Optional registration
    st.markdown('<div class="create-account-wrap">', unsafe_allow_html=True)
    if st.button("Create account", key="paper_create_account"):
        st.session_state.show_register = not st.session_state.show_register
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.show_register:
        st.markdown('<div class="register-panel">', unsafe_allow_html=True)
        st.markdown(
            '<h3 style="text-align:center;color:#555866;font-family:Georgia;">Create Account</h3>',
            unsafe_allow_html=True
        )

        r1, r2 = st.columns(2)
        with r1:
            name = st.text_input("Full Name", key="paper_register_name")
            email = st.text_input("Email / Username", key="paper_register_email")
        with r2:
            password = st.text_input(
                "Password", type="password", key="paper_register_password"
            )
            confirm_password = st.text_input(
                "Confirm Password",
                type="password",
                key="paper_register_confirm"
            )

        if st.button(
            "Create account",
            key="paper_register_button",
            use_container_width=True
        ):
            email_clean = email.strip().lower()
            accounts = load_accounts()

            if not all([name.strip(), email_clean, password, confirm_password]):
                st.warning("⚠️ Please fill all fields.")
            elif "@" not in email_clean or "." not in email_clean.split("@")[-1]:
                st.warning("⚠️ Please enter a valid email address.")
            elif password != confirm_password:
                st.warning("⚠️ Passwords do not match.")
            elif len(password) < 4:
                st.warning("⚠️ Password must contain at least 4 characters.")
            elif email_clean in accounts:
                st.warning("⚠️ This account already exists. Please log in.")
            else:
                accounts[email_clean] = {
                    "name": name.strip(),
                    "password": password_hash(password)
                }
                save_accounts(accounts)
                st.session_state.logged_in = True
                st.session_state.user = name.strip()
                st.success("Account created successfully!")
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# STUDY PLANNER - MAIN APPLICATION
# Features:
# 🏠 Dashboard
# 📅 Calendar
# 📚 Subjects
# 📊 Progress
# 🤖 Study Chatbot
# ============================================================

def calculate_streak():

    if not st.session_state.completed_days:
        return 0

    current = date.today()
    streak = 0

    while current in st.session_state.completed_days:
        streak += 1
        current -= timedelta(days=1)

    return streak


# ============================================================
# ADD STUDY SESSION
# ============================================================

def add_session():

    st.markdown(
        '<div class="section-heading">'
        '➕ Add Study Session'
        '</div>',
        unsafe_allow_html=True
    )

    with st.container(border=True):

        col1, col2 = st.columns(2)

        with col1:

            subject = st.selectbox(
                "Subject",
                st.session_state.subjects,
                key="add_subject"
            )

            session_date = st.date_input(
                "Date",
                date.today(),
                key="add_date"
            )

            topic = st.text_input(
                "Topic",
                placeholder="Example: Python Loops",
                key="add_topic"
            )

        with col2:

            session_time = st.time_input(
                "Time",
                key="add_time"
            )

            duration = st.number_input(
                "Duration in minutes",
                min_value=5,
                value=45,
                step=5,
                key="add_duration"
            )

        if st.button(
            "➕ Add Study Session",
            use_container_width=True
        ):

            session = {
                "subject": subject,
                "date": session_date,
                "time": session_time.strftime("%H:%M"),
                "duration": int(duration),
                "topic": topic,
                "completed": False
            }

            st.session_state.sessions.append(session)

            st.success(
                "Study session added successfully! 🎉"
            )

            st.rerun()


# ============================================================
# SIDEBAR
# ============================================================

def app_sidebar():

    with st.sidebar:

        html("""
            <div style="
                text-align:center;
                padding:12px 0;
            ">

                <div style="font-size:43px;">
                    📚
                </div>

                <div style="
                    font-size:21px;
                    font-weight:800;
                    color:white;
                ">
                    Study Planner
                </div>

                <div style="
                    font-size:11px;
                    color:#b8b5ff;
                ">
                    Smart Study Planner
                </div>

            </div>
            """)

        st.divider()

        st.write(
            f"👋 **{st.session_state.user}**"
        )

        st.divider()

        page = st.radio(
            "MENU",
            feature_sidebar_pages()
        )

        st.divider()

        st.caption(
            "Your productivity matters 💜"
        )

        if st.button(
            "🚪 Logout",
            use_container_width=True
        ):

            st.session_state.logged_in = False
            st.session_state.user = ""

            st.rerun()

    return page


# ============================================================
# MAIN APPLICATION
# ============================================================

def study_planner():

    page = app_sidebar()

    # ========================================================
    # DASHBOARD
    # ========================================================

    if page == "🏠 Dashboard":

        hour = datetime.now().hour

        if hour < 12:
            greeting = "Good Morning"
        elif hour < 18:
            greeting = "Good Afternoon"
        else:
            greeting = "Good Evening"

        html("""
            <div class="page-title">
                🏠 Study Dashboard
            </div>

            <div class="page-subtitle">
                Your learning journey at a glance
            </div>
            """)

        html(f"""
            <div class="welcome-box">

                <h2>
                    {greeting},
                    {st.session_state.user}! 👋
                </h2>

                <p>
                    Stay consistent today and make progress
                    toward your goals.
                </p>

            </div>
            """)

        # ----------------------------------------------------
        # DASHBOARD METRICS
        # ----------------------------------------------------

        streak = calculate_streak()

        total_sessions = len(
            st.session_state.sessions
        )

        total_subjects = len(
            st.session_state.subjects
        )

        study_days = len(
            st.session_state.completed_days
        )

        col1, col2, col3, col4 = st.columns(4)

        metrics = [
            ("🔥", "Study Streak", f"{streak} days"),
            ("📚", "Subjects", total_subjects),
            ("⏱️", "Sessions", total_sessions),
            ("✅", "Study Days", study_days)
        ]

        for col, metric in zip(
            [col1, col2, col3, col4],
            metrics
        ):

            with col:

                html(f"""
                    <div class="metric-card">

                        <div class="metric-icon">
                            {metric[0]}
                        </div>

                        <div class="metric-title">
                            {metric[1]}
                        </div>

                        <div class="metric-value">
                            {metric[2]}
                        </div>

                    </div>
                    """)

        # ----------------------------------------------------
        # TODAY'S SESSIONS
        # ----------------------------------------------------

        st.markdown(
            '<div class="section-title">'
            '📅 Today\'s Sessions'
            '</div>',
            unsafe_allow_html=True
        )

        today = date.today()

        today_sessions = [
            (i, s)
            for i, s in enumerate(
                st.session_state.sessions
            )
            if s["date"] == today
        ]

        if today_sessions:

            for index, session in today_sessions:

                status = (
                    "✅ Completed"
                    if session.get(
                        "completed",
                        False
                    )
                    else "⏳ Upcoming"
                )

                html(f"""
                    <div class="session-card">

                        <div class="session-subject">
                            📚 {session["subject"]}
                        </div>

                        <div class="session-topic">
                            📝 {session["topic"] or "Study session"}
                        </div>

                        <div class="session-meta">

                            ⏰ {session["time"]}

                            &nbsp; • &nbsp;

                            ⏱️ {session["duration"]} minutes

                            &nbsp; • &nbsp;

                            {status}

                        </div>

                    </div>
                    """)

                if not session["completed"]:

                    if st.button(
                        f"✅ Complete — {session['subject']}",
                        key=f"dashboard_complete_{index}"
                    ):

                        st.session_state.sessions[
                            index
                        ]["completed"] = True

                        st.session_state.completed_days.add(
                            today
                        )

                        st.rerun()

        else:

            st.info(
                "🎉 No study sessions scheduled for today."
            )

        # ----------------------------------------------------
        # ADD SESSION
        # ----------------------------------------------------

        add_session()


    # ========================================================
    # CALENDAR
    # ========================================================

    elif page == "📅 Calendar":

        html("""
            <div class="page-title">
                📅 Study Calendar
            </div>

            <div class="page-subtitle">
                Organize your study sessions
            </div>
            """)

        selected_date = st.date_input(
            "Choose a date",
            date.today(),
            key="calendar_date"
        )

        html(f"""
            <div class="section-title">
                📅
                {selected_date.strftime("%A, %d %B %Y")}
            </div>
            """)

        sessions = [
            (i, s)
            for i, s in enumerate(
                st.session_state.sessions
            )
            if s["date"] == selected_date
        ]

        if sessions:

            for index, session in sessions:

                status = (
                    "✅ Completed"
                    if session["completed"]
                    else "⏳ Pending"
                )

                html(f"""
                    <div class="session-card">

                        <div class="session-subject">
                            📚 {session["subject"]}
                        </div>

                        <div class="session-topic">
                            📝 {session["topic"] or "Study session"}
                        </div>

                        <div class="session-meta">

                            ⏰ {session["time"]}

                            &nbsp; • &nbsp;

                            ⏱️ {session["duration"]} minutes

                            &nbsp; • &nbsp;

                            {status}

                        </div>

                    </div>
                    """)

                if not session["completed"]:

                    if st.button(
                        "✅ Mark Completed",
                        key=f"calendar_complete_{index}"
                    ):

                        st.session_state.sessions[
                            index
                        ]["completed"] = True

                        st.session_state.completed_days.add(
                            selected_date
                        )

                        st.rerun()

        else:

            st.info(
                "📭 No study sessions planned for this date."
            )


    # ========================================================
    # SUBJECTS
    # ========================================================

    elif page == "📚 Subjects":

        html("""
            <div class="page-title">
                📚 My Subjects
            </div>

            <div class="page-subtitle">
                Track your learning by subject
            </div>
            """)

        icons = [
            "🧪",
            "📖",
            "🐍",
            "💻",
            "📐",
            "🌐"
        ]

        for number, subject in enumerate(
            st.session_state.subjects
        ):

            subject_sessions = [
                s
                for s in st.session_state.sessions
                if s["subject"] == subject
            ]

            total = len(subject_sessions)

            completed = sum(
                1
                for s in subject_sessions
                if s.get(
                    "completed",
                    False
                )
            )

            percentage = (
                int(
                    completed /
                    total *
                    100
                )
                if total
                else 0
            )

            icon = icons[
                number % len(icons)
            ]

            html(f"""
                <div class="subject-card">

                    <div class="subject-name">
                        {icon} {subject}
                    </div>

                    <div class="subject-info">
                        {total} study sessions
                        &nbsp; • &nbsp;
                        {percentage}% completed
                    </div>

                </div>
                """)

            st.progress(
                percentage / 100
            )


        # Quick study overview
        today_minutes = sum(
            int(s.get("duration", 0)) for s in st.session_state.sessions
            if s.get("date") == date.today()
        )
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("🔥 Streak", f"{calculate_streak()} day(s)")
        c2.metric("⏱️ Today", f"{today_minutes} min")
        c3.metric("🎯 Daily Goal", f"{st.session_state.daily_goal_minutes} min")
        c4.metric("🏆 Pomodoros", st.session_state.pomodoro_count)

        st.divider()

        st.subheader(
            "➕ Add New Subject"
        )

        new_subject = st.text_input(
            "Subject name",
            placeholder="Example: Java",
            key="new_subject"
        )

        if st.button(
            "Add Subject",
            use_container_width=True
        ):

            new_subject = new_subject.strip()

            if (
                new_subject
                and new_subject not in
                st.session_state.subjects
            ):

                st.session_state.subjects.append(
                    new_subject
                )

                st.success(
                    "Subject added successfully! 🎉"
                )

                st.rerun()

            else:

                st.warning(
                    "Enter a new subject name."
                )


    # ========================================================
    # PROGRESS
    # ========================================================

    elif page == "📊 Progress":

        html("""
            <div class="page-title">
                📊 Study Progress
            </div>

            <div class="page-subtitle">
                Understand your study habits and performance
            </div>
            """)

        if not st.session_state.sessions:

            st.info(
                "📚 Add study sessions to see your progress."
            )

        else:

            df = pd.DataFrame(
                st.session_state.sessions
            )

            total_minutes = int(
                df["duration"].sum()
            )

            total_hours = round(
                total_minutes / 60,
                1
            )

            completed = sum(
                1
                for s in st.session_state.sessions
                if s.get(
                    "completed",
                    False
                )
            )

            total = len(
                st.session_state.sessions
            )

            rate = int(
                completed /
                total *
                100
            )

            c1, c2, c3 = st.columns(3)

            c1.metric(
                "⏱️ Study Hours",
                total_hours
            )

            c2.metric(
                "✅ Completed",
                completed
            )

            c3.metric(
                "🎯 Completion",
                f"{rate}%"
            )

            st.divider()

            # ------------------------------------------------
            # SUBJECT CHART
            # ------------------------------------------------

            subject_data = (
                df.groupby(
                    "subject"
                )["duration"]
                .sum()
                .reset_index()
            )

            fig = px.bar(
                subject_data,
                x="subject",
                y="duration",
                title="📚 Study Time by Subject",
                labels={
                    "duration": "Minutes",
                    "subject": "Subject"
                }
            )

            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            # ------------------------------------------------
            # DAILY CHART
            # ------------------------------------------------

            daily = (
                df.groupby(
                    "date"
                )["duration"]
                .sum()
                .reset_index()
            )

            fig2 = px.line(
                daily,
                x="date",
                y="duration",
                markers=True,
                title="📈 Daily Study Time",
                labels={
                    "duration": "Minutes",
                    "date": "Date"
                }
            )

            fig2.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)"
            )

            st.plotly_chart(
                fig2,
                use_container_width=True
            )


    # ========================================================
    # CHATBOT + AI STUDY MODE
    elif page == "🤖 Study Chatbot":
        html("""<div class="page-title">🤖 Study AI Assistant</div><div class="page-subtitle">Offline PDF assistant with study modes and voice tools</div>""")
        up=st.file_uploader("📄 Upload your study PDF",type=["pdf"],key="latest_pdf")
        if up:
            ok,msg=handle_pdf_upload(up)
            if not ok: st.error(msg)
        ensure_pdf_ready()
        if st.session_state.pdf_name: st.success(f"📚 {st.session_state.pdf_name} loaded — {len(st.session_state.pdf_text.split()):,} words")
        else: st.info("Upload a text-based PDF to use PDF study features.")
        st.session_state.ai_mode=st.selectbox("🧠 AI Study Mode",["Explain","Summarize","Quiz Me","Important Questions","Revision"],key="ai_mode_select")
        st.markdown("### 🎤 Voice Questions")
        st.caption("Use your browser microphone. Copy the recognized text into the chat box.")
        st.iframe("""<button id='m'>🎤 Start Voice</button><span id='s'></span><div id='r' style='margin-top:8px;padding:10px;background:#f7f5ff;border-radius:10px'>Your speech appears here.</div><script>const b=document.getElementById('m'),r=document.getElementById('r'),s=document.getElementById('s'),SR=window.SpeechRecognition||window.webkitSpeechRecognition;if(!SR){b.disabled=true;s.textContent=' Not supported'}else{const x=new SR();x.lang='en-IN';x.onstart=()=>s.textContent=' Listening...';x.onresult=e=>{r.textContent=e.results[0][0].transcript;s.textContent=' Done'};x.onerror=e=>s.textContent=' '+e.error;b.onclick=()=>x.start()}</script>""",height=100)
        for i,m in enumerate(st.session_state.chat_history):
            if m["role"]=="user": html(f'<div class="chat-user">👤 {html_lib.escape(m["text"])}</div>')
            else:
                html(f'<div class="chat-bot">🤖 {html_lib.escape(m["text"])}</div>')
                if st.button("🔊 Read Answer Aloud",key=f"speak_{i}"): speak_text(m["text"])
        question=st.chat_input("Ask a question from your PDF or study planner...")
        if question:
            st.session_state.chat_history.append({"role":"user","text":question}); mode=st.session_state.ai_mode
            if mode=="Explain": response=answer_from_pdf(question,st.session_state.pdf_text) if st.session_state.pdf_text else "Upload a PDF first."
            elif mode=="Summarize": response=("📌 **Summary**\n\n"+"\n\n".join(st.session_state.pdf_text.split("\n")[:10])) if st.session_state.pdf_text else "Upload a PDF first."
            elif mode=="Quiz Me": response=("🧠 **Quick Quiz**\n\n"+"\n".join(f"{i+1}. {item['question']}" for i,item in enumerate(generate_important_questions(st.session_state.pdf_text,5)))) if st.session_state.pdf_text else "Upload a PDF first."
            elif mode=="Important Questions": response="⭐ Open Important Questions from the sidebar."
            else: response=("🔄 **Revision Mode**\n\n"+answer_from_pdf(question,st.session_state.pdf_text)) if st.session_state.pdf_text else "Upload a PDF first."
            st.session_state.chat_history.append({"role":"bot","text":response}); award("First Question","💬","Asked your first study question")
            if sum(1 for m in st.session_state.chat_history if m["role"]=="user")>=10: award("10 Questions","🎯","Asked 10 study questions")
            st.rerun()

    # ========================================================
    # PDF TO SUMMARY
    elif page == "📄 PDF Summary":
        html("""<div class="page-title">📄 PDF to Summary</div><div class="page-subtitle">Turn your uploaded study PDF into quick revision notes — completely offline</div>""")
        up=st.file_uploader("📄 Upload a study PDF", type=["pdf"], key="summary_pdf_uploader")
        if up:
            ok,msg=handle_pdf_upload(up)
            if not ok: st.error(msg)
        ensure_pdf_ready()
        if not st.session_state.pdf_text:
            st.info("Upload a text-based PDF to generate its summary.")
        else:
            st.success(f"📚 {st.session_state.pdf_name} loaded")
            if st.button("🔄 Regenerate Summary", use_container_width=True):
                st.session_state.pdf_summary=create_pdf_summary(st.session_state.pdf_text)
                st.rerun()
            st.markdown("### 📌 Quick Revision Summary")
            st.markdown(st.session_state.pdf_summary or create_pdf_summary(st.session_state.pdf_text))
            st.download_button(
                "⬇️ Download Summary",
                data=(st.session_state.pdf_summary or create_pdf_summary(st.session_state.pdf_text)),
                file_name="study_summary.txt",
                mime="text/plain",
                use_container_width=True
            )

    # ========================================================
    # AUTOMATIC PDF QUIZ
    elif page == "🧠 PDF Quiz":
        html("""<div class="page-title">🧠 Automatic PDF Quiz</div><div class="page-subtitle">Generate multiple-choice questions directly from your uploaded PDF</div>""")
        up=st.file_uploader("📄 Upload a study PDF", type=["pdf"], key="quiz_pdf_uploader")
        if up:
            ok,msg=handle_pdf_upload(up)
            if not ok: st.error(msg)
        ensure_pdf_ready()

        if not st.session_state.pdf_text:
            st.info("Upload a PDF to generate your quiz.")
        elif not st.session_state.pdf_quiz:
            st.warning("I could not build reliable questions from this PDF. The quiz needs at least four "
                       "definitions or question-and-answer pairs (for example: 'A variable is a name that stores a value'). "
                       "Try a text-based PDF with more study content.")
        else:
            quiz = st.session_state.pdf_quiz
            qid = st.session_state.quiz_id
            submitted = st.session_state.quiz_submitted

            st.success(f"📚 {st.session_state.pdf_name} — {len(quiz)} questions generated")
            st.caption("Every correct answer is copied from your PDF. No API is used.")

            if submitted:
                score = st.session_state.quiz_score
                total = len(quiz)
                percentage = round(score / total * 100) if total else 0
                st.success(f"🎉 Score: {score}/{total} ({percentage}%)")
                if st.session_state.pop("quiz_celebrate", False):
                    st.balloons()

            for i, q in enumerate(quiz):
                st.markdown(f"### Question {i+1}")
                st.markdown(_md_safe(q["question"]))
                choice = st.radio(
                    "Choose one answer:",
                    q["options"],
                    key=f"pdf_quiz_{qid}_{i}",
                    index=None,
                    disabled=submitted,
                    format_func=_md_safe,
                )
                st.session_state.quiz_answers[i] = choice

                if submitted:
                    if choice == q["answer"]:
                        st.success("✅ Correct")
                    else:
                        st.error("❌ Not answered" if not choice else "❌ Not correct")
                        st.info("✔ Correct answer: " + _md_safe(q["answer"]))
                    if q.get("explanation"):
                        st.caption("📖 From your PDF: " + _md_safe(q["explanation"]))
                st.divider()

            if not submitted:
                answered = sum(1 for i in range(len(quiz)) if st.session_state.quiz_answers.get(i))
                st.caption(f"Answered {answered} of {len(quiz)} questions")
                if st.button("✅ Submit Quiz", use_container_width=True):
                    score = 0
                    for i, q in enumerate(quiz):
                        selected = st.session_state.quiz_answers.get(i)
                        if selected == q["answer"]:
                            score += 1
                            continue

                        # Save incorrect / unanswered questions for later revision.
                        item = {
                            "question": q["question"],
                            "selected": selected,
                            "answer": q["answer"],
                            "pdf": st.session_state.pdf_name or "PDF Quiz"
                        }
                        already = [
                            saved for saved in st.session_state.mistake_review
                            if saved.get("question") == item["question"]
                            and saved.get("pdf") == item["pdf"]
                        ]
                        if not already:
                            st.session_state.mistake_review.append(item)

                    st.session_state.quiz_score = score
                    st.session_state.quiz_submitted = True
                    st.session_state.quiz_celebrate = (round(score / len(quiz) * 100) >= 80) if quiz else False
                    award("PDF Quiz Starter","🧠","Completed an automatic PDF quiz")
                    st.rerun()

            if st.button("🔄 Generate New Quiz", use_container_width=True):
                new_quiz = generate_pdf_quiz(st.session_state.pdf_text, limit=10)
                if new_quiz:
                    st.session_state.pdf_quiz = new_quiz
                st.session_state.quiz_id += 1          # fresh widget keys -> no leftover selections
                st.session_state.quiz_answers = {}
                st.session_state.quiz_submitted = False
                st.session_state.quiz_score = 0
                st.rerun()

    # ========================================================
    # POMODORO TIMER
    elif page == "⏱️ Pomodoro Timer":
        html("""<div class="page-title">⏱️ Pomodoro Study Timer</div>
        <div class="page-subtitle">Focus deeply, take breaks, and record your study time</div>""")
        render_pomodoro_timer()
        st.markdown("---")
        st.metric("Pomodoros Completed", st.session_state.pomodoro_count,
                  f"{st.session_state.pomodoro_minutes} total minutes")

    # ========================================================
    # DAILY GOALS
    elif page == "🎯 Daily Goals":
        html("""<div class="page-title">🎯 Daily Goals</div>
        <div class="page-subtitle">Set a target and track today's study progress</div>""")
        render_daily_goals()

    # ========================================================
    # STUDY ANALYTICS
    elif page == "📈 Study Analytics":
        html("""<div class="page-title">📈 Study Analytics</div>
        <div class="page-subtitle">Understand your study time, consistency, and subject focus</div>""")
        render_analytics()

    # ========================================================
    # SMART SCHEDULE
    elif page == "📅 Smart Schedule":
        html("""<div class="page-title">📅 Smart Study Schedule</div>
        <div class="page-subtitle">Build a balanced timetable from your available study time</div>""")
        render_smart_schedule()

    # ========================================================
    # MISTAKE REVIEW
    elif page == "🔁 Mistake Review":
        html("""<div class="page-title">🔁 Mistake Review</div>
        <div class="page-subtitle">Review questions you answered incorrectly in PDF quizzes</div>""")
        render_mistake_review()

    # ========================================================
    # ACHIEVEMENTS
    elif page == "🏆 Achievements":
        html("""<div class="page-title">🏆 Achievements</div><div class="page-subtitle">Your study milestones</div>""")
        qcount=sum(1 for m in st.session_state.chat_history if m["role"]=="user")
        if qcount>=1: award("First Question","💬","Asked your first question")
        if qcount>=10: award("10 Questions","🎯","Asked 10 study questions")
        if calculate_streak()>=7: award("7 Day Streak","🔥","Studied for seven consecutive days")
        if not st.session_state.achievements: st.info("Complete study activities to unlock badges.")
        for a in st.session_state.achievements: html(f'<div class="glass-card"><div class="card-title">{a["icon"]} {a["name"]}</div><div class="card-text">{a["description"]}</div></div>')

    elif page == "📝 Personal Notes":
        html("""<div class="page-title">📝 Personal Notes</div><div class="page-subtitle">Create and search your revision notes</div>""")
        with st.form("note_form"):
            subject=st.selectbox("Subject",st.session_state.subjects); title=st.text_input("Note title"); body=st.text_area("Your note",height=150); save=st.form_submit_button("💾 Save Note",use_container_width=True)
        if save and body.strip(): st.session_state.notes.append({"subject":subject,"title":title or "Untitled Note","body":body,"time":datetime.now().strftime("%d-%m-%Y %H:%M")});award("First Note","📝","Created your first personal note");st.success("Note saved!")
        search=st.text_input("🔎 Search notes")
        for i,n in enumerate(reversed(st.session_state.notes)):
            if search and search.lower() not in (n["title"]+" "+n["body"]+" "+n["subject"]).lower(): continue
            with st.expander(f"{n['subject']} — {n['title']}"): st.write(n["body"]);st.caption(n["time"])

    # ========================================================
    # IMPORTANT QUESTIONS
    elif page == "⭐ Important Questions":
        html("""<div class="page-title">⭐ Important Questions</div>
        <div class="page-subtitle">Question and answer pairs taken from your uploaded PDF</div>""")

        if not ensure_pdf_ready():
            st.info("📄 Upload a PDF in Study Chatbot first.")
        else:
            pdf_text = st.session_state.pdf_text
            st.success(f"📚 PDF loaded: {st.session_state.pdf_name}")

            if st.button("🔄 Show Next Set of Questions", use_container_width=True):
                st.session_state.important_offset = st.session_state.get("important_offset", 0) + 10
                st.session_state.important_questions = generate_important_questions(
                    pdf_text, limit=10, offset=st.session_state.important_offset)
                st.rerun()

            questions = st.session_state.get("important_questions", [])
            if not questions:
                st.warning("The PDF was loaded, but no reliable question-and-answer pairs were found. "
                           "Important Questions needs definitions ('X is ...'), a question list, "
                           "or question-and-answer text in the PDF.")
            else:
                for i, item in enumerate(questions, start=1):
                    st.markdown(f"### ⭐ {i}. {_md_safe(item.get('question', ''))}")
                    st.markdown("**📝 Answer:** " + _md_safe(item.get("answer", "")))
                    if item.get("section"):
                        st.caption(f"📍 From section: {item['section']}")

                    if st.button("🔖 Save", key=f"important_save_{i}_{st.session_state.get('important_offset', 0)}"):
                        if item not in st.session_state.saved_important:
                            st.session_state.saved_important.append(item)
                        award("Important Question", "⭐", "Saved an important revision question")
                        st.success("Question saved!")

                    st.divider()


# ============================================================
# RUN STUDY PLANNER AFTER LOGIN
# ============================================================
inject_css()

if st.session_state.logged_in:

    study_planner() 
else:
    login_page()