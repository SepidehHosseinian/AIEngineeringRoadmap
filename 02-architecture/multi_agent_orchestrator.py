"""
DESIGN PATTERN: Multi-Agent Orchestration (Supervisor Pattern)
Delegating tasks to specialized agents (Analyst vs. Researcher).
Tooling Suggestion: Implement using LangGraph for complex state management.
"""

class SpecializedAgent:
    def __init__(self, name: str, expertise: str):
        self.name = name
        self.expertise = expertise

    def work(self, task: str):
        return f"[{self.name}] processed the task '{task}' using {self.expertise} expertise."

class Orchestrator:
    def __init__(self):

        self.researcher = SpecializedAgent("Researcher", "Document Retrieval")
        self.analyst = SpecializedAgent("Analyst", "Numerical/Excel Data")

    def route_task(self, user_query: str):
        """Logic to decide which agent should handle the request."""
        print(f"Orchestrator: Analyzing query -> {user_query}")

        if any(word in user_query.lower() for word in ["calculate", "profit", "loan"]):
            return self.analyst.work(user_query)
        else:
            return self.researcher.work(user_query)

if name == "__main__":
    master = Orchestrator()

    # Scenario 1: Needs Analysis
    print(master.route_task("Calculate the total interest for a 12-month loan."))

    # Scenario 2: Needs Research
    print(master.route_task("What are the terms and conditions for opening an account?"))
