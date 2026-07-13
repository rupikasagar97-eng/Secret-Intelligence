import streamlit as st
import os
import re
import subprocess
import tempfile
import shutil

# The Engine Logic
SECRET_PATTERNS = {
    "GitHub Personal Access Token": r"ghp_[a-zA-Z0-9]{36}",
    "AWS Access Key ID": r"AKIA[0-9A-Z]{16}",
    "Exposed Password/Secret": r"(?i)(password|secret|api_key|passwd)\s*=\s*['\"]([^'\"]+)['\"]",
    "Slack Webhook URL": r"https://hooks\.slack\.com/services/T[A-Z0-9]+/B[A-Z0-9]+/[A-Za-z0-9]+"
}

st.set_page_config(page_title="IRIS Scanner", page_icon="🛡️")
st.title("🛡️ IRIS: Live Security Engine")
st.write("Enter any public GitHub repository to scan for hardcoded secrets in real-time.")

repo_url = st.text_input("Repository URL:", "https://github.com/rupikasagar97-eng/Secret-Intelligence")

if st.button("Run Real-Time Scan"):
    with st.spinner("Scanning repository..."):
        temp_dir = tempfile.mkdtemp()
        
        # Clone repo
        clone_result = subprocess.run(["git", "clone", "--depth", "1", repo_url, temp_dir], capture_output=True)
        
        if clone_result.returncode != 0:
            st.error("Could not scan repo. Ensure it is public.")
        else:
            violations = []
            for root, _, files in os.walk(temp_dir):
                if '.git' in root: continue
                for file in files:
                    file_path = os.path.join(root, file)
                    with open(file_path, "r", errors="ignore") as f:
                        content = f.read()
                        for label, pattern in SECRET_PATTERNS.items():
                            if re.search(pattern, content):
                                violations.append({"File": file, "Issue": label})
            
            if violations:
                st.error("🚨 Leaks Detected!")
                st.table(violations)
            else:
                st.success("✅ Clean: No secrets found.")
        
        shutil.rmtree(temp_dir)