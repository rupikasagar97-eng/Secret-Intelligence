import streamlit as st
import os
import re
import subprocess
import tempfile
import shutil

# 1. Real-Time Secret Signatures
SECRET_PATTERNS = {
    "GitHub Personal Access Token": r"ghp_[a-zA-Z0-9]{36}",
    "AWS Access Key ID": r"AKIA[0-9A-Z]{16}",
    "Exposed Database Password/Secret": r"(?-i)(password|secret|api_key|passwd)\s*=\s*['\"]([^'\"]+)['\"]",
    "Slack Webhook URL": r"https://hooks\.slack\.com/services/T[A-Z0-9]+/B[A-Z0-9]+/[A-Za-z0-9]+"
}

# 2. Streamlit UI Configuration
st.set_page_config(page_title="IRIS Secret Intelligence Engine", page_icon="🛡️", layout="wide")

st.title("🛡️ IRIS: Real-Time SDLC Threat Intelligence Engine")
st.markdown("""
This interactive platform allows recruiters and engineers to audit public GitHub repositories for exposed credentials, 
high-entropy tokens, and lateral-movement vectors in real time.
""")

st.sidebar.header("Scanner Configuration")
repo_url = st.text_input("Enter Public GitHub Repository URL to Scan:", placeholder="https://github.com/username/repository")

if st.button("Launch Live Real-Time Scan"):
    if not repo_url:
        st.error("Please provide a valid GitHub repository URL.")
    else:
        with st.spinner("Initializing isolated runtime environment and cloning target asset..."):
            # Create an isolated temporary directory to pull the recruiter's repo into
            temp_dir = tempfile.mkdtemp()
            
            try:
                # Perform a shallow clone (depth 1) to make the real-time scan incredibly fast
                result = subprocess.run(
                    ["git", "clone", "--depth", "1", repo_url, temp_dir],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                
                if result.returncode != 0:
                    st.error(f"Failed to clone repository. Ensure the link is public. Error: {result.stderr}")
                    shutil.rmtree(temp_dir)
                    st.stop()
                
                st.success("Target asset successfully isolated. Commencing dynamic signature analysis...")
                st.divider()
                
                # 3. Live Scanning Execution Loop
                violations_found = []
                
                for root, dirs, files in os.walk(temp_dir):
                    # Skip internal git metadata
                    if '.git' in root.split(os.sep):
                        continue
                        
                    for file in files:
                        file_path = os.path.join(root, file)
                        relative_path = os.path.relpath(file_path, temp_dir)
                        
                        try:
                            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                                for line_number, line in enumerate(f, 1):
                                    for label, pattern in SECRET_PATTERNS.items():
                                        match = re.search(pattern, line)
                                        if match:
                                            violations_found.append({
                                                "file": relative_path,
                                                "line": line_number,
                                                "type": label,
                                                "leak": f"{match.group(0)[:6]}..."
                                            })
                        except Exception:
                            pass # Safely bypass binary/system unreadable files
                
                # 4. Display Real-Time Metrics & Forensic Logs
                if violations_found:
                    st.metric(label="Pipeline Security Status", value="BREACHED", delta="- Critical Vulnerabilities", delta_color="inverse")
                    st.error(f"🚨 Security Gate Breached: Found {len(violations_found)} unencrypted credential exposures.")
                    
                    # Display forensic table
                    st.subheader("📋 Forensic Threat Intelligence Report")
                    st.table(violations_found)
                else:
                    st.metric(label="Pipeline Security Status", value="SECURE", delta="0 Threat Profiles Detected")
                    st.success("✅ Security Gate Passed: No high-entropy keys or credentials found in the scanned target branch.")
                    
            except Exception as e:
                st.error(f"An error occurred during execution processing: {e}")
            finally:
                # Clean up the system memory/disk after the scan wraps up
                if os.path.exists(temp_dir):
                    shutil.rmtree(temp_dir)
