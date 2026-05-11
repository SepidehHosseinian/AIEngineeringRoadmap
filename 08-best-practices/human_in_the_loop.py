"""
BEST PRACTICE #3: Human-in-the-Loop (HITL)
Goal: Ensure high-risk actions require human verification.
"""

def process_transaction(amount):
    CRITICAL_THRESHOLD = 10000
    
    if amount >= CRITICAL_THRESHOLD:
        return "ACTION_REQUIRED: HUMAN_REVIEW_NEEDED"
    return "ACTION_SUCCESS: AUTO_PROCESSED"

def handle_ai_request(transaction_amount):
    print(f"--- [LOG] AI suggesting transaction of ${transaction_amount} ---")
    status = process_transaction(transaction_amount)
    
    if "HUMAN_REVIEW" in status:
        print(f"⚠️  High-risk detected! Freezing transaction for Admin approval.")
    else:
        print(f"✅ Low-risk transaction approved automatically.")

if __name__ == "__main__":
    handle_ai_request(15000) # Triggers HITL