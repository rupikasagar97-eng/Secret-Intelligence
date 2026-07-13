import streamlit as st
import os
import re
import subprocess
import tempfile
import shutil
import pandas as pd

# The Engine Logic
SECRET_PATTERNS = {
    "GitHub Personal Access Token": r"ghp_[a-zA-Z0-9]{36}",
    "AWS Access Key ID": r"AKIA[0-9A-Z]{16}",
    "Exposed Password/Secret": r"(?i)(password|secret|api_key|passwd)\s*=\s*['\"]([^'\"]+)['\"]",
    "Slack Webhook URL": r"https://hooks\.slack\.com/services/T[A-Z0-9]+/B[A-Z0-9]+/[A-Za-z0-9]+"
}

def get_severity(issue):
    """Assigns basic severity levels."""
    if "Token" in issue or "AWS" in issue: return "Critical"
    return "High"

st.set_page_config(page_title="IRIS Scanner", page_icon="🛡️", layout="wide")
st.title("🛡️ IRIS: Holistic Security Engine")

# Multi-repo input
repo_input = st.text_area("Enter Repository URLs (one per line):", 
                          "https://github.com/rupikasagar97-eng/Secret-Intelligence")

if st.button("Run Holistic Scan"):
    repos = [r.strip() for r in repo_input.split('\n') if r.strip()]
    all_violations = []

    with st.spinner("Analyzing repositories..."):
        for repo_url in repos:
            temp_dir = tempfile.mkdtemp()
            clone_result = subprocess.run(["git", "clone", "--depth", "1", repo_url, temp_dir], capture_output=True)
            
            if clone_result.returncode == 0:
                for root, _, files in os.walk(temp_dir):
                    if '.git' in root: continue
                    for file in files:
                        file_path = os.path.join(root, file)
                        try:
                            with open(file_path, "r", errors="ignore") as f:
                                content = f.read()
                                for label, pattern in SECRET_PATTERNS.items():
                                    if re.search(pattern, content):
                                        all_violations.append({
                                            "Repository": repo_url.split('/')[-1],
                                            "File": file, 
                                            "Issue": label,
                                            "Severity": get_severity(label)
                                        })
                        except Exception:
                            continue
            shutil.rmtree(temp_dir)

    if all_violations:
        # Holistic Report Components
        df = pd.DataFrame(all_violations)
        
        # Summary Metrics
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Leaks Found", len(df))
        col2.metric("Unique Files Affected", df['File'].nunique())
        col3.metric("Critical Alerts", len(df[df['Severity'] == 'Critical']))
        
        st.error("🚨 Security Findings Detected")
        st.table(df)
        
        # Download Report
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Full Report (CSV)", csv, "security_report.csv", "text/csv")
    else:
        st.success("✅ Clean: No secrets found in any repository.")
