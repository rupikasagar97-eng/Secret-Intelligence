cat << 'EOF' > app.py
import streamlit as st
import subprocess
import os
import shutil
import uuid

st.set_page_config(page_title="Secret Intelligence Engine", page_icon="🛡️", layout="wide")

st.title("🛡️ Secret Intelligence Pipeline")
st.subheader("Enterprise Cyber Threat & Real-Time Repository Scanner")
st.write("Audit codebases instantly. Paste a public GitHub URL or upload a configuration file to isolate active credential leaks.")

st.divider()

# Create tabs for File Upload vs Live Git Scan
tab1, tab2 = st.tabs(["🌐 Scan Public GitHub Repository", "📁 Upload Local Configuration File"])

# --- TAB 1: GITHUB REPOSITORY SCANNING ---
with tab1:
    st.write("### Audit a Live Codebase")
    repo_url = st.text_input(
        "Enter Public GitHub Repository URL:", 
        placeholder="https://github.com/rupikasagar97-eng/Secret-Intelligence"
    )
    
    if st.button("🚀 Run Live Repository Audit"):
        if not repo_url:
            st.error("Please provide a valid GitHub repository URL.")
        else:
            # Generate a completely unique folder name to avoid collisions
            unique_id = str(uuid.uuid4())[:8]
            target_clone_dir = f"scan_target_{unique_id}"
            
            with st.spinner("Cloning repository branches and preparing stream-parser..."):
                try:
                    # 1. Clone the repo with depth=1 (blazing fast, no massive history download)
                    clone_res = subprocess.run(
                        ["git", "clone", "--depth", "1", repo_url, target_clone_dir],
                        capture_output=True, text=True
                    )
                    
                    if clone_res.returncode != 0:
                        st.error("Failed to clone repository. Verify the URL is public and typed correctly.")
                        st.code(clone_res.stderr)
                    else:
                        st.success("Repository successfully mapped into analysis sandbox! Scanning all assets...")
                        
                        # 2. Iterate through every single file in the repo
                        combined_report = ""
                        files_scanned = 0
                        secrets_found = 0
                        
                        for root, dirs, files in os.walk(target_clone_dir):
                            # Skip the internal .git metadata folder
                            if ".git" in root:
                                continue
                                
                            for file in files:
                                file_path = os.path.join(root, file)
                                files_scanned += 1
                                
                                # Run main.py scanner against this specific file
                                scan_res = subprocess.run(
                                    ["python", "main.py", "--file", file_path],
                                    capture_output=True, text=True
                                )
                                
                                # If the output contains alerts, track it
                                if "[ALERT]" in scan_res.stdout:
                                    # Clean up paths to make the readout beautiful for recruiters
                                    clean_path = file_path.replace(f"{target_clone_dir}/", "")
                                    readable_output = scan_res.stdout.replace(file_path, clean_path)
                                    combined_report += readable_output + "\n"
                                    secrets_found += 1
                        
                        # 3. Present the data beautifully to the recruiter
                        st.divider()
                        col1, col2 = st.columns(2)
                        col1.metric("Total Files Analyzed", files_scanned)
                        col2.metric("Compromised Assets Located", secrets_found, delta="Action Required", delta_color="inverse")
                        
                        if combined_report:
                            st.write("### 📊 Live Pipeline Threat Report")
                            st.code(combined_report, language="text")
                        else:
                            st.balloons()
                            st.success("✨ Flawless Audit! No high-entropy secrets or credential signatures found in this repository.")
                            
                except Exception as e:
                    st.error(f"An unexpected exception occurred: {str(e)}")
                finally:
                    # 4. Securely destroy the cloned repository folder after processing
                    if os.path.exists(target_clone_dir):
                        shutil.rmtree(target_clone_dir)

# --- TAB 2: STANDALONE FILE UPLOAD ---
with tab2:
    st.write("### Audit Single Configuration Asset")
    uploaded_file = st.file_uploader("Drag and drop your target file here", type=["env", "txt", "csv", "json", "py"])

    if uploaded_file is not None:
        temp_filename = f"temp_{uploaded_file.name}"
        with open(temp_filename, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.success(f"File '{uploaded_file.name}' loaded.")

        if st.button("🚀 Execute File Analysis"):
            with st.spinner("Analyzing high-entropy strings..."):
                try:
                    result = subprocess.run(
                        ["python", "main.py", "--file", temp_filename],
                        capture_output=True, text=True, check=True
                    )
                    st.divider()
                    st.write("### 📊 Live Pipeline Threat Report")
                    clean_output = result.stdout.replace(temp_filename, uploaded_file.name)
                    st.code(clean_output, language="text")
                except subprocess.CalledProcessError as e:
                    st.error("Engine Error encountered.")
                    st.code(e.stderr)
                finally:
                    if os.path.exists(temp_filename):
                        os.remove(temp_filename)
EOF
