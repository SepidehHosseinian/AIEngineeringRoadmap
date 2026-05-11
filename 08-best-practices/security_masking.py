"""
BEST PRACTICE #4: Security First (PII Masking)
Goal: Anonymize sensitive data before sending to 3rd-party LLMs.
"""
import re

def mask_sensitive_info(text):
    # Patterns for Credit Cards and National IDs
    card_pattern = r'\d{4}-\d{4}-\d{4}-\d{4}'
    ssn_pattern = r'\d{3}-\d{2}-\d{4}'
    
    masked_text = re.sub(card_pattern, "[CARD_REDACTED]", text)
    masked_text = re.sub(ssn_pattern, "[ID_REDACTED]", masked_text)
    return masked_text

if __name__ == "__main__":
    raw_user_query = "My card number is 1234-5678-9012-3456 and my ID is 123-45-6789."
    print("Sending to OpenAI API:", mask_sensitive_info(raw_user_query))