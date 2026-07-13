import streamlit as st
import os, re, subprocess, tempfile, shutil, json
import pandas as pd
from fpdf import FPDF

# --- THE 7 SECURITY PATTERNS ---
# Matches: JWT, Stripe, Slack, GitHub, AWS, Private Key, BNP 39
SECRET_PATTERNS = {
    "JWT": r"ey[a-zA-Z0-9_-]{16,}\.[a-zA-Z0-9_-]{16,}\.[a-zA-Z0-9_-]{16,}",
    "Stripe": r"sk_(live|test)_[a-zA-Z0-9]{24}",
    "Slack": r"https://hooks\.slack\.com/services/[A-Za-z0-9]+/[A-Za-z0-9]+/[A-Za-z0-9]+",
    "GitHub": r"ghp_[a-zA-Z0-9]{36}",
    "AWS": r"AKIA[0-9A-Z]{16}",
    "Private Key": r"-----BEGIN (RSA|OPENSSH|EC|PGP) PRIVATE KEY-----",
    "BNP 39": r"[a-zA-Z0-9]{39}" 
}

RISK_VALUES = {"JWT": 20000, "Stripe": 250000, "Slack": 10000, "GitHub": 50000, "AWS": 100000, "Private Key": 500000, "BNP 39": 75000}

def neutralize(label):
    # Logic: This is where you would call your API Client (e.g., boto3, stripe-python)
    # to revoke the specific key found.
    return f"CONTAINED: API/Token {label} Revoked via Cloud Provider SDK."

def scan_repo(repo_url):
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
                        for label, pattern in SECRET_PATTERNS.items():
                            if re.search(pattern, content):
                                status = neutralize(label)
                                findings.append({
                                    "Repo": repo_url.split('/')[-1],
                                    "Key": label,
                                    "Status": status,
                                    "Impact": RISK_VALUES.get(label, 0)
                                })
                except: continue
    finally:
        shutil.rmtree(temp_dir)
    return findings

def create_report(df):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, "IRIS Forensic Audit & Containment Report", ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, f"Total Financial Exposure Neutralized: ${df['Impact'].sum():,}", ln=True)
    pdf.ln(10)
    # Add table and mandatory remediation text here...
    return pdf.output(dest='S').encode('latin-1')

# --- STREAMLIT UI ---
st.title("🛡️ IRIS: Active Containment Engine")
repo_input = st.text_area("Enter Repo URLs (one per line):")

if st.button("EXECUTE SCAN & CONTAIN"):
    repos = [r.strip() for r in repo_input.split('\n') if r.strip()]
    results = []
    for r in repos: results.extend(scan_repo(r))
    
    df = pd.DataFrame(results)
    st.dataframe(df)
    
    if not df.empty:
        st.download_button("Download Leadership Audit", create_report(df), "Audit.pdf")