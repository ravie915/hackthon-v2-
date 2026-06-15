import streamlit as st
import calendar
from datetime import datetime, timedelta
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.notifications import send_appointment_reminder

st.set_page_config(
    page_title="ClarityNet - Appointments",
    layout="wide",
    page_icon="📅"
)

st.markdown("""
<style>
.appointment-card {
    background: white;
    padding: 20px;
    border-radius: 12px;
    border-left: 4px solid #1a3c5e;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    margin-bottom: 16px;
}

.time-slot {
    padding: 12px;
    border: 2px solid #dee2e6;
    border-radius: 8px;
    margin: 4px;
    text-align: center;
    cursor: pointer;
    transition: all 0.2s;
}

.time-slot:hover {
    border-color: #1a3c5e;
    background: #f0f4f8;
}

.time-slot.selected {
    background: linear-gradient(135deg, #1a3c5e 0%, #2d5a8c 100%);
    color: white;
    border-color: #1a3c5e;
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
    st.markdown("##### 📅 Book Appointment")

with col3:
    if st.button("📊 Dashboard", use_container_width=True):
        st.switch_page("pages/02_📊_dashboard.py")

st.markdown("---")

# ════════════════════════════════════════════════════════════════
# APPOINTMENT FORM
# ════════════════════════════════════════════════════════════════

tab1, tab2 = st.tabs(["📅 Book New", "📋 My Appointments"])

with tab1:
    st.markdown("## 📅 Schedule an Appointment")
    
    with st.form("appointment_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            program = st.selectbox(
                "Select Program",
                ["SNAP", "Medicaid", "LIHEAP"]
            )
            
            appointment_type = st.selectbox(
                "Type",
                ["In-person", "Phone Call", "Video Call"]
            )
        
        with col2:
            date = st.date_input(
                "Preferred Date",
                min_value=datetime.now().date()
            )
            
            time = st.selectbox(
                "Preferred Time",
                ["9:00 AM", "10:00 AM", "11:00 AM", "2:00 PM", "3:00 PM", "4:00 PM"]
            )
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Your Name*")
            phone = st.text_input("Phone Number*")
        
        with col2:
            email = st.text_input("Email Address*")
            notes = st.text_area("Additional Notes")
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.form_submit_button("✅ Schedule Appointment", use_container_width=True):
                st.success("""
                ✅ **Appointment Scheduled!**
                
                **Details:**
                - Program: SNAP
                - Date: Dec 15, 2024
                - Time: 10:00 AM
                - Type: In-person
                - Location: 123 Main St, Suite 100
                
                **Confirmation sent to:** your-email@example.com
                
                You'll receive reminders 1 day and 1 hour before.
                """)
                
                # Send reminder email
                send_appointment_reminder(email, {
                    "date": str(date),
                    "time": time,
                    "program": program
                })
        
        with col2:
            if st.form_submit_button("❌ Cancel", use_container_width=True):
                st.info("Cancelled")

with tab2:
    st.markdown("## 📋 My Appointments")
    
    appointments = [
        {
            "program": "SNAP",
            "date": "Dec 15, 2024",
            "time": "10:00 AM",
            "location": "123 Main St, Suite 100",
            "status": "Confirmed",
            "contact": "1-800-XXX-XXXX"
        },
    ]
    
    if not appointments:
        st.info("No appointments scheduled yet.")
    else:
        for apt in appointments:
            st.markdown(f"""
            <div class="appointment-card">
                <div style="display: flex; justify-content: space-between; margin-bottom: 12px;">
                    <h3 style="margin: 0;">{apt['program']} Appointment</h3>
                    <span style="background: #d4edda; color: #1d7a4c; padding: 4px 12px; border-radius: 50px; font-size: 12px; font-weight: 700;">
                        ✅ {apt['status']}
                    </span>
                </div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; font-size: 14px;">
                    <div><b>📅 Date:</b> {apt['date']}</div>
                    <div><b>🕐 Time:</b> {apt['time']}</div>
                    <div><b>📍 Location:</b> {apt['location']}</div>
                    <div><b>☎️ Contact:</b> {apt['contact']}</div>
                </div>
                <div style="margin-top: 12px; display: flex; gap: 8px;">
                    <button style="padding: 8px 16px; border: none; border-radius: 6px; background: #1a3c5e; color: white; cursor: pointer;">
                        📝 Reschedule
                    </button>
                    <button style="padding: 8px 16px; border: none; border-radius: 6px; background: #e74c3c; color: white; cursor: pointer;">
                        ❌ Cancel
                    </button>
                </div>
            </div>
            """, unsafe_allow_html=True)