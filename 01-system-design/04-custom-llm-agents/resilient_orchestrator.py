import os
import requests
from langchain_openai import ChatOpenAI
from langchain_community.llms import Ollama  # For Local Execution
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

class ResilientAIManager:
    """
    A Manager that switches between Cloud and Local LLMs 
    based on network availability (Critical for Iran's current situation).
    """
    def __init__(self):
        self.cloud_model = "gpt-4o"
        self.local_model = "llama3" # Assuming Ollama is running locally
        self.timeout = 5 # seconds

    def is_global_internet_available(self):
        """Checks if international API (like OpenAI) is reachable."""
        try:
            # Trying to ping OpenAI API or a global DNS
            requests.get("https://api.openai.com", timeout=self.timeout)
            return True
        except (requests.ConnectionError, requests.Timeout):
            return False

    def get_brain(self):
        """Decides which LLM to use based on the environment context."""
        if self.is_global_internet_available():
            print("🌐 Connection: Global. Using Cloud LLM (GPT-4o)...")
            return ChatOpenAI(model=self.cloud_model, temperature=0)
        else:
            print("🏠 Connection: Intranet/Offline. Switching to Local LLM (Ollama/Llama3)...")
            # In a real scenario, this would connect to an Ollama instance on a local server
            return Ollama(model=self.local_model)

    def execute_task(self, task_description: str):
        llm = self.get_brain()
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a resilient AI assistant operating in a constrained environment. "
                       "Your goal is to provide accurate technical advice regardless of connectivity."),
            ("user", "{input}")
        ])
        
        chain = prompt | llm | StrOutputParser()
        return chain.invoke({"input": task_description})

if __name__ == "__main__":
    manager = ResilientAIManager()
    
    # Example Task
    task = "How to optimize a SQL query for a banking transaction table?"
    response = manager.execute_task(task)
    
    print(f"\n[SYSTEM RESPONSE]:\n{response}")
