import re

"""
================================================================================
TECHNICAL DECISION: PII Masking (Security Guardrails)
================================================================================
Why: To ensure sensitive user data never reaches the LLM provider,
complying with data privacy regulations (like GDPR or local banking laws).
================================================================================
"""

def mask_sensitive_info(text: str):
    # Masking National ID (10 digits) and Card Numbers (16 digits)
    masked = re.sub(r'\d{10}', '[NATIONAL_ID_MASKED]', text)
    masked = re.sub(r'\d{16}', '[CARD_NUM_MASKED]', masked)
    return masked

if __name__ == "__main__":
    user_input = "شماره ملی من 1234567890 است و شماره کارتم 6037991234567890."
    print("Original:", user_input)
    print("Safe Version:", mask_sensitive_info(user_input))