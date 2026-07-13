IRIS: Intelligent Repository Intelligence & Secret-detection System
An automated credential exposure detection and risk quantification engine — built to operationalize early-stage fraud prevention at the infrastructure layer.

Live Demo: https://hello-who--rupikasagar97.replit.app

What This Is
Exposed API keys are one of the most common and costly vectors for payment fraud. When a Stripe secret key, AWS credential, or JWT is committed to a public repository, it can be harvested by automated scanners within minutes — enabling unauthorized charges, account takeovers, and large-scale financial loss.

IRIS automates the detection, containment, and reporting of these exposures. It scans GitHub repositories, identifies live credentials, quantifies the estimated financial risk, and generates a leadership-ready forensic audit report — all in under 60 seconds.

This project was built as a proof-of-concept connecting infrastructure security to fraud strategy: the same credential types that enable payment fraud are the ones IRIS detects.

What It Detects
Credential Type	Threat Vector	Estimated Risk
Stripe Live API Key (sk_live_...)	Unauthorized balance payout / gateway fraud	$125,000
AWS Access Key (AKIA...)	Full cloud infrastructure takeover	$200,000
JSON Web Token (JWT)	Session hijacking / account takeover	$150,000
Slack API Token (xoxb-...)	Workspace data exfiltration	$75,000
GitHub Personal Access Token	Repository takeover / supply chain attack	$180,000
BIP39 Crypto Seed Phrase	Total digital asset drainage	$300,000
How It Works
GitHub Repo URL
      |
      v
GitHub API  ──►  File Content Fetch (no git clone required)
      |
      v
IRIS Detection Engine  ──►  Regex + Semantic Pattern Matching
      |
      v
False Positive Filter  ──►  Strips mock/test/example strings
      |
      v
Risk Scoring Matrix  ──►  Per-credential financial exposure estimate
      |
      v
Forensic Case Token  ──►  Case ID, redacted payload, root cause, remediation
      |
      v
Leadership PDF Report  ──►  Executive summary + mandatory remediation protocol

Pipeline Phases
Phase 1 (Complete): Deterministic regex scanner + interactive Streamlit dashboard. Supports multi-repo batch scanning (up to 10 repositories per run).

Phase 2 (In Development): LLM Risk Intelligence Agent for dynamic, context-aware analysis of credential exposure patterns and blast radius estimation.

Phase 3 (Planned): Containerized Python microservice via Docker for distributed deployment.

Phase 4 (Planned): GitHub Actions pre-merge security gate — blocks commits containing live credentials before they reach the repository.

Fraud Strategy Context
This tool sits at the intersection of infrastructure security and financial fraud prevention:

Stripe secret key exposure → fraudulent API charges, unauthorized payouts
AWS key exposure → provisioning of infrastructure for fraud-at-scale operations
JWT exposure → account takeover fraud, identity impersonation
GitHub PAT exposure → supply chain compromise, injection of malicious payment flows
Early detection at the code layer is materially cheaper than detection at the transaction layer. IRIS operationalizes that principle.

Repository Structure
iris_engine.py          # Core CLI detection engine (credential classification + risk scoring)
iris_app.py             # Streamlit web application (multi-repo scanner + PDF report)
Production_config.py    # Sample production config containing dummy secrets (for demo purposes)
production.csv          # Sample data file containing dummy secrets (for demo purposes)
.github/workflows/
  iris-pipeline.yml     # GitHub Actions: manual pipeline execution with test key input
  security-gate.yml     # GitHub Actions: pre-merge security scan gate

Running Locally
pip install streamlit fpdf2 requests pandas
streamlit run iris_app.py

Risk Methodology
Financial exposure estimates are baseline figures derived from published breach cost benchmarks and average merchant gross transaction volume (GTV) exposure. Real-world impact varies dynamically based on merchant scale, time-to-detection, and attacker sophistication. These figures are intended as risk-awareness proxies, not insurance valuations.

Author
Rupika Sagar Fraud Operations Associate, Stripe Bangalore [https://www.linkedin.com/in/rupika-sagar-548258152/]
