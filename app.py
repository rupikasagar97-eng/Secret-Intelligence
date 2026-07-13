import streamlit as st
import os
import re
import subprocess
import tempfile
import shutil
import pandas as pd
import io
import concurrent.futures

# --- HOLLISTIC RISK & REMEDIATION CONFIG ---
RISK_MATRIX = {
    "GitHub Personal Access Token": {"Risk": "Critical", "Potential_Loss": 50000, "Remediation": "Revoke & Rotate"},
    "AWS Access Key ID": {"Risk": "Critical", "Potential_Loss": 100000, "Remediation": "Revoke & Rotate"},
    "Exposed Password/Secret": {"Risk": "High", "Potential_Loss": 25000, "Remediation": "Update & Secrets Manager"},
    "Slack Webhook URL": {"Risk": "Medium", "Potential_Loss": 10000, "Remediation": "Delete & Reissue"}
}

SECRET_PATTERNS = {
    "GitHub Personal Access Token": r"ghp_[a-zA-Z0-9]{36}",
    "AWS Access Key ID": r"AKIA[0-9A-Z]{16}",
    "Exposed Password/Secret": r"(?i)(password|secret|api_key|passwd)\s*=\s*['\"]([^'\"]+)['\"]",
    "Slack Webhook URL": r"https://hooks\.slack\.com/services/T[A-Z0-9]+/B[A-Z0-9]+/[A-Za-z0-9]+"
}

def scan_single_repo(repo_url):
    """Function to process one repository entirely."""
    results = []
    temp_dir = tempfile.mkdtemp()
    
    # Clone logic
    subprocess.run(["git", "clone", "--depth", "1", repo_url, temp_dir], capture_output=True)
    
    for root, _, files in os.walk(temp_dir):
        if '.git' in root: continue
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, "r", errors="ignore") as f:
                    content = f.read()
                    for label, pattern in SECRET_PATTERNS.items():
                        if re.search(pattern, content):
                            metadata = RISK_MATRIX.get(label, {"Risk": "High", "Potential_Loss": 0, "Remediation": "Review"})
                            results.append({
                                "Repository": repo_url.split('/')[-1],
                                "File": file, 
                                "Issue": label,
                                "Risk Level": metadata['Risk'],
                                "Potential Loss ($)": metadata['Potential_Loss'],
                                "Execution Matrix (Status)": "Open / Needs Review",
                                "Remediation Plan": metadata['Remediation']
                            })
            except: continue
    shutil.rmtree(temp_dir)
    return results

# --- UI LAYER ---
st.set_page_config(page_title="IRIS: Holistic Engine", layout="wide")
st.title("🛡️ IRIS: Holistic Execution & Risk Matrix")

repo_input = st.text_area("Target Repositories (One URL per line):", height=150)

if st.button("🚀 Run Parallel Holistic Analysis"):
    repos = [r.strip() for r in repo_input.split('\n') if r.strip()]
    all_violations = []

    with st.spinner(f"Analyzing {len(repos)} repositories in parallel..."):
        # Use ThreadPoolExecutor to scan repos simultaneously (Supports 10+ easily)
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            future_to_repo = {executor.submit(scan_single_repo, repo): repo for repo in repos}
            for future in concurrent.futures.as_completed(future_to_repo):
                all_violations.extend(future.result())

    if all_violations:
        df = pd.DataFrame(all_violations)
        
        # --- EXECUTIVE DASHBOARD ---
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Findings", len(df))
        col2.metric("Critical Risks", len(df[df['Risk Level'] == 'Critical']))
        col3.metric("Total Exposure ($)", f"${df['Potential Loss ($)'].sum():,}")
        col4.metric("Action Items", len(df))
        
        st.subheader("Risk Distribution & Execution Matrix")
        st.dataframe(df, use_container_width=True)
        
        # --- EXCEL EXPORT ---
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Security Findings')
        
        st.download_button("Download Full Risk & Remediation Report (.xlsx)", buffer.getvalue(), 
                           "IRIS_Holistic_Report.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    else:
        st.success("✅ Clean: No risks detected across all repositories.")