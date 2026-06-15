import streamlit as st
import json
import os
from datetime import datetime

st.set_page_config(
    page_title="ClarityNet - AI Benefits Navigator",
    layout="wide",
    page_icon="🧭",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://claritynet.ai/help',
        'Report a bug': 'https://claritynet.ai/bugs',
    }
)

# ════════════════════════════════════════════════════════════════
# CUSTOM STYLING
# ════════════════════════════════════════════════════════════════

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=Bebas+Neue&display=swap');

:root {
    --primary: #1a3c5e;
    --primary-light: #2d5a8c;
    --success: #2f9e6e;
    --warning: #f4a460;
    --danger: #e74c3c;
    --bg: #f5f7fa;
    --card: #ffffff;
    --text: #1a1a1a;
    --text-light: #6c757d;
    --border: #e9ecef;
}

* {
    font-family: 'DM Sans', sans-serif !important;
    transition: all 0.3s ease;
}

.stApp {
    background: linear-gradient(135deg, var(--bg) 0%, #e9ecef 100%) !important;
}

/* Header */
.app-header {
    display: flex;
    align-items: center;
    gap: 20px;
    padding: 30px;
    background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%);
    border-radius: 20px;
    color: white;
    margin-bottom: 30px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.15);
}

.app-logo {
    font-size: 60px;
    animation: float 3s ease-in-out infinite;
}

@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-10px); }
}

.app-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 42px;
    letter-spacing: 2px;
    line-height: 1;
}

.app-subtitle {
    font-size: 14px;
    opacity: 0.9;
}

/* Stats */
.stats-container {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 16px;
    margin-bottom: 30px;
}

.stat-card {
    background: white;
    padding: 20px;
    border-radius: 12px;
    border-left: 4px solid var(--primary);
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

.stat-icon {
    font-size: 32px;
    margin-bottom: 8px;
}

.stat-value {
    font-size: 28px;
    font-weight: 700;
    color: var(--primary);
}

.stat-label {
    font-size: 12px;
    color: var(--text-light);
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* Feature Cards */
.feature-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 20px;
    margin: 20px 0;
}

.feature-card {
    background: white;
    padding: 24px;
    border-radius: 16px;
    border: 2px solid var(--border);
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    text-decoration: none;
    color: inherit;
    cursor: pointer;
    transition: all 0.3s ease;
}

.feature-card:hover {
    border-color: var(--primary);
    box-shadow: 0 8px 24px rgba(26, 60, 94, 0.15);
    transform: translateY(-4px);
}

.feature-card-icon {
    font-size: 48px;
    margin-bottom: 12px;
}

.feature-card-title {
    font-size: 18px;
    font-weight: 700;
    color: var(--primary);
    margin-bottom: 8px;
}

.feature-card-desc {
    font-size: 14px;
    color: var(--text-light);
    line-height: 1.5;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 12px 24px !important;
    font-weight: 600 !important;
    box-shadow: 0 4px 12px rgba(26, 60, 94, 0.2) !important;
    transition: all 0.3s ease !important;
    width: 100% !important;
}

.stButton > button:hover {
    box-shadow: 0 6px 16px rgba(26, 60, 94, 0.3) !important;
    transform: translateY(-2px) !important;
}

/* Sidebar */
.stSidebar {
    background: linear-gradient(180deg, white 0%, #f8f9fa 100%) !important;
}

[data-testid="stSidebarNav"] {
    padding: 20px 0 !important;
}

/* Responsive */
@media (max-width: 768px) {
    .app-header {
        flex-direction: column;
        text-align: center;
    }
    
    .app-logo {
        font-size: 48px;
    }
    
    .app-title {
        font-size: 28px;
    }
    
    .feature-grid {
        grid-template-columns: 1fr;
    }
}
</style>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
# SESSION STATE
# ════════════════════════════════════════════════════════════════

if "user_id" not in st.session_state:
    import uuid
    st.session_state.user_id = str(uuid.uuid4())[:8]

if "language" not in st.session_state:
    st.session_state.language = "en"

# ════════════════════════════════════════════════════════════════
# HEADER
# ════════════════════════════════════════════════════════════════

st.markdown("""
<div class="app-header">
    <div class="app-logo">🧭</div>
    <div>
        <div class="app-title">CLARITYNET</div>
        <div class="app-subtitle">AI-Powered Benefits Navigator | Get Support in Minutes</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
# STATS
# ════════════════════════════════════════════════════════════════

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-icon">✅</div>
        <div class="stat-value">15K+</div>
        <div class="stat-label">People Helped</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-icon">🎯</div>
        <div class="stat-value">$2.1B</div>
        <div class="stat-label">Benefits Found</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-icon">⏱️</div>
        <div class="stat-value">3 min</div>
        <div class="stat-label">Avg Assessment</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-icon">🌐</div>
        <div class="stat-value">5 Languages</div>
        <div class="stat-label">Supported</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ════════════════════════════════════════════════════════════════
# MAIN CONTENT
# ════════════════════════════════════════════════════════════════

st.markdown("## 🚀 Choose Your Journey")

st.markdown("""
<div class="feature-grid">
    <div class="feature-card">
        <div class="feature-card-icon">💬</div>
        <div class="feature-card-title">Chat with AI</div>
        <div class="feature-card-desc">Talk naturally about your situation. Get instant eligibility insights.</div>
    </div>
    
    <div class="feature-card">
        <div class="feature-card-icon">📊</div>
        <div class="feature-card-title">Eligibility Dashboard</div>
        <div class="feature-card-desc">See visual breakdown of all programs you may qualify for.</div>
    </div>
    
    <div class="feature-card">
        <div class="feature-card-icon">📄</div>
        <div class="feature-card-title">Document Manager</div>
        <div class="feature-card-desc">Upload documents and get AI guidance on what's needed.</div>
    </div>
    
    <div class="feature-card">
        <div class="feature-card-icon">📅</div>
        <div class="feature-card-title">Book Appointment</div>
        <div class="feature-card-desc">Schedule with agencies directly. Get reminders & confirmations.</div>
    </div>
    
    <div class="feature-card">
        <div class="feature-card-icon">📈</div>
        <div class="feature-card-title">Track Application</div>
        <div class="feature-card-desc">Monitor your applications in real-time from start to approval.</div>
    </div>
    
    <div class="feature-card">
        <div class="feature-card-icon">👤</div>
        <div class="feature-card-title">My Profile</div>
        <div class="feature-card-desc">View your info, history, and personalized recommendations.</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ════════════════════════════════════════════════════════════════
# QUICK ACCESS BUTTONS
# ════════════════════════════════════════════════════════════════

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("💬 Start Chat", use_container_width=True, key="btn_chat"):
        st.switch_page("pages/01_💬_chat.py")

with col2:
    if st.button("📊 View Dashboard", use_container_width=True, key="btn_dashboard"):
        st.switch_page("pages/02_📊_dashboard.py")

with col3:
    if st.button("📄 Documents", use_container_width=True, key="btn_docs"):
        st.switch_page("pages/03_📄_documents.py")

st.markdown("---")

# ════════════════════════════════════════════════════════════════
# INFO SECTION
# ════════════════════════════════════════════════════════════════

with st.container():
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### 🌟 Why ClarityNet?
        
        - **AI-Powered**: Smart eligibility matching
        - **Fast**: Get results in minutes
        - **Comprehensive**: SNAP, Medicaid, LIHEAP + more
        - **Secure**: Your data is protected
        - **Free**: No hidden fees
        - **Multi-Language**: Spanish, Vietnamese, Chinese, Arabic
        
        ### 📞 Need Help?
        - Call: 1-800-XXX-XXXX
        - Email: support@claritynet.ai
        - Chat: Available 24/7
        """)
    
    with col2:
        st.markdown("""
        ### 📊 Recent Stats
        
        **This Month:**
        - 1,245 applications started
        - $45.2M in benefits found
        - 94% satisfaction rate
        
        **Success Stories:**
        - Family of 4 got $8,400/year
        - Senior got free healthcare
        - Single parent saved $200/month
        """)

st.markdown("---")

# ════════════════════════════════════════════════════════════════
# LANGUAGE SELECTOR (SIDEBAR)
# ════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("### ⚙️ Settings")
    
    language = st.selectbox(
        "Language / Idioma / Ngôn ngữ",
        ["English", "Español", "Tiếng Việt", "中文", "العربية"],
        index=0,
        key="lang_select"
    )
    
    lang_map = {
        "English": "en",
        "Español": "es",
        "Tiếng Việt": "vi",
        "中文": "zh",
        "العربية": "ar"
    }
    
    st.session_state.language = lang_map[language]
    
    st.markdown("---")
    st.markdown("""
    ### ℹ️ About
    
    **ClarityNet** is an AI-powered benefits navigator designed to help people discover and access public support programs.
    
    - Made with ❤️ for communities
    - Powered by OpenAI
    - Built on Streamlit
    
    **Disclaimer:** This is not an official government service. Always verify with official agencies.
    """)