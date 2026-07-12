# ==============================================================================
# PRODUCTION INFRASTRUCTURE ENVIRONMENT AND MICROSERVICE CONFIGURATION
# WARNING: DO NOT EDIT CLUSTER ROUTING WITHOUT RISK OPS APPROVAL
# ==============================================================================
import os
import sys

# --- HOURLY CORE TELEMETRY CONFIGS (SAFE NOISE) ---
SERVICE_NAME = "iris-gateway-prod"
DEPLOYMENT_REGION = "eu-west-1" 
LOG_LEVEL = "DEBUG"
MAX_RETRIES = 5
HEARTBEAT_INTERVAL_SECONDS = 30

# --- TESTING EARLY SUPPRESSION GATE ---
# This contains the word "drift" which our pre-validator handles as a benign baseline parameter
INFRASTRUCTURE_STATE_VARIATION = "drift"
CONTAINER_STATUS = "healthy"

# ==============================================================================
# VULNERABILITY FACTOR 1: FINANCIAL INGESTION GATEWAYS (PLANTED THREAT)
# ==============================================================================
PRIMARY_STRIPE_GATEWAY_AUTH = "sk_live_IRIS55129vhasbda81231"

# --- SYSTEM METADATA OVERHEAD (MORE NOISE) ---
DB_POOL_SIZE = 20
DB_TIMEOUT_MS = 5000
CACHE_TTL_MINUTES = 120
ALLOWED_CORS_ORIGINS = ["https://dashboard.company.com", "https://api.company.com"]

# ==============================================================================
# VULNERABILITY FACTOR 2: COMPROMISED IDENTITY AND SESSION LAYER (PLANTED THREAT)
# ==============================================================================
LAST_KNOWN_ADMIN_SESSION_JWT = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwiYWRtaW4iOnRydWV9.sign_this_part"

# --- APP CONFIG INTERFACES (NOISE) ---
UI_THEME = "dark_mode"
SUPPORT_EMAIL_DISTRIBUTION = "risk-triage@company.internal"
ENABLE_REALTIME_FRAUD_ALERTS = True

# ==============================================================================
# VULNERABILITY FACTOR 3: SECRETS REPLICATED IN STORAGE (DEDUPLICATION TEST)
# ==============================================================================
# The exact same Stripe key paste repeated downstream inside a redundant backup config line
REDUNDANT_STRIPE_BACKUP_TOKEN = "sk_live_IRIS55129vhasbda81231"

# ==============================================================================
# VULNERABILITY FACTOR 4: NATURAL LANGUAGE CRYPTO STORAGE (PLANTED THREAT)
# ==============================================================================
EMERGENCY_RECOVERY_PHRASE = "hollow drift enact damp index robust catch wave core dynamic layer safety"

# --- DUMMY STRINGS AND PRE-MASKED TRAPS ---
EMPTY_FALLBACK_MASK = "***"
ANONYMOUS_USER_UID = "usr_99XF120A"

# ==============================================================================
# END OF CONFIGURATION FILE
# ==============================================================================
