"""
BEST PRACTICE #2: Deterministic Over Probabilistic
Goal: Use Python for calculations to avoid LLM hallucinations.
"""

def calculate_compound_interest(principal, rate, time):
    """Deterministic calculation using standard formula."""
    return principal  (1 + rate) * time

def financial_agent_workflow(user_input):
    print(f"--- [LOG] Analyzing Input: '{user_input}' ---")

    # Simulating LLM extracting parameters (Structured Extraction)
    extracted_params = {"principal": 5000, "rate": 0.07, "time": 5}

    # Using code for the actual math
    final_amount = calculate_compound_interest(*extracted_params)

    return f"Calculated Amount (Deterministic): ${final_amount:,.2f}"

if name == "__main__":
    print(financial_agent_workflow("Calculate my return for $5000 at 7% for 5 years"))
