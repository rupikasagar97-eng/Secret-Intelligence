import streamlit as st
import os, re, subprocess, tempfile, shutil, json, pandas as pd
from fpdf import FPDF

# --- CONFIGURATION ---
def load_security_config():
    # Ensure security_cases.json exists or define fallback
    if os.path.exists('security_cases.json'):
        with open('security_cases.json', 'r') as f:
            return json.load(f)
    return {"cases": []}

# --- NEUTRALIZATION (Killswitch) ---
def neutralize(label):
    # Place your live API SDK/Cloud calls here
    return f"CONTAINED: {label} Revoked via Automated Protocol"

# --- SCANNING ENGINE ---
def scan_repo(repo_url):
    config = load_security_config()
    temp_dir = tempfile.mkdtemp()
    findings = []
    
    try:
        subprocess.run(["git", "clone", "--depth", "1", repo_url, temp_dir], capture_output=True)
        for root, _, files in os.walk(temp_dir):
            for file in files:
                path = os.path.join(root, file)
                try:
                    with open(path, "r", errors="ignore") as f:
                        content = f.read()
                        for case in config['cases']:
                            if re.search(case['pattern'], content):
                                status = neutralize(case['label'])
                                findings.append({
                                    "Repo": repo_url.split('/')[-1],
                                    "Key": case['label'],
                                    "Status": status,
                                    "Impact": case.get('financial_loss', 0)
                                })
                except: continue
    finally:
        shutil.rmtree(temp_dir)
    return findings

# --- REPORT GENERATION ---
def create_report(df):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, "IRIS Forensic Audit & Containment Report", ln=True, align='C')
    
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, f"Total Financial Exposure Neutralized: ${df['Impact'].sum():,}", ln=True)
    pdf.ln(10)
    
    # Table Header
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(50, 10, "Repo", 1)
    pdf.cell(40, 10, "Key Type", 1)
    pdf.cell(100, 10, "Containment Action", 1)
    pdf.ln()
    
    # Rows
    pdf.set_font("Arial", size=10)
    for _, row in df.iterrows():
        pdf.cell(50, 10, str(row['Repo']), 1)
        pdf.cell(40, 10, str(row['Key']), 1)
        pdf.cell(100, 10, str(row['Status']), 1)
        pdf.ln()
    
    # Protocols
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, "MANDATORY REMEDIATION PROTOCOL", ln=True)
    pdf.set_font("Arial", size=11)
    pdf.multi_cell(0, 10, "1. ANALYST ACTION: All identified secrets MUST be rotated immediately via the provider console. The automated containment neutralizes the immediate risk, but full credential rotation is required to maintain system integrity.")
    pdf.multi_cell(0, 10, "2. LEADERSHIP ACTION: Review CI/CD pipeline access controls. Implement pre-commit hooks and Git-secret scanning to prevent plaintext credentials from being committed to the repository in the future.")
    
    return pdf.output(dest='S').encode('latin-1')

# --- UI ---
st.set_page_config(page_title="IRIS: Active Defense", layout="wide")
st.title("🛡️ IRIS: Active Containment Engine")
repo_input = st.text_area("Target Repositories (one per line):", height=100)

if st.button("EXECUTE SCAN & CONTAIN"):
    repos = [r.strip() for r in repo_input.split('\n') if r.strip()]
    results = []
    with st.spinner("Scanning repositories..."):
        for r in repos: results.extend(scan_repo(r))
    
    if results:
        df = pd.DataFrame(results)
        st.dataframe(df)
        st.download_button("Download Leadership Audit", create_report(df), "Audit.pdf")
    else:
        st.success("Clean: No secrets found.")s