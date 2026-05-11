"""
CASE STUDY: Financial Underwriting Engine
A mini-demonstration of automated credit risk assessment.
"""

class UnderwritingEngine:
    def __init__(self):
        self.threshold = 700 # Minimum credit score for auto-approval

    def extract_financial_metrics(self, document_text):
        # In a real scenario, this would be an LLM extracting JSON
        print("--- [Agent] Extracting metrics from document... ---")
        return {
            "credit_score": 720,
            "debt_to_income_ratio": 0.35,
            "annual_income": 85000
        }

    def evaluate_risk(self, metrics):
        print("--- [Logic] Applying banking regulations... ---")
        if metrics["credit_score"] >= self.threshold and metrics["debt_to_income_ratio"] < 0.4:
            return "APPROVED (Low Risk)"
        return "REFERRED TO HUMAN (Manual Review Required)"

    def run_pipeline(self, doc):
        metrics = self.extract_financial_metrics(doc)
        decision = self.evaluate_risk(metrics)
        return f"Final Decision: {decision}"

if __name__ == "__main__":
    raw_doc = "User income is 85k with a credit history of 720..."
    engine = UnderwritingEngine()
    print(engine.run_pipeline(raw_doc))