"""
================================================================================
STRATEGIC ASSET: Model Selection Logic (Logic-to-Choice Mapping)
================================================================================

This module simulates the decision-making process for choosing between 
Frontier Models (GPT-4), OS Models (Llama-3), and SLMs (Phi-3).
================================================================================
"""

class ModelSelector:
    @staticmethod
    def select_model(task_complexity: str, data_privacy: bool, budget: str):
        """
        Decision Matrix:

        - Complexity: High (Reasoning) | Mid (Summary) | Low (Classification)
        - Privacy: True (On-premise required) | False (Cloud OK)
        - Budget: High | Low
        """

        if data_privacy:
            if task_complexity == "High":
                return "Llama-3-70B (Self-hosted on A100s)"
            return "Llama-3-8B or Phi-3 (Edge Deployment)"

        if not data_privacy:
            if task_complexity == "High" and budget == "High":
                return "Claude 3.5 Sonnet / GPT-4o"
            if budget == "Low":
                return "GPT-4o-mini or Groq-hosted Llama-3"

        return "Hybrid Approach: RAG + SLM"

# --- Simulation ---
if name == "__main__":
    # Scenario: Financial Data Analysis (High Privacy, High Complexity)
    choice = ModelSelector.select_model(
        task_complexity="High", 
        data_privacy=True, 
        budget="Mid"
    )
    print(f"🎯 Recommended Architecture: {choice}")