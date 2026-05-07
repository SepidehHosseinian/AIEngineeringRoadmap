from .01_agent_function_calling import FinancialAgent
from 03_safety_guardrails.safety_manager import SafetyManager

class ProtectedFinancialAgent:
    """
    Combines the Financial Agent with the Guardrail Agent 
    as described in the Multi-Agent Orchestration section.
    """
    def __init__(self):
        self.agent = FinancialAgent()
        self.safety = SafetyManager()

    def run_safe_workflow(self, user_query: str):
        # This acts as the 'Orchestrator' logic
        print(f"Executing workflow for: {user_query}")
        
        # 1. Internal Safety Check (Input)
        # 2. Agent Execution (Tool Use)
        # 3. Final Compliance Check (Output) via SafetyManager
        
        # We wrap the agent's execute method as a callback for the safety manager
        safe_response = self.safety.process_request(
            user_query, 
            self._agent_callback
        )
        return safe_response

    def _agent_callback(self, query: str):
        # The SafetyManager expects (response, context)
        # For an agent, the context can be its 'internal thought process' or retrieved data
        result = self.agent.execute(query)
        return result['output'], "Agent internal reasoning and tool outputs"

if __name__ == "__main__":
    protected_agent = ProtectedFinancialAgent()
    # This query will be scrutinized by the Guardrail Agent before returning results
    final_output = protected_agent.run_safe_workflow("What is the ROI for 100M at 5% for 10 years?")
    print(f"Final Secure Output: {final_output}")