import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Load environment variables
load_dotenv()

class ReflectiveAgent:
    """
    Implements the 'Reflection Pattern'.
    The agent generates an initial response, critiques it, 
    and then refines it for maximum accuracy and professional tone.
    """
    def __init__(self):
        # Using a high-reasoning model for the reflection loop
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0.2)
        self.parser = StrOutputParser()

    def _generate_initial_draft(self, user_query: str) -> str:
        """First pass: Generate a basic response."""
        prompt = ChatPromptTemplate.from_template(
            "You are an expert AI Engineer. Provide a detailed answer to: {query}"
        )
        chain = prompt | self.llm | self.parser
        return chain.invoke({"query": user_query})

    def _critique_response(self, draft: str) -> str:
        """Second pass: Identify flaws, missing edge cases, or tone issues."""
        prompt = ChatPromptTemplate.from_template(
            "Critique the following AI-generated response. "
            "Look for technical inaccuracies, lack of depth, or readability issues. "
            "Be harsh and professional. \n\nDRAFT: {draft}"
        )
        chain = prompt | self.llm | self.parser
        return chain.invoke({"draft": draft})

    def _refine_response(self, draft: str, critique: str) -> str:
        """Third pass: Produce the final polished output based on the critique."""
        prompt = ChatPromptTemplate.from_template(
            "Update the initial draft by incorporating the feedback from the critique. "
            "Ensure the final output is world-class and production-ready.\n\n"
            "INITIAL DRAFT: {draft}\n\n"
            "CRITIQUE: {critique}"
        )
        chain = prompt | self.llm | self.parser
        return chain.invoke({"draft": draft, "critique": critique})

    def run(self, user_query: str):
        """Orchestrates the Reflection Loop."""
        print(f"--- Step 1: Generating Draft ---")
        draft = self._generate_initial_draft(user_query)
        
        print(f"--- Step 2: Critiquing ---")
        critique = self._critique_response(draft)
        
        print(f"--- Step 3: Refining ---")
        final_output = self._refine_response(draft, critique)
        
        return {
            "draft": draft,
            "critique": critique,
            "final_output": final_output
        }

if __name__ == "__main__":
    agent = ReflectiveAgent()
    query = "Explain the advantages of using Vector Databases over traditional RDBMS for LLM applications."
    
    result = agent.run(query)
    
    print("\n[FINAL REFLECTED OUTPUT]:")
    print(result['final_output'])