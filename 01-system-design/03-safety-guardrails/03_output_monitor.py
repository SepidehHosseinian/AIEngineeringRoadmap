import re
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

class OutputGuardrail:
    """
    Monitors AI-generated responses before they reach the user.
    Handles PII masking and Hallucination detection.
    """
    def __init__(self):
        self.llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)

        # Regex patterns for sensitive data masking (PII)
        self.sensitive_patterns = {
            "IP_ADDRESS": r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b',
            "CREDIT_CARD": r'\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b',
            "INTERNAL_URL": r'https?://internal\.(.)\.local'
        }

    def mask_sensitive_data(self, text: str) -> str:
        """Scans and redacts fixed-format sensitive information."""

        masked_text = text
        for label, pattern in self.sensitive_patterns.items():
            masked_text = re.sub(pattern, f"[REDACTED_{label}]", masked_text)
        return masked_text

    def check_hallucination(self, query: str, context: str, answer: str) -> bool:
        """
        Verifies if the generated answer is grounded in the provided context.
        Implements the 'Self-Correction' or 'Faithfulness' logic.
        """
        template = """
        As a Quality Assurance AI, verify if the Answer is strictly based on the Context.
        If the Answer contains information NOT present in the Context, flag it.

        CONTEXT: {context}
        QUERY: {query}
        ANSWER: {answer}

        Is the answer faithful to the context? Answer only 'Yes' or 'No'.
        """

        prompt = PromptTemplate(template=template, input_variables=["context", "query", "answer"])
        chain = prompt | self.llm
        response = chain.invoke({"context": context, "query": query, "answer": answer})

        return "yes" in response.content.lower()

    def secure_response(self, query: str, context: str, raw_answer: str) -> str:
        """Orchestrates all output safety checks."""
        # 1. Redact sensitive identifiers
        safe_text = self.mask_sensitive_data(raw_answer)

        # 2. Check for grounding (avoid hallucinations)
        is_faithful = self.check_hallucination(query, context, safe_text)

        if not is_faithful:
            return "Safety Alert: The generated answer could not be verified against official documents."

        return safe_text
