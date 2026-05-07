from pydantic import BaseModel, Field
from typing import List, Optional

class SafetyCheckResult(BaseModel):
    """Data model for security check outcomes."""
    is_safe: bool = Field(description="Boolean flag indicating if content is safe")
    reason: Optional[str] = Field(description="Explanation for rejection if content is unsafe")
    risk_level: str = Field(description="Risk assessment: Low, Medium, High")

class GuardrailResponse(BaseModel):
    """Final system response model incorporating safety layers."""
    original_query: str
    is_allowed: bool
    sanitized_answer: str
    flagged_topics: List[str] = []

# List of prohibited topics for the enterprise environment
BANNED_TOPICS = [
    "internal_salary_details",
    "system_vulnerabilities",
    "competitor_praising",
    "political_opinions",
    "personal_data_leak"
]