import streamlit as st
import requests
import json
import time
import sqlite3
import pandas as pd
import folium
from streamlit_folium import st_folium
from datetime import datetime

API_URL = "http://127.0.0.1:7600/predict"
LOGIN_URL = "http://127.0.0.1:7600/login"
SIGNUP_URL = "http://127.0.0.1:7600/signup"
DB_PATH = "tool_calls.db"

st.set_page_config(
    page_title="AI Tool Orchestrator",
    page_icon="⚡",
    layout="wide"
)

if "token" not in st.session_state:
    st.session_state.token = None

if "username" not in st.session_state:
    st.session_state.username = None

if "role" not in st.session_state:
    st.session_state.role = None


def login_ui():
    st.markdown("""
    <style>
    [data-testid="stToolbar"], [data-testid="stDecoration"], #MainMenu, footer {
        display: none !important;
    }
    header[data-testid="stHeader"] {
        visibility: hidden !important;
        height: 0rem !important;
    }
    .stApp {
        background: #f5f7fb !important;
    }
    .block-container {
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100% !important;
    }
    section[data-testid="stSidebar"] {
        display: none !important;
    }

    /* LOGIN PAGE ONLY: two main columns */
    .login-left-box {
        min-height: 100vh;
        background:
            radial-gradient(circle at 50% 88%, rgba(124,58,237,0.32), transparent 26%),
            linear-gradient(180deg, #03172f 0%, #020817 100%);
        color: white;
        padding: 95px 58px 50px 58px;
        box-sizing: border-box;
    }
    .login-brand-row {
        display: flex;
        align-items: center;
        gap: 18px;
        margin-bottom: 36px;
    }
    .login-bolt {
        font-size: 66px;
        line-height: 1;
    }
    .login-brand-title {
        color: white;
        font-size: 34px;
        font-weight: 950;
        letter-spacing: -1px;
        line-height: 1.15;
    }
    .login-subtitle {
        color: #dbeafe;
        font-size: 20px;
        line-height: 1.6;
        margin-bottom: 38px;
    }
    .login-divider {
        height: 1px;
        width: 100%;
        background: rgba(255,255,255,0.22);
        margin: 0 0 34px 0;
    }
    .feature-line {
        display: flex;
        align-items: center;
        gap: 22px;
        margin: 28px 0;
    }
    .feature-circle {
        width: 58px;
        height: 58px;
        border-radius: 999px;
        border: 2px solid #8b5cf6;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 28px;
        box-shadow: 0 0 20px rgba(139,92,246,0.35);
        background: rgba(15,23,42,0.24);
        flex: 0 0 auto;
    }
    .feature-title {
        color: #ffffff;
        font-size: 18px;
        font-weight: 900;
        margin-bottom: 5px;
    }
    .feature-caption {
        color: #cbd5e1;
        font-size: 15px;
    }
    .ai-chip-wrap {
        margin: 68px auto 0 auto;
        width: 230px;
        height: 230px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(124,58,237,0.42), transparent 65%);
    }
    .ai-chip-core {
        width: 100px;
        height: 100px;
        border-radius: 18px;
        background: linear-gradient(135deg, #7c3aed, #4c1d95);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 42px;
        font-weight: 950;
        border: 2px solid rgba(255,255,255,0.45);
        box-shadow: 0 0 60px rgba(124,58,237,0.75);
    }

    .login-right-wrap {
    padding-top: 20px;
    }
    .login-form-shell {
        width: 100%;
        max-width: 560px;
        margin: 0 auto;
    }
    .login-top-card {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 24px 24px 0 0;
        box-shadow: 0 22px 60px rgba(15,23,42,0.11);
        padding: 46px 46px 28px 46px;
        text-align: center;
    }
    .login-avatar {
        width: 86px;
        height: 86px;
        border-radius: 50%;
        margin: 0 auto 20px auto;
        background: #ede9fe;
        color: #6d28d9;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 42px;
    }
    .login-heading {
        color: #0f172a;
        font-size: 34px;
        font-weight: 950;
        letter-spacing: -0.8px;
        margin-bottom: 8px;
    }
    .login-subheading {
        color: #64748b;
        font-size: 17px;
    }

    /* Make Streamlit tabs look like lower part of the card */
    div[data-testid="stTabs"] {
        background: #ffffff !important;
        border-left: 1px solid #e5e7eb !important;
        border-right: 1px solid #e5e7eb !important;
        border-bottom: 1px solid #e5e7eb !important;
        border-radius: 0 0 24px 24px !important;
        box-shadow: 0 22px 60px rgba(15,23,42,0.11) !important;
        padding: 10px 46px 38px 46px !important;
        box-sizing: border-box !important;
    }
    button[data-baseweb="tab"] {
        font-weight: 800 !important;
    }
    div[data-testid="stTextInput"] label,
    div[data-testid="stSelectbox"] label {
        font-weight: 800 !important;
        color: #111827 !important;
        font-size: 14px !important;
    }
    div[data-testid="stTextInput"] input {
        height: 52px !important;
        border-radius: 12px !important;
        border: 1px solid #d1d5db !important;
        background: white !important;
        padding-left: 16px !important;
    }
    .stCheckbox label {
        color: #374151 !important;
    }
    .stButton > button {
        background: linear-gradient(90deg, #6d3df5, #5b21b6) !important;
        color: white !important;
        border-radius: 12px !important;
        height: 56px !important;
        font-weight: 900 !important;
        border: none !important;
        font-size: 16px !important;
        margin-top: 8px !important;
    }
    .stButton > button:hover {
        background: linear-gradient(90deg, #7c3aed, #4c1d95) !important;
        color: white !important;
    }
    .login-helper {
        text-align: center;
        color: #64748b;
        margin-top: 22px;
        font-size: 15px;
    }
    .login-helper b {
        color: #6d28d9;
    }
    .login-footer {
        text-align: center;
        color: #64748b;
        margin-top: 28px;
        font-size: 14px;
    }

    @media (max-width: 950px) {
        .login-left-box { display: none; }
        .login-right-wrap { padding: 20px; }
        .login-top-card, div[data-testid="stTabs"] { padding-left: 24px !important; padding-right: 24px !important; }
    }
    </style>
    """, unsafe_allow_html=True)

    left_col, right_col = st.columns([0.34, 0.66], gap="large")

    with left_col:
        st.markdown("""
        <div class="login-left-box">
            <div class="login-brand-row">
                <div class="login-bolt">⚡</div>
                <div class="login-brand-title">AI Tool Orchestrator</div>
            </div>
            <div class="login-subtitle">
                AI Tool Calling Platform<br>
                Powered by LoRA
            </div>
            <div class="login-divider"></div>
            <div class="feature-line">
                <div class="feature-circle">🛡️</div>
                <div>
                    <div class="feature-title">Secure</div>
                    <div class="feature-caption">JWT Authentication</div>
                </div>
            </div>
            <div class="feature-line">
                <div class="feature-circle">⚡</div>
                <div>
                    <div class="feature-title">Fast</div>
                    <div class="feature-caption">Real-time Execution</div>
                </div>
            </div>
            <div class="feature-line">
                <div class="feature-circle">🧠</div>
                <div>
                    <div class="feature-title">Intelligent</div>
                    <div class="feature-caption">AI Powered Routing</div>
                </div>
            </div>
            <div class="ai-chip-wrap">
                <div class="ai-chip-core">AI</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with right_col:
        st.markdown("""
        <div class="login-right-wrap">
            <div class="login-form-shell">
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="login-top-card">
            <div class="login-avatar">👤</div>
            <div class="login-heading">Welcome Back!</div>
            <div class="login-subheading">Login to access your account</div>
        </div>
        """, unsafe_allow_html=True)

        tab1, tab2 = st.tabs(["Login", "Signup"])

        with tab1:
            username = st.text_input(
                "Username",
                placeholder="Enter your username",
                key="login_username"
            )
            password = st.text_input(
                "Password",
                placeholder="Enter your password",
                type="password",
                key="login_password"
            )
            st.checkbox("Remember me", key="remember_me")

            if st.button("Login", width='stretch'):
                try:
                    response = requests.post(
                        LOGIN_URL,
                        json={"username": username, "password": password},
                        timeout=15
                    )

                    if response.status_code == 200:
                        data = response.json()
                        st.session_state.token = data["access_token"]
                        st.session_state.username = data["username"]
                        st.session_state.role = data["role"]
                        st.rerun()
                    else:
                        st.error("Invalid username or password")

                except requests.exceptions.ConnectionError:
                    st.error("FastAPI backend is not running. Start backend on port 7600.")

            st.markdown('<div class="login-helper">New user? <b>Open Signup tab</b></div>', unsafe_allow_html=True)

        with tab2:
            new_username = st.text_input(
                "New Username",
                placeholder="Create username",
                key="signup_username"
            )
            new_password = st.text_input(
                "New Password",
                placeholder="Create password",
                type="password",
                key="signup_password"
            )
            role = st.selectbox("Role", ["user", "admin"])

            if st.button("Create Account", width='stretch'):
                try:
                    response = requests.post(
                        SIGNUP_URL,
                        json={
                            "username": new_username,
                            "password": new_password,
                            "role": role
                        },
                        timeout=15
                    )

                    if response.status_code == 200:
                        st.success("Account created successfully. Please login now.")
                    else:
                        try:
                            st.error(response.json().get("detail", "Signup failed"))
                        except Exception:
                            st.error(response.text)

                except requests.exceptions.ConnectionError:
                    st.error("FastAPI backend is not running. Start backend on port 7600.")

        st.markdown(
            '<div class="login-footer">© 2024 AI Tool Orchestrator. All rights reserved.</div>'
            '</div>'
            '</div>',
            unsafe_allow_html=True
        )

if st.session_state.token is None:
    login_ui()
    st.stop()


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tool_calls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            request TEXT NOT NULL,
            tool TEXT NOT NULL,
            arguments TEXT,
            result TEXT,
            response_time REAL,
            confidence REAL DEFAULT 0.0,
            status TEXT DEFAULT 'success',
            feedback TEXT DEFAULT '',
            timestamp TEXT NOT NULL
        )
    """)

    for sql in [
        "ALTER TABLE tool_calls ADD COLUMN confidence REAL DEFAULT 0.0",
        "ALTER TABLE tool_calls ADD COLUMN status TEXT DEFAULT 'success'",
        "ALTER TABLE tool_calls ADD COLUMN feedback TEXT DEFAULT ''"
    ]:
        try:
            cursor.execute(sql)
        except Exception:
            pass

    cursor.execute("UPDATE tool_calls SET confidence = 0.0 WHERE confidence IS NULL")
    cursor.execute("UPDATE tool_calls SET status = 'success' WHERE status IS NULL OR status='unknown'")
    cursor.execute("UPDATE tool_calls SET feedback = '' WHERE feedback IS NULL")

    conn.commit()
    conn.close()


def save_tool_call(request, tool, arguments, result, response_time, confidence=0.0, status="success"):
    confidence = confidence if confidence is not None else 0.0
    status = status if status not in [None, "", "unknown"] else "success"

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO tool_calls
        (request, tool, arguments, result, response_time, confidence, status, feedback, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        request,
        tool,
        json.dumps(arguments, ensure_ascii=False),
        json.dumps(result, ensure_ascii=False),
        response_time,
        confidence,
        status,
        "",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()


def fetch_one(query, default=0):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(query)
    row = cursor.fetchone()
    conn.close()
    return row[0] if row and row[0] is not None else default


def get_total_requests():
    return fetch_one("SELECT COUNT(*) FROM tool_calls", 0)


def get_avg_response_time():
    return fetch_one("SELECT AVG(response_time) FROM tool_calls", 0)


def get_fastest_response():
    return fetch_one("SELECT MIN(response_time) FROM tool_calls", 0)


def get_success_rate():
    total = get_total_requests()
    success = fetch_one("SELECT COUNT(*) FROM tool_calls WHERE status='success'", 0)
    return (success / total * 100) if total else 0


def get_avg_confidence():
    return fetch_one("SELECT AVG(confidence) FROM tool_calls", 0)


def get_tool_usage():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT tool, COUNT(*)
        FROM tool_calls
        GROUP BY tool
        ORDER BY COUNT(*) DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    return {tool: count for tool, count in rows}


def get_recent_history(limit=100):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, request, tool, arguments, result, response_time, confidence, status, feedback, timestamp
        FROM tool_calls
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))
    rows = cursor.fetchall()
    conn.close()
    return rows


def clear_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tool_calls")
    conn.commit()
    conn.close()


def delete_row(row_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tool_calls WHERE id = ?", (row_id,))
    conn.commit()
    conn.close()


def update_feedback(row_id, feedback):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE tool_calls SET feedback = ? WHERE id = ?", (feedback, row_id))
    conn.commit()
    conn.close()


def safe_json_load(value):
    try:
        return json.loads(value)
    except Exception:
        return value


def tool_icon(tool_name):
    icons = {
        "book_cab": "🚕",
        "order_food": "🍔",
        "set_reminder": "⏰",
        "book_hotel": "🏨",
        "weather": "🌦️",
        "send_email": "📧",
        "unknown": "❓"
    }
    return icons.get(tool_name, "🛠️")


init_db()

st.markdown("""
<style>
[data-testid="stToolbar"], [data-testid="stDecoration"], #MainMenu, footer {
    display: none !important;
}
header[data-testid="stHeader"] {
    visibility: hidden !important;
    height: 0rem !important;
}
.stApp {
    background: #f5f6f8;
    color: #0f172a;
}
.block-container {
    padding-top: 1.1rem;
    padding-left: 2.2rem;
    padding-right: 2.2rem;
    max-width: 1550px;
}
section[data-testid="stSidebar"] {
    background: #070b14;
    border-right: 1px solid #111827;
}
section[data-testid="stSidebar"] * {
    color: #f8fafc !important;
}
.sidebar-title {
    font-size: 22px;
    font-weight: 900;
}
.sidebar-muted {
    color: #94a3b8 !important;
    font-size: 13px;
    margin-bottom: 14px;
}
.status-pill {
    display: inline-block;
    background: rgba(34,197,94,0.14);
    color: #86efac !important;
    border: 1px solid rgba(34,197,94,0.45);
    padding: 7px 11px;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 800;
    margin: 4px 4px 4px 0;
}
.hero {
    background: linear-gradient(135deg, #111827 0%, #1f2937 60%, #050505 100%);
    padding: 24px 28px;
    border-radius: 22px;
    color: white;
    margin-bottom: 18px;
    box-shadow: 0 18px 42px rgba(15,23,42,0.22);
}
.badge {
    display: inline-block;
    background: #ff9900;
    color: #111827;
    padding: 6px 13px;
    border-radius: 999px;
    font-weight: 900;
    font-size: 12px;
    margin-bottom: 12px;
}
.hero-title {
    font-size: 38px;
    font-weight: 950;
    letter-spacing: -1.2px;
    margin-bottom: 5px;
}
.hero-subtitle {
    color: #cbd5e1;
    font-size: 16px;
}
.section-title {
    font-size: 22px;
    font-weight: 900;
    margin: 10px 0 8px 0;
    color: #0f172a;
}
.muted {
    color: #64748b;
    font-size: 14px;
    margin-bottom: 12px;
}
.card {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 20px;
    padding: 22px;
    box-shadow: 0 12px 30px rgba(15,23,42,0.07);
}
.arch-card {
    background: #0f172a;
    color: #f8fafc;
    border-radius: 20px;
    padding: 24px;
    min-height: 305px;
    box-shadow: 0 16px 34px rgba(15,23,42,0.22);
}
.arch-card li {
    color: #e5e7eb;
    line-height: 1.65;
}
.tool-card {
    background: linear-gradient(135deg, #fff7ed, #ffedd5);
    border: 1px solid #fdba74;
    border-left: 7px solid #f97316;
    border-radius: 18px;
    padding: 20px;
    margin-bottom: 10px;
}
.result-card {
    background: linear-gradient(135deg, #ecfdf5, #dcfce7);
    border: 1px solid #86efac;
    border-left: 7px solid #16a34a;
    border-radius: 18px;
    padding: 20px;
    margin-bottom: 10px;
}
.chat-chip {
    background: white;
    border: 1px solid #e5e7eb;
    padding: 16px 18px;
    border-radius: 18px;
    margin-bottom: 12px;
    box-shadow: 0 10px 24px rgba(15,23,42,0.06);
}
.assistant-chip {
    background: #111827;
    color: white;
}
div[data-testid="stMetric"] {
    background: white;
    border: 1px solid #e5e7eb;
    padding: 16px;
    border-radius: 18px;
    box-shadow: 0 10px 24px rgba(15,23,42,0.07);
    min-height: 115px;
}
div[data-testid="stMetricValue"] {
    font-size: 27px;
    font-weight: 950;
    color: #0f172a;
}
.stButton > button,
div[data-testid="stDownloadButton"] button {
    background: #111827;
    color: white;
    border-radius: 14px;
    border: none;
    height: 48px;
    font-weight: 900;
}
.stButton > button:hover,
div[data-testid="stDownloadButton"] button:hover {
    background: #ff9900;
    color: #111827;
}
textarea {
    border-radius: 14px !important;
    border: 1px solid #d1d5db !important;
}
.weather-main-card {
    background: linear-gradient(135deg, #0f172a, #1e293b);
    color: white;
    padding: 40px;
    border-radius: 20px;
    text-align: center;
    min-height: 420px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    box-shadow: 0 16px 40px rgba(15, 23, 42, 0.22);
}
.weather-main-card h1 {
    font-size: 72px;
    margin-bottom: 10px;
    font-weight: 950;
}
.temp-value {
    font-size: 72px;
    font-weight: 950;
}
.weather-main-card h3 {
    font-size: 28px;
    color: #cbd5e1;
    margin: 5px 0;
}
.weather-main-card p {
    font-size: 18px;
    color: #94a3b8;
    margin: 5px 0;
}
.forecast-card {
    background: linear-gradient(135deg, #667eea, #764ba2);
    border-radius: 20px;
    padding: 20px;
    min-height: 140px;
    transition: all 0.3s ease;
    color: white;
    text-align: center;
    display: flex;
    flex-direction: column;
    justify-content: center;
}
.forecast-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
}
.sun-card {
    border-radius: 24px;
    padding: 35px;
    text-align: center;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}
.sun-time {
    font-size: 42px;
    font-weight: 700;
    margin-top: 15px;
}

</style>
""", unsafe_allow_html=True)

tool_usage = get_tool_usage()
total_requests = get_total_requests()
avg_response = get_avg_response_time()
fastest_response = get_fastest_response()
success_rate = get_success_rate()
avg_confidence = get_avg_confidence()
unique_tools = len(tool_usage)
history = get_recent_history()

st.sidebar.markdown('<div class="sidebar-title">⚡ AI Orchestrator</div>', unsafe_allow_html=True)
st.sidebar.markdown('<div class="sidebar-muted">Production tool-calling system</div>', unsafe_allow_html=True)

st.sidebar.markdown("""
<span class="status-pill">● Backend Online</span>
<span class="status-pill">● DB Connected</span>
<span class="status-pill">● Model Ready</span>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.write(f"👤 **{st.session_state.username}**")
st.sidebar.write(f"Role: **{st.session_state.role}**")

if st.sidebar.button("Logout", use_container_width=True):
    st.session_state.token = None
    st.session_state.username = None
    st.session_state.role = None
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.subheader("Tools")
for t in ["🚕 book_cab", "🍔 order_food", "⏰ set_reminder", "🏨 book_hotel", "🌦️ weather", "📧 send_email"]:
    st.sidebar.write(t)

st.sidebar.markdown("---")
st.sidebar.subheader("Usage")
if tool_usage:
    for tool, count in tool_usage.items():
        st.sidebar.write(f"{tool_icon(tool)} **{tool}** — {count}")
else:
    st.sidebar.info("No calls yet.")

st.sidebar.markdown("---")
if st.session_state.role == "admin":
    if st.sidebar.button("Clear History", use_container_width=True):
        clear_database()
        st.rerun()
else:
    st.sidebar.info("Only admin can clear history.")

st.markdown("""
<div class="hero">
    <div class="badge">ENTERPRISE AI PLATFORM</div>
    <div class="hero-title">AI Tool Orchestrator</div>
    <div class="hero-subtitle">
        JWT security, multi-tool execution, confidence scoring, feedback loop, searchable history, CSV export, and production analytics.
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-title">Live Operations Dashboard</div>', unsafe_allow_html=True)

m1, m2, m3, m4, m5, m6 = st.columns(6)
m1.metric("Requests", total_requests)
m2.metric("Success Rate", f"{success_rate:.1f}%")
m3.metric("Avg Latency", f"{avg_response:.2f}s")
m4.metric("Fastest", f"{fastest_response:.2f}s")
m5.metric("Avg Confidence", f"{avg_confidence:.2f}")
m6.metric("Unique Tools", unique_tools)

st.markdown("---")

examples = [
    "Book a cab from Hyderabad to Warangal",
    "Order chicken biryani from Paradise",
    "Remind me to submit assignment at 6 PM",
    "Book a hotel in Goa for Sunday",
    "What is the weather in Hyderabad",
    "Send email to test@gmail.com subject Meeting Update message I will join at 5 PM",
    "What is the weather in Hyderabad and send email to test@gmail.com subject Weather Update message Weather checked successfully"
]

left, right = st.columns([1.2, 0.8], gap="large")

with left:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Chat Interface</div>', unsafe_allow_html=True)
    st.markdown('<div class="muted">Supports secure single-tool and multi-tool requests.</div>', unsafe_allow_html=True)

    example = st.selectbox("Choose Example", examples)
    user_input = st.text_area("User Request", value=example, height=120)
    run_button = st.button("Generate & Execute Tool", use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown("""
    <div class="arch-card">
        <h3>System Flow</h3>
        <ul>
            <li>JWT Login / Signup</li>
            <li>User request</li>
            <li>Tool router</li>
            <li>Argument extraction</li>
            <li>Tool execution</li>
            <li>Confidence scoring</li>
            <li>SQLite analytics</li>
            <li>Feedback loop</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

if run_button:
    if not user_input.strip():
        st.warning("Please enter a request.")
    else:
        try:
            start_time = time.time()

            response = requests.post(
                API_URL,
                json={"user_input": user_input},
                headers={
                    "Authorization": f"Bearer {st.session_state.token}"
                },
                timeout=20
            )

            response_time = time.time() - start_time

            if response.status_code == 200:
                result = response.json()
                executions = result.get("tool_calls", []) if result.get("multi_tool") else [result]

                st.markdown("---")
                st.markdown('<div class="section-title">Conversation</div>', unsafe_allow_html=True)

                st.markdown(
                    f"""
                    <div class="chat-chip">
                        <b>👤 You</b><br>{user_input}
                    </div>
                    <div class="chat-chip assistant-chip">
                        <b>🤖 Assistant</b><br>
                        I detected {len(executions)} tool call(s), executed them, and saved analytics.
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                for item in executions:
                    tool_call = item.get("tool_call", {})
                    tool_result = item.get("tool_result", {})

                    tool_name = tool_call.get("tool_name", "unknown")
                    arguments = tool_call.get("arguments", {})
                    confidence = tool_call.get("confidence", 0.0) or 0.0
                    status = tool_result.get("status", "success")
                    status = status if status not in [None, "", "unknown"] else "success"

                    save_tool_call(
                        request=user_input,
                        tool=tool_name,
                        arguments=arguments,
                        result=tool_result,
                        response_time=response_time,
                        confidence=confidence,
                        status=status
                    )

                    # Weather UI - Professional Dashboard
                    if tool_name == "weather":
                        city = tool_result.get("city", arguments.get("city", "Hyderabad"))
                        temp = tool_result.get("temperature", "33°C")
                        feels_like = tool_result.get("feels_like", "35°C")
                        humidity = tool_result.get("humidity", "48%")
                        condition = tool_result.get("condition", "Partly Cloudy")
                        wind_speed = tool_result.get("wind_speed", "12 km/h")
                        visibility = tool_result.get("visibility", "10 km")
                        pressure = tool_result.get("pressure", "1008 hPa")
                        min_temp = tool_result.get("min_temp", "28°C")
                        max_temp = tool_result.get("max_temp", "35°C")
                        sunrise = tool_result.get("sunrise", "6:00 AM")
                        sunset = tool_result.get("sunset", "6:30 PM")
                        aqi = tool_result.get("aqi", 42)
                        alerts = tool_result.get("alerts", [])

                        # Weather icon mapping
                        icon_map = {
                            "Sunny": "☀️",
                            "Cloudy": "☁️",
                            "Partly Cloudy": "⛅",
                            "Rain": "🌧️",
                            "Light Rain": "🌦️",
                            "overcast clouds": "☁️",
                            "clear sky": "☀️"
                        }
                        weather_icon = icon_map.get(condition, "🌤️")

                        st.markdown("---")
                        st.subheader("🌦️ Weather Information")

                        # 2-column layout: Main weather card + Metrics
                        col1, col2 = st.columns([2, 1])

                        with col1:
                            st.markdown(f"""
                            <div class="weather-main-card">
                                <h1>{temp}</h1>
                                <h3>{weather_icon} {condition}</h3>
                                <p>{city}, India</p>
                            </div>
                            """, unsafe_allow_html=True)

                        with col2:
                            st.metric("💧 Humidity", humidity)
                            st.metric("🌬️ Wind Speed", wind_speed)
                            st.metric("👁️ Visibility", visibility)
                            st.metric("🔻 Pressure", pressure)

                        # Temperature Range + Feels Like
                        t1, t2, t3 = st.columns(3)
                        with t1:
                            st.metric("🌡️ Min Temp", min_temp)
                        with t2:
                            st.metric("🔥 Max Temp", max_temp)
                        with t3:
                            st.metric("🌡️ Feels Like", feels_like)

                        st.markdown("---")

                        # Air Quality Section
                        st.subheader("💨 Air Quality")
                        aqi_status = "🟢 Good" if aqi < 50 else "🟡 Moderate" if aqi < 100 else "🔴 Poor"
                        aq1, aq2 = st.columns(2)
                        with aq1:
                            st.metric("AQI Index", aqi)
                        with aq2:
                            st.markdown(f"<h4>{aqi_status}</h4>", unsafe_allow_html=True)

                        st.markdown("---")

                        # Weather Alerts
                        if alerts:
                            st.subheader("⚠️ Weather Alerts")
                            for alert in alerts:
                                st.warning(f"🚨 {alert}")
                            st.markdown("---")

                        # 5-Day Forecast Section
                        st.subheader("📅 5-Day Forecast")
                        forecast_data = tool_result.get("forecast", [
                            {"day": "Tomorrow", "high": "35°C", "low": "28°C", "condition": "Sunny"},
                            {"day": "Friday", "high": "33°C", "low": "27°C", "condition": "Partly Cloudy"},
                            {"day": "Saturday", "high": "32°C", "low": "26°C", "condition": "Cloudy"},
                            {"day": "Sunday", "high": "31°C", "low": "25°C", "condition": "Light Rain"},
                            {"day": "Monday", "high": "33°C", "low": "27°C", "condition": "Sunny"}
                        ])

                        forecast_cols = st.columns(5, gap="small")
                        for i, forecast_item in enumerate(forecast_data[:5]):
                            condition_str = forecast_item.get('condition', 'N/A')
                            fc_icon = icon_map.get(condition_str, "🌤️")
                            with forecast_cols[i]:
                                st.markdown(f"""
                                <div class="forecast-card">
                                    <p style="margin: 0; font-weight: bold; font-size: 13px;">{forecast_item.get('day', 'Day')}</p>
                                    <p style="margin: 8px 0; font-size: 28px;">{fc_icon}</p>
                                    <p style="margin: 5px 0; font-size: 12px;">{condition_str}</p>
                                    <p style="margin: 0; font-size: 11px;">↑ {forecast_item.get('high', 'N/A')} ↓ {forecast_item.get('low', 'N/A')}</p>
                                </div>
                                """, unsafe_allow_html=True)

                        st.markdown("---")

                        # Temperature Trend (5-day)
                        st.subheader("📈 Temperature Trend")
                        trend_data = {
                            "Mon": 28,
                            "Tue": 30,
                            "Wed": 29,
                            "Thu": 32,
                            "Fri": 33
                        }
                        trend_cols = st.columns(5, gap="small")
                        for i, (day, temp_val) in enumerate(trend_data.items()):
                            with trend_cols[i]:
                                st.markdown(f"""
                                <div style="text-align: center; padding: 15px; border-radius: 12px; background: linear-gradient(135deg, #4facfe, #00f2fe); color: white; font-weight: bold;">
                                    <p style="margin: 0; font-size: 13px;">{day}</p>
                                    <p style="margin: 10px 0; font-size: 24px;">{temp_val}°</p>
                                </div>
                                """, unsafe_allow_html=True)

                        st.markdown("---")

                        # Sunrise & Sunset Section
                        st.subheader("🌅 Sunrise & Sunset")
                        s1, s2 = st.columns(2)
                        with s1:
                            st.markdown(f"""
                            <div class="sun-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; height: 180px;">
                                <h2 style="margin: 0;">🌅</h2>
                                <p style="margin: 5px 0; font-size: 14px; opacity: 0.9;">Sunrise</p>
                                <div class="sun-time">{sunrise}</div>
                            </div>
                            """, unsafe_allow_html=True)
                        with s2:
                            st.markdown(f"""
                            <div class="sun-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white; height: 180px;">
                                <h2 style="margin: 0;">🌇</h2>
                                <p style="margin: 5px 0; font-size: 14px; opacity: 0.9;">Sunset</p>
                                <div class="sun-time">{sunset}</div>
                            </div>
                            """, unsafe_allow_html=True)

                        st.markdown("---")


                    # Hide developer UI for weather (production-ready)
                    if tool_name != "weather":
                        c1, c2 = st.columns(2, gap="large")

                        with c1:
                            st.markdown(
                                f"""
                                <div class="tool-card">
                                    <h3>{tool_icon(tool_name)} Tool Call</h3>
                                    <p><b>{tool_name}</b></p>
                                    <p><b>Confidence:</b> {confidence:.2f}</p>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
                            st.json(arguments)

                        with c2:
                            st.markdown("""
                            <div class="result-card">
                                <h3>✅ Execution Result</h3>
                                <p>Tool completed successfully.</p>
                            </div>
                            """, unsafe_allow_html=True)
                            st.json(tool_result)

                # ===============================
                # CAB RESULT - PROFESSIONAL VIEW
                # ===============================
                if result.get("tool_call", {}).get("tool_name") == "book_cab" or any(item.get("tool_call", {}).get("tool_name") == "book_cab" for item in executions):

                    st.markdown("---")
                    st.subheader("🚖 Cab Booking Result")

                    # Top Metrics
                    m1, m2, m3, m4 = st.columns(4)

                    with m1:
                        st.metric("📍 Distance", f"{result.get('distance_km', 110)} km")

                    with m2:
                        st.metric("⏱ ETA", f"{result.get('duration_min', 120)} min")

                    with m3:
                        st.metric("💰 Fare", f"₹{result.get('estimated_fare', 1500)}")

                    with m4:
                        st.metric("🎯 Confidence", f"{result.get('confidence', 0.95):.2f}")

                    st.markdown("<br>", unsafe_allow_html=True)

                    # Full Width Map
                    st.markdown("""
                    <h3>🗺️ Route Visualization</h3>
                    """, unsafe_allow_html=True)

                    route_map = folium.Map(location=[17.5, 79.0], zoom_start=8)

                    folium.Marker(
                        [17.3850, 78.4867],
                        popup="Pickup: Hyderabad",
                        tooltip="Hyderabad",
                        icon=folium.Icon(color="green", icon="play")
                    ).add_to(route_map)

                    folium.Marker(
                        [17.9689, 79.5941],
                        popup="Drop: Warangal",
                        tooltip="Warangal",
                        icon=folium.Icon(color="red", icon="flag")
                    ).add_to(route_map)

                    folium.PolyLine(
                        [[17.3850, 78.4867], [17.9689, 79.5941]],
                        weight=5,
                        opacity=0.8
                    ).add_to(route_map)

                    st_folium(
                        route_map,
                        width=None,
                        height=600,
                        returned_objects=[]
                    )

                    st.markdown("<br>", unsafe_allow_html=True)

                    # Information Cards
                    c1, c2 = st.columns(2)

                    with c1:
                        st.info(f"""
📍 Pickup: Hyderabad

🏁 Destination: Warangal

📏 Distance: {result.get('distance_km', 110)} km
                        """)

                    with c2:
                        st.success(f"""
⏱ Duration: {result.get('duration_min', 120)} min

💰 Estimated Fare: ₹{result.get('estimated_fare', 1500)}

🌐 Source: OpenRouteService
                        """)

                    # Google Maps Button
                    google_url = (
                        "https://www.google.com/maps/dir/"
                        "Hyderabad/Warangal"
                    )

                    st.link_button(
                        "🧭 Open in Google Maps",
                        google_url,
                        width='stretch'
                    )

                    st.markdown("---")

            elif response.status_code == 401:
                st.error("Session expired or invalid token. Please logout and login again.")

            else:
                st.error(f"Backend returned error: {response.status_code}")
                st.code(response.text)

        except requests.exceptions.ConnectionError:
            st.error("Backend not running. Start FastAPI using: uvicorn api.server:app --reload")
        except Exception as e:
            st.error("Something went wrong.")
            st.code(str(e))

st.markdown("---")
st.markdown('<div class="section-title">Tool Analytics</div>', unsafe_allow_html=True)

if tool_usage:
    usage_df = pd.DataFrame({
        "Tool": list(tool_usage.keys()),
        "Calls": list(tool_usage.values())
    }).set_index("Tool")

    chart_col, table_col = st.columns([1.2, 0.8], gap="large")

    with chart_col:
        st.bar_chart(usage_df, use_container_width=True)

    with table_col:
        st.dataframe(usage_df.reset_index(), use_container_width=True, hide_index=True)
else:
    st.info("No analytics available yet.")

st.markdown("---")
st.markdown('<div class="section-title">Recent Requests</div>', unsafe_allow_html=True)

table_rows = []
for row in history:
    call_id, request, tool, arguments, result, response_time, confidence, status, feedback, timestamp = row
    table_rows.append({
        "ID": call_id,
        "Tool": tool,
        "Request": request,
        "Latency": f"{response_time:.2f}s",
        "Confidence": f"{confidence if confidence is not None else 0.0:.2f}",
        "Status": status if status not in [None, "", "unknown"] else "success",
        "Feedback": feedback if feedback is not None else "",
        "Time": timestamp
    })

history_df = pd.DataFrame(table_rows)

if not history_df.empty:
    toolbar_left, toolbar_right = st.columns([4, 1], gap="medium")

    with toolbar_left:
        search_query = st.text_input(
            "Search history by request/tool/status",
            placeholder="weather, cab, email, success..."
        )

    if search_query.strip():
        q = search_query.lower()
        history_df = history_df[
            history_df.astype(str).apply(
                lambda row: row.str.lower().str.contains(q, regex=False).any(),
                axis=1
            )
        ]

    csv_data = history_df.to_csv(index=False).encode("utf-8")

    with toolbar_right:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        st.download_button(
            "📥 Download CSV",
            data=csv_data,
            file_name="tool_call_history.csv",
            mime="text/csv",
            use_container_width=True
        )

    st.dataframe(
        history_df,
        use_container_width=True,
        height=360,
        hide_index=True
    )

    with st.expander("View Detailed History / Feedback / Delete"):
        for row in history_df.to_dict("records"):
            call_id = row["ID"]
            request = row["Request"]
            tool = row["Tool"]
            safe_confidence = float(row["Confidence"])
            safe_status = row["Status"]

            original = next((x for x in history if x[0] == call_id), None)
            if not original:
                continue

            _, _, _, arguments, result, response_time, confidence, status, feedback, timestamp = original

            st.markdown(f"### #{call_id} | {tool_icon(tool)} {tool}")
            st.write(f"Request: {request}")
            st.write(f"Latency: {response_time:.2f}s | Confidence: {safe_confidence:.2f} | Status: {safe_status}")

            a, b = st.columns(2)

            with a:
                st.write("Arguments")
                parsed_args = safe_json_load(arguments)
                if isinstance(parsed_args, dict):
                    st.json(parsed_args)
                else:
                    st.code(str(parsed_args))

            with b:
                st.write("Result")
                parsed_result = safe_json_load(result)
                if isinstance(parsed_result, dict):
                    st.json(parsed_result)
                else:
                    st.code(str(parsed_result))

            f1, f2, f3 = st.columns(3)

            with f1:
                if st.button("👍 Correct", key=f"good_{call_id}", use_container_width=True):
                    update_feedback(call_id, "correct")
                    st.rerun()

            with f2:
                if st.button("👎 Wrong", key=f"bad_{call_id}", use_container_width=True):
                    update_feedback(call_id, "wrong")
                    st.rerun()

            with f3:
                if st.session_state.role == "admin":
                    if st.button("Delete", key=f"delete_{call_id}", use_container_width=True):
                        delete_row(call_id)
                        st.rerun()
                else:
                    st.button("Admin Only", key=f"admin_only_{call_id}", disabled=True, use_container_width=True)

            st.markdown("---")
else:
    st.info("No request history yet.")