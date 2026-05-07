"""
DESIGN PATTERN: Reflection Pattern
The agent generates an answer, critiques it, and regenerates if necessary.
Essential for high-accuracy domains like Fintech (AzkiVam) and Banking (Behsazan).
"""

import logging
from typing import Dict

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger("ReflectionAgent")

class ReflectionAgent:
    def __init__(self, model_name: str = "gpt-4o"):
        self.model_name = model_name

    def generate_initial_answer(self, query: str) -> str:
        """Step 1: First draft generation."""
        logger.info("Generating initial draft...")
        # Simulating LLM response
        return "The daily transfer limit is 50 million Tomans for all users."

    def critique_answer(self, query: str, answer: str) -> Dict[str, str]:
        """Step 2: Self-critique to find potential hallucinations or errors."""
        logger.info("Critiquing the draft...")
        
        # Simulating a critique logic
        if "all users" in answer.lower():
            return {
                "is_accurate": "no",
                "critique": "The limit for verified users (KYC Level 2) is actually 100 million, not 50."
            }
        return {"is_accurate": "yes", "critique": "None"}

    def improve_answer(self, original_query: str, draft: str, critique: str) -> str:
        """Step 3: Regenerating a refined answer based on the critique."""
        logger.info("Refining answer based on critique...")
        return "The daily transfer limit is 50 million Tomans for standard users, but verified users (KYC Level 2) can transfer up to 100 million Tomans."

    def run(self, query: str):
        # Execution Flow
        draft = self.generate_initial_answer(query)
        review = self.critique_answer(query, draft)
        
        if review["is_accurate"] == "no":
            final_answer = self.improve_answer(query, draft, review["critique"])
        else:
            final_answer = draft
            
        return final_answer

if __name__ == "__main__":
    agent = ReflectionAgent()
    user_query = "What is the daily transfer limit?"
    
    result = agent.run(user_query)
    print(f"\nFinal Verified Answer:\n{result}")