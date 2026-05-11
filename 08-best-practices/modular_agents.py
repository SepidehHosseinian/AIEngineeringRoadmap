"""
BEST PRACTICE #5: Modular Agentic Design
Goal: Break complex tasks into specialized, testable agents.

"""

class BaseAgent:
    def init__(self, role):
        self.role = role

    def execute(self, task):
        print(f"--- [Agent: {self.role}] Processing task: {task} ---")

def run_multi_agent_pipeline(user_request):
    # Decomposing a large task into specialized components
    router = BaseAgent("Router")
    analyst = BaseAgent("Financial Analyst")
    summarizer = BaseAgent("Editor")

    router.execute("Classify request as Financial Analysis")
    analyst.execute("Analyze stock market trends for 2024")
    summarizer.execute("Create a concise summary for the user")

if __name == "__main__":
    run_multi_agent_pipeline("Give me a market report for Apple Inc.")
