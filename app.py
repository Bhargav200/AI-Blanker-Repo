import streamlit as st
import requests
import os
import time
import pandas as pd
import json

BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="AI PII Redactor", layout="wide")

st.title("🧩 AI PII Redactor for Public Datasets")
st.markdown("Safely sanitize your datasets for AI/LLM training.")

# Sidebar for navigation
menu = ["Home", "New Redaction Job", "Job History", "Compliance Summary", "Evaluation Report", "API Access"]
choice = st.sidebar.selectbox("Navigation", menu)

if choice == "Home":
    st.subheader("Welcome to the AI PII Redactor")
    st.write("This tool helps you detect and redact Personally Identifiable Information (PII) from various file formats.")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.info("📂 **Multi-Format**\nTXT, CSV, JSON, PDF, DOCX, Images")
    with col2:
        st.info("🔍 **Hybrid Detection**\nRegex + NLP Transformer")
    with col3:
        st.info("🛡️ **Redaction Modes**\nMask, Label, Pseudonym, Synthetic")
    with col4:
        st.info("📊 **Compliance**\nGDPR, HIPAA, DPDP Ready")

elif choice == "New Redaction Job":
    st.subheader("🚀 Create New Redaction Job")
    
    with st.form("redaction_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 1. Upload Files")
            uploaded_files = st.file_uploader("Choose files", accept_multiple_files=True)
            
            st.markdown("### 2. Detection Settings")
            confidence_threshold = st.slider("Confidence Threshold", 0.0, 1.0, 0.5)
            pii_categories = st.multiselect(
                "PII Categories",
                ["EMAIL", "PHONE", "SSN", "CREDIT_CARD", "PERSON", "ORGANIZATION", "LOCATION", "DATE", "IP_ADDRESS", "BANK_ACCOUNT", "PASSPORT", "DRIVER_LICENSE"],
                default=["EMAIL", "PHONE", "PERSON", "SSN"]
            )
            
        with col2:
            st.markdown("### 3. Redaction Settings")
            redaction_mode = st.radio("Redaction Mode", ["Mask", "Label", "Pseudonym", "Synthetic"])
            compliance_profile = st.selectbox("Compliance Profile", ["Default", "GDPR", "HIPAA", "DPDP"])
            language_hint = st.selectbox("Language Hint", ["English", "Hindi Assist", "Telugu Assist"])
            
        submitted = st.form_submit_button("Start Redaction Job")
        
        if submitted:
            if not uploaded_files:
                st.error("Please upload at least one file.")
            else:
                # Prepare data for API
                files_payload = [("files", (f.name, f.getvalue(), f.type)) for f in uploaded_files]
                config = {
                    "redaction_mode": redaction_mode,
                    "confidence_threshold": confidence_threshold,
                    "compliance_profile": compliance_profile,
                    "language_hint": language_hint,
                    "pii_categories": pii_categories
                }
                
                with st.spinner("Uploading and starting job..."):
                    try:
                        # We need to send config as part of the multipart/form-data or separately
                        # FastAPI expects config as a JSON object in the form.
                        # For simplicity, we'll send files and config in the same request.
                        # Note: Sending complex JSON in multipart can be tricky with some libraries.
                        # We'll use a trick or adjust the backend if needed.
                        
                        # Simplified for MVP: Send config as separate form fields
                        data = {
                            "redaction_mode": redaction_mode,
                            "confidence_threshold": str(confidence_threshold),
                            "compliance_profile": compliance_profile,
                            "language_hint": language_hint,
                            "pii_categories": json.dumps(pii_categories)
                        }
                        
                        response = requests.post(f"{BASE_URL}/jobs/create", files=files_payload, data=data)
                        
                        if response.status_code == 200:
                            job_data = response.json()
                            st.success(f"Job started! ID: {job_data['job_id']}")
                            st.session_state.current_job_id = job_data['job_id']
                            st.info("Check 'Job History' or wait for results below.")
                        else:
                            st.error(f"Error starting job: {response.text}")
                    except Exception as e:
                        st.error(f"Connection error: {str(e)}")

elif choice == "Job History":
    st.subheader("📜 Redaction Job History")
    if st.button("🔄 Refresh Status"):
        st.rerun()
    
    # This would normally fetch from the DB
    # For now, let's assume we can fetch all jobs
    try:
        # We need an endpoint for this
        # response = requests.get(f"{BASE_URL}/jobs")
        # For now, let's just show a placeholder or the current job if it exists
        if 'current_job_id' in st.session_state:
            job_id = st.session_state.current_job_id
            response = requests.get(f"{BASE_URL}/jobs/{job_id}")
            if response.status_code == 200:
                job = response.json()
                st.markdown(f"### Job: {job['job_uuid']}")
                st.write(f"Status: **{job['status']}**")
                st.progress(job['processed_files'] / job['total_files'] if job['total_files'] > 0 else 0)
                
                st.write(f"Entities Detected: {job['total_entities_detected']}")
                
                if job['files']:
                    st.markdown("#### Files")
                    for f in job['files']:
                        with st.expander(f"📄 {f['filename']} (Risk: {f['risk_level']})"):
                            col1, col2 = st.columns(2)
                            
                            # Fetch file details for comparison
                            file_details_res = requests.get(f"{BASE_URL}/files/{f['id']}")
                            if file_details_res.status_code == 200:
                                file_details = file_details_res.json()
                                
                                with col1:
                                    st.markdown("**Before (Original)**")
                                    try:
                                        # Fetch original visual image as bytes
                                        img_res = requests.get(f"{BASE_URL}/files/{f['id']}/visual-original")
                                        if img_res.status_code == 200 and len(img_res.content) > 0:
                                            st.image(img_res.content, use_container_width=True)
                                            st.success(f"Loaded original ({len(img_res.content)} bytes)")
                                        else:
                                            # Fallback to text area if visual-original is not available or not an image
                                            st.text_area("Original", file_details.get('raw_content', ''), height=300, key=f"raw_{f['id']}")
                                    except Exception as e:
                                        st.text_area("Original", file_details.get('raw_content', ''), height=300, key=f"raw_{f['id']}")
                                    
                                with col2:
                                    st.markdown("**After (Redacted Result)**")
                                    try:
                                        # Fetch visual redacted image as bytes
                                        visual_res = requests.get(f"{BASE_URL}/files/{f['id']}/visual")
                                        if visual_res.status_code == 200 and len(visual_res.content) > 0:
                                            st.image(visual_res.content, use_container_width=True)
                                            st.success(f"Loaded visual ({len(visual_res.content)} bytes)")
                                        else:
                                            st.error(f"Failed to load redacted image (Status: {visual_res.status_code}, Size: {len(visual_res.content) if visual_res else 'N/A'})")
                                    except Exception as e:
                                        st.error(f"Error loading redacted: {str(e)}")
                                
                                st.markdown("#### Detected Entities")
                                if file_details.get('entities'):
                                    ent_df = pd.DataFrame(file_details['entities'])
                                    st.dataframe(ent_df[['text', 'type', 'confidence', 'risk_level']])
                                else:
                                    st.write("No entities detected.")
                            else:
                                st.error("Could not fetch file details.")
            else:
                st.write("No jobs found.")
        else:
            st.write("No active jobs. Start a new one!")
    except Exception as e:
        st.error(f"Error fetching job history: {str(e)}")

elif choice == "Compliance Summary":
    st.subheader("🛡️ Compliance Summary")
    if 'current_job_id' in st.session_state:
        job_id = st.session_state.current_job_id
        try:
            response = requests.get(f"{BASE_URL}/jobs/{job_id}/compliance")
            if response.status_code == 200:
                summary = response.json()
                st.markdown(f"### Profile: {summary['name']}")
                st.write(summary['description'])
                
                st.markdown("#### Alignment Mapping")
                df = pd.DataFrame(summary['mappings'])
                st.table(df)
            else:
                st.warning("Could not fetch compliance summary for the current job.")
        except Exception as e:
            st.error(f"Error: {str(e)}")
    else:
        st.info("Run a redaction job first to see the compliance mapping.")

elif choice == "Evaluation Report":
    st.subheader("📊 Redaction Accuracy Report")
    try:
        response = requests.get(f"{BASE_URL}/evaluation/metrics")
        if response.status_code == 200:
            metrics = response.json()
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Precision", f"{metrics['precision']*100:.1f}%")
            col2.metric("Recall", f"{metrics['recall']*100:.1f}%")
            col3.metric("F1 Score", f"{metrics['f1_score']*100:.1f}%")
            
            st.markdown("#### Confusion Matrix (Entity Level)")
            cm_data = []
            for entity, counts in metrics['confusion_matrix'].items():
                cm_data.append({"Entity": entity, **counts})
            st.table(pd.DataFrame(cm_data))
        else:
            st.error("Error fetching evaluation metrics.")
    except Exception as e:
        st.error(f"Error: {str(e)}")

elif choice == "API Access":
    st.subheader("🔗 API Documentation")
    st.code("""
POST /jobs/create
Content-Type: multipart/form-data

files: [binary]
redaction_mode: "Mask"
confidence_threshold: 0.5
compliance_profile: "GDPR"
pii_categories: ["EMAIL", "PHONE"]
    """, language="bash")
    
    st.code("""
GET /jobs/{job_id}
Response:
{
  "job_id": 1,
  "status": "Completed",
  "total_entities_detected": 42,
  ...
}
    """, language="json")

st.sidebar.markdown("---")
st.sidebar.info(f"Version: 1.0.0-MVP")
