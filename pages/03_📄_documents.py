import streamlit as st
import os
from datetime import datetime
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.document_processor import validate_document, extract_text_from_image
from utils.database import save_document, get_documents

st.set_page_config(
    page_title="ClarityNet - Documents",
    layout="wide",
    page_icon="📄"
)

st.markdown("""
<style>
.doc-card {
    background: white;
    padding: 16px;
    border-radius: 12px;
    border: 2px solid #e9ecef;
    margin: 8px 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.doc-status-ready {
    color: #2f9e6e;
    font-weight: 700;
}

.doc-status-missing {
    color: #e74c3c;
    font-weight: 700;
}

.upload-area {
    border: 2px dashed #1a3c5e;
    border-radius: 12px;
    padding: 40px;
    text-align: center;
    background: #f0f4f8;
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
    st.markdown("##### 📄 Document Manager")

with col3:
    if st.button("📊 Dashboard", use_container_width=True):
        st.switch_page("pages/02_📊_dashboard.py")

st.markdown("---")

# ════════════════════════════════════════════════════════════════
# REQUIRED DOCUMENTS
# ════════════════════════════════════════════════════════════════

st.markdown("## 📋 Required Documents Checklist")

documents_needed = [
    {
        "id": "id",
        "name": "Photo ID",
        "description": "Driver's license, passport, or state ID",
        "status": "ready",
        "uploaded": "ID_scan.pdf"
    },
    {
        "id": "income",
        "name": "Proof of Income",
        "description": "Last 2 pay stubs or tax return",
        "status": "missing",
        "uploaded": None
    },
    {
        "id": "address",
        "name": "Address Proof",
        "description": "Utility bill or lease agreement",
        "status": "ready",
        "uploaded": "utility_bill.pdf"
    },
    {
        "id": "residence",
        "name": "Proof of Residency",
        "description": "Any official document with your address",
        "status": "missing",
        "uploaded": None
    },
]

progress = sum(1 for d in documents_needed if d["status"] == "ready") / len(documents_needed) * 100

st.markdown(f"""
<div style="background: #f0f4f8; padding: 16px; border-radius: 12px; margin-bottom: 20px;">
    <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
        <b>Progress</b>
        <b>{int(progress)}%</b>
    </div>
    <div style="background: white; border-radius: 8px; overflow: hidden; height: 24px;">
        <div style="background: linear-gradient(90deg, #1a3c5e 0%, #2d5a8c 100%); width: {progress}%; height: 100%; transition: width 0.3s;"></div>
    </div>
</div>
""", unsafe_allow_html=True)

for doc in documents_needed:
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col1:
        status_text = "✅ Ready" if doc["status"] == "ready" else "❌ Missing"
        status_class = "doc-status-ready" if doc["status"] == "ready" else "doc-status-missing"
        uploaded_text = f" ({doc['uploaded']})" if doc["uploaded"] else ""
        
        st.markdown(f"""
        <div class="doc-card">
            <div>
                <b>{doc['name']}</b>
                <div style="font-size: 12px; color: #6c757d;">{doc['description']}</div>
                <div class="{status_class}" style="font-size: 12px; margin-top: 4px;">{status_text}{uploaded_text}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# ════════════════════════════════════════════════════════════════
# UPLOAD SECTION
# ════════════════════════════════════════════════════════════════

st.markdown("## 📤 Upload Documents")

st.markdown("""
<div class="upload-area">
    <div style="font-size: 48px; margin-bottom: 12px;">📁</div>
    <b>Drag and drop files here or click to upload</b>
    <div style="font-size: 12px; color: #6c757d; margin-top: 8px;">
        Supported: PDF, JPG, PNG, DOC (Max 10MB each)
    </div>
</div>
""", unsafe_allow_html=True)

uploaded_files = st.file_uploader(
    "Upload documents",
    type=["pdf", "jpg", "png", "doc", "docx"],
    accept_multiple_files=True,
    label_visibility="collapsed"
)

if uploaded_files:
    st.markdown("### 📋 Uploaded Files")
    
    for file in uploaded_files:
        # Validate
        is_valid, msg = validate_document(file)
        
        if is_valid:
            st.success(f"✅ {file.name}")
            
            # Extract text if image
            if file.type.startswith("image/"):
                extracted_text = extract_text_from_image(file)
                with st.expander("📄 Extracted Information"):
                    st.text(extracted_text)
            
            # Save
            save_document(st.session_state.user_id, file)
        else:
            st.error(f"❌ {file.name}: {msg}")

st.markdown("---")

# ════════════════════════════════════════════════════════════════
# TEMPLATES
# ════════════════════════════════════════════════════════════════

st.markdown("## 📝 Document Templates")

with st.expander("📄 Proof of Income Letter Template"):
    st.markdown("""
    ```
    [Your Name]
    [Your Address]
    [Date]
    
    To Whom It May Concern,
    
    This letter certifies that [Your Name] has been employed at [Company]
    as a [Job Title] since [Date].
    
    Current Monthly Income: $[Amount]
    
    Sincerely,
    
    [Employer Name]
    [Company]
    ```
    
    [Download Template](# )
    """)

with st.expander("🏠 Proof of Residency Letter Template"):
    st.markdown("""
    ```
    [Your Name]
    [Address]
    [Date]
    
    To the Appropriate Agency,
    
    I hereby certify that [Your Name] resides at [Your Address]
    as of [Date].
    
    [Landlord/Owner Name]
    [Contact Information]
    ```
    
    [Download Template](# )
    """)