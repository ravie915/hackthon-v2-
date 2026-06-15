import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.database import load_user_profile
from utils.visualizations import create_eligibility_gauge, create_timeline, create_heatmap

st.set_page_config(
    page_title="ClarityNet - Dashboard",
    layout="wide",
    page_icon="📊"
)

st.markdown("""
<style>
.dashboard-card {
    background: white;
    padding: 24px;
    border-radius: 16px;
    border: 2px solid #e9ecef;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}

.kpi {
    text-align: center;
    padding: 20px;
    background: linear-gradient(135deg, #1a3c5e 0%, #2d5a8c 100%);
    color: white;
    border-radius: 12px;
    margin: 8px;
}

.kpi-value {
    font-size: 36px;
    font-weight: 700;
    margin: 8px 0;
}

.kpi-label {
    font-size: 12px;
    opacity: 0.9;
}
</style>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
# HEADER
# ════════════════════════════════════════════════════════════════

col1, col2, col3 = st.columns([1, 3, 1])

with col1:
    st.markdown("### 🧭 ClarityNet")

with col2:
    st.markdown("##### 📊 Eligibility Dashboard")

with col3:
    if st.button("💬 Chat", use_container_width=True):
        st.switch_page("pages/01_💬_chat.py")

st.markdown("---")

# ════════════════════════════════════════════════════════════════
# KPIs
# ════════════════════════════════════════════════════════════════

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="kpi">
        <div class="kpi-value">85%</div>
        <div class="kpi-label">Overall Match</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="kpi">
        <div class="kpi-value">3/3</div>
        <div class="kpi-label">Programs Eligible</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="kpi">
        <div class="kpi-value">$12.5K</div>
        <div class="kpi-label">Annual Benefits</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="kpi">
        <div class="kpi-value">🟢</div>
        <div class="kpi-label">Ready to Apply</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ════════════════════════════════════════════════════════════════
# PROGRAM ELIGIBILITY
# ════════════════════════════════════════════════════════════════

st.markdown("## 📋 Program Eligibility Breakdown")

# Sample data - replace with actual data
programs = [
    {"name": "SNAP", "match": 95, "status": "Likely Match", "color": "green"},
    {"name": "Medicaid", "match": 88, "status": "Likely Match", "color": "green"},
    {"name": "LIHEAP", "match": 65, "status": "Possible Match", "color": "orange"},
]

col1, col2, col3 = st.columns(3)

for idx, program in enumerate(programs):
    with [col1, col2, col3][idx]:
        st.markdown(f"""
        <div class="dashboard-card">
            <h3>{program['name']}</h3>
            <div style="background: #f0f4f8; border-radius: 8px; overflow: hidden; height: 30px; margin: 16px 0;">
                <div style="background: {'#2f9e6e' if program['color'] == 'green' else '#f4a460'}; width: {program['match']}%; height: 100%; display: flex; align-items: center; justify-content: center; color: white; font-weight: 700; font-size: 12px;">
                    {program['match']}%
                </div>
            </div>
            <p style="text-align: center; color: #6c757d; margin: 0;">
                <b style="color: {'#2f9e6e' if program['color'] == 'green' else '#f4a460'}">{program['status']}</b>
            </p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# ════════════════════════════════════════════════════════════════
# CHARTS
# ════════════════════════════════════════════════════════════════

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 💰 Income vs Poverty Line")
    
    # Sample chart
    fig = go.Figure(data=[
        go.Bar(x=['Your Income', 'Program Limit'], y=[2000, 1845], 
               marker_color=['#2f9e6e', '#dee2e6'])
    ])
    fig.update_layout(
        height=300,
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=False,
        hovermode='x unified'
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("### 📅 Application Timeline")
    
    # Sample timeline
    timeline_data = {
        "Stage": ["Submit", "Review", "Decision", "Receive"],
        "Days": [0, 7, 14, 21]
    }
    
    fig = go.Figure(data=[
        go.Scatter(x=timeline_data["Days"], y=timeline_data["Stage"],
                  mode='markers+lines',
                  marker=dict(size=12, color='#1a3c5e'))
    ])
    fig.update_layout(
        height=300,
        margin=dict(l=0, r=0, t=0, b=0),
        hovermode='closest',
        yaxis_title="",
        xaxis_title="Days"
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ════════════════════════════════════════════════════════════════
# NEXT STEPS
# ════════════════════════════════════════════════════════════════

st.markdown("## ✅ Your Next Steps")

steps = [
    ("📄", "Upload Required Documents", "Proof of income, ID, address"),
    ("📞", "Call to Confirm Eligibility", "1-800-252-8263"),
    ("📝", "Complete Application", "Online or in-person"),
    ("✅", "Review & Submit", "Submit application by Dec 15"),
]

for icon, title, desc in steps:
    col1, col2 = st.columns([0.5, 9.5]
    
    with col1:
        st.markdown(f"<h3 style='margin: 0; color: #1a3c5e;'>{icon}</h3>", unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"**{title}**  \n{desc}")

st.markdown("---")

# ════════════════════════════════════════════════════════════════
# ACTIONS
# ════════════════════════════════════════════════════════════════

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📄 Upload Documents", use_container_width=True):
        st.switch_page("pages/03_📄_documents.py")

with col2:
    if st.button("📅 Schedule Appointment", use_container_width=True):
        st.switch_page("pages/04_📅_appointments.py")

with col3:
    if st.button("📈 Track Application", use_container_width=True):
        st.switch_page("pages/05_📈_tracker.py")