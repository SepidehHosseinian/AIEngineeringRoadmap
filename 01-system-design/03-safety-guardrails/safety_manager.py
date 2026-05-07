from .02_input_analyzer import InputGuardrail
from .03_output_monitor import OutputGuardrail

class SafetyManager:
    """
    A unified interface to manage both input and output guardrails.
    Can be easily integrated into any RAG or Agentic pipeline.
    """
    def __init__(self):
        self.input_guard = InputGuardrail()
        self.output_guard = OutputGuardrail()

    def process_request(self, user_query: str, rag_callback_func):
        """
        Wraps the core RAG logic with safety shields.
        
        Args:
            user_query (str): The raw input from user.
            rag_callback_func: The function that retrieves data and generates a response.
        """
        # Step 1: Input Validation
        input_check = self.input_guard.validate_input(user_query)
        if not input_check.is_safe:
            return f"Access Denied: {input_check.reason} (Risk: {input_check.risk_level})"

        # Step 2: Execute Core RAG Logic
        # Expecting a tuple: (generated_text, retrieval_context)
        raw_answer, context = rag_callback_func(user_query)

        # Step 3: Output Validation and Masking
        final_answer = self.output_guard.secure_response(user_query, context, raw_answer)
        return final_answer