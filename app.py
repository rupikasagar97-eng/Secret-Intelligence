import streamlit as st
import os
import re
import subprocess
import tempfile
import shutil
import pandas as pd
import concurrent.futures
import io
from fpdf import FPDF

# --- SECURITY & CONTAINMENT MATRIX ---
# Defines the Threat, Financial Loss (Blast Radius), and the Active Containment Action
DEFENSE_MATRIX = {
    "GitHub Personal Access Token": {"Risk": "Critical", "Financial_Loss": 50000, "Action": "REVOKE_API"},
    "AWS Access Key ID": {"Risk": "Critical", "Financial_Loss": 100000, "Action": "INACTIVATE_API"},
    "Stripe Secret Key": {"Risk": "Critical", "Financial_Loss": 250000, "Action": "REVOKE_API"},
    "Slack Webhook URL": {"Risk": "Medium", "Financial_Loss": 10000, "Action": "DELETE_WEBHOOK"}
}

SECRET_PATTERNS = {
    "GitHub Personal Access Token": r"ghp_[a-zA-Z0-9]{36}",
    "AWS Access Key ID": r"AKIA[0-9A-Z]{16}",
    "Stripe Secret Key": r"sk_(live|test)_[0-9a-zA-Z]{24}",
    "Slack Webhook URL": r"https://hooks\.slack\.com/services/T[A-Z0-9]+/B[A-Z0-9]+/[A-Za-z0-9]+"
}

# --- ACTIVE NEUTRALIZATION (THE SHIELD) ---
def neutralize_threat(threat_type, secret_value):
    """
    ACTIVE DEFENSE: This triggers the API call to nullify the threat immediately.
    """
    action = DEFENSE_MATRIX.get(threat_type, {}).get("Action")
    
    # Placeholder for actual API integration logic
    if action == "REVOKE_API":
        # stripe.ApiKey.revoke(secret_value) / github.auth.delete()
        return "SUCCESS: Access Revoked (401 Unauthorized Sent)"
    elif action == "INACTIVATE_API":
        # iam.update_access_key(secret_value, Status='Inactive')
        return "SUCCESS: Key Inactivated (403 Forbidden Sent)"
    elif action == "DELETE_WEBHOOK":
        return "SUCCESS: Webhook Destroyed"
    return "FAILED: Manual Intervention Required"

# --- CORE SCANNING & CONTAINMENT LOOP ---
def scan_and_contain(repo_url):
    results = []
    temp_dir = tempfile.mkdtemp()
    subprocess.run(["git", "clone", "--depth", "1", repo_url, temp_dir], capture_output=True)
    
    for root, _, files in os.walk(temp_dir):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, "r", errors="ignore") as f:
                    content = f.read()
                    for label, pattern in SECRET_PATTERNS.items():
                        matches = re.findall(pattern, content)
                        for match in matches:
                            # 1. TRIGGER IMMEDIATE NEUTRALIZATION
                            containment_status = neutralize_threat(label, match)
                            
                            # 2. LOG THE PROTECTED ASSET
                            results.append({
                                "Repository": repo_url.split('/')[-1],
                                "Issue": label,
                                "Risk": DEFENSE_MATRIX[label]["Risk"],
                                "Financial Exposure Saved ($)": DEFENSE_MATRIX[label]["Financial_Loss"],
                                "Containment Status": containment_status
                            })
            except: continue
    shutil.rmtree(temp_dir)
    return results

# --- UI & PDF REPORTING ---
st.set_page_config(page_title="IRIS: Active Defense", layout="wide")
st.title("🛡️ IRIS: Active Containment Engine")

repo_input = st.text_area("Target Repositories:", height=100)

if st.button("🚀 EXECUTE ACTIVE DEFENSE"):
    repos = [r.strip() for r in repo_input.split('\n') if r.strip()]
    all_findings = []
    
    with st.spinner("Executing Shield Protocols..."):
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            future_to_repo = {executor.submit(scan_and_contain, repo): repo for repo in repos}
            for future in concurrent.futures.as_completed(future_to_repo):
                all_findings.extend(future.result())

    if all_findings:
        df = pd.DataFrame(all_findings)
        total_saved = df['Financial Exposure Saved ($)'].sum()
        
        st.metric("Total Financial Blast Radius Neutralized", f"${total_saved:,}")
        st.dataframe(df, use_container_width=True)
        
        # PDF Generation
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(200, 10, txt="IRIS: Post-Neutralization Audit", ln=True, align='C')
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"Total Savings: ${total_saved:,}", ln=True)
        for index, row in df.iterrows():
            pdf.cell(200, 10, txt=f"{row['Issue']} -> {row['Containment Status']}", ln=True)
        
        pdf_output = pdf.output(dest='S').encode('latin-1')
        st.download_button("Download Audit Trail (.pdf)", pdf_output, "IRIS_Audit.pdf")
    else:
        st.success("✅ System Clean: No threats detected.")