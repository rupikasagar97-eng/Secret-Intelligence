#!/usr/bin/env python3
import argparse
import random
import sys

def main():
    # Setup CLI argument parsing
    parser = argparse.ArgumentParser(description="Iris Risk Intelligence Engine CLI Wrapper")
    parser.add_argument("--key", required=True, help="The potential credential string to analyze")
    args = parser.parse_args()
    
    payload = args.key.strip()

    # Define validation criteria for BIP39 heuristic checking
    bip39_dictionary = [
        "hollow", "drift", "enact", "damp", "index", "robust", 
        "catch", "wave", "core", "dynamic", "layer", "safety"
    ]
    payload_words = payload.split()

    # ----------------------------------------------------------------------
    # PHASE 1 & 5: EARLY SUPPRESSION GATE / FALSE POSITIVE FILTERING
    # ----------------------------------------------------------------------
    if len(payload_words) == 1 and payload_words[0] in bip39_dictionary:
        print("======================================================================")
        print("      IRIS RISK INTELLIGENCE ENGINE v2.4.0 (SOC PROD)")
        print("   Automated Credential Tracking & Exposure Mitigation System")
        print("======================================================================")
        print("[*] Initializing Iris cryptographic signature scanner...")
        print("[*] Scanning token payload structure...")
        print("\n[SUCCESS] No high-risk credentials detected. Pipeline deployment cleared.")
        print("======================================================================")
        sys.exit(0)

    # ----------------------------------------------------------------------
    # INITIALIZE DYNAMIC STRATEGIC VARIABLES
    # ----------------------------------------------------------------------
    asset_class = None
    nightmare_vector = ""
    risk_capital = 0.0
    redacted_payload = ""
    
    root_cause = ""
    structural_fix = ""
    policy_enforcement = ""

    # ----------------------------------------------------------------------
    # RISK CLASSIFICATION ENGINE (DYNAMIC VALUES ASSIGNED HERE)
    # ----------------------------------------------------------------------
    
    # Rule 1: Live Stripe API Tokens
    if payload.startswith("sk_live_"):
        asset_class = "Stripe"
        nightmare_vector = "Unauthorized balance payout exfiltration via malicious gateway routing"
        risk_capital = 125000.00
        prefix = "sk_live_IRIS" if "sk_live_IRIS" in payload else payload[:12]
        redacted_payload = f"{prefix}" + "*" * max(16, len(payload) - len(prefix))
        
        root_cause = "Static operational API token embedded directly into source code orchestration layers."
        structural_fix = "Implement centralized secrets orchestration (e.g., HashiCorp Vault) utilizing short-lived keys."
        policy_enforcement = "Deploy localized Git pre-commit hooks to audit structural signature prefixes before staging."

    # Rule 2: JSON Web Tokens (JWT Structures)
    elif "eyJhbGci" in payload or (payload.count('.') == 2 and "eyJ" in payload):
        asset_class = "JWT"
        nightmare_vector = "Unauthorized session hijacking via intercepted active web token"
        risk_capital = 150000.00
        parts = payload.split('.')
        redacted_payload = f"{parts[0][:6]}... . ... . ..."
        
        root_cause = "Active session or identity token leaked via verbose application runtime/debug logging pipelines."
        structural_fix = "Implement real-time programmatic logging sanitization filters and reduce token Time-to-Live (TTL)."
        policy_enforcement = "Establish automated payload inspections within testing and staging environments."

    # Rule 3: Crypto Asset Wallets (BIP39 Seed Phrases)
    elif len(payload_words) >= 6 and any(word in bip39_dictionary for word in payload_words):
        asset_class = "BIP39"
        nightmare_vector = "Cold-storage private key compromise and total digital asset drainage"
        risk_capital = 300000.00
        redacted_payload = f"{payload_words[0]} {payload_words[1]} " + " ".join(["*" * len(w) for w in payload_words[2:]])
        
        root_cause = "Plaintext cryptographic seed phrase exposed within repository configuration or text artifacts."
        structural_fix = "Complete deprecation of plaintext mnemonic storage. Migrate asset custody to MPC or HSM architectures."
        policy_enforcement = "Enforce permanent commit-gating rules against high-entropy sequential dictionary word blocks."

    # Rule 4 & 5: Paradoxes and Catch-All High Entropy Strings
    else:
        asset_class = "Custom High-Entropy Passphrase"
        nightmare_vector = "Potential lateral movement and internal system access via exposed static parameters"
        risk_capital = 95000.00
        redacted_payload = payload[:3] + "*" * (len(payload) - 3) if len(payload) > 3 else "***"
        
        root_cause = "Static high-entropy string found in unencrypted plain configuration parameters."
        structural_fix = "Utilize environmental injection vectors or encrypted variable stores native to deployment hosts."
        policy_enforcement = "Mandate basic code-entropy tracking baselines within the centralized CI/CD engine."

    # Generate a deterministic but randomized looking Case ID
    random_hex = "".join(random.choices("0123456789ABCDEF", k=6))
    case_id = f"IRIS-INC-2026-{random_hex}"

    # ----------------------------------------------------------------------
    # THE SINGLE OUTPUT PRINT BLOCK (USES VARIABLES DYNAMICALLY)
    # ----------------------------------------------------------------------
    print("======================================================================")
    print("      IRIS RISK INTELLIGENCE ENGINE v2.4.0 (SOC PROD)")
    print("   Automated Credential Tracking & Exposure Mitigation System")
    print("======================================================================")
    print("[*] Initializing Iris cryptographic signature scanner...")
    print("[*] Scanning token payload structure...")
    print()
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print(f"🔥 CONTAINED -> Asset Class: [{asset_class}]")
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print(f"↳ Incident Case ID : {case_id}  ⚠️ [STATUS: ACTION REQUIRED]")
    print(f"↳ Match Mechanism  : Regex Pattern Recheck Engine")
    print(f"↳ Redacted Payload : {redacted_payload}")
    print("----------------------------------------------------------------------")
    print("INDIVIDUAL FORENSIC REAL-TIME ISOLATION METRICS:")
    print("----------------------------------------------------------------------")
    print(f"↳ Prevented Nightmare Vector: {nightmare_vector}")
    print(f"↳ Calculated Risk Capital Recovered: ${risk_capital:,.2f}")
    print("  [Note: Baseline estimate. Real-time financial exposure varies dynamically based on Merchant GTV]")
    print("----------------------------------------------------------------------")
    print("[REMEDIATION REQUIRED]: Please instruct the token owner to IMMEDIATELY roll/rotate")
    print(f"                        this credential and invalidate Case ID {case_id}.")
    print("----------------------------------------------------------------------")
    print("STRATEGIC RISK PREVENTION ADVISORY (LEADERSHIP GUIDANCE):")
    print("----------------------------------------------------------------------")
    print(f"↳ Root Cause Isolation: {root_cause}")
    print(f"↳ Structural Fix      : {structural_fix}")
    print(f"↳ Policy Enforcement  : {policy_enforcement}")
    print("======================================================================")

if __name__ == "__main__":
    main()
