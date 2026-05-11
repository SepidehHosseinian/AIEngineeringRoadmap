
from pydantic import BaseModel, Field
from typing import List

"""
================================================================================
GUARDRAILS: Structured Data Extraction
================================================================================
Ensuring the LLM output follows a strict schema for downstream API consumption.
================================================================================
"""

class TransactionAnalysis(BaseModel):
    category: str = Field(description="دسته بندی تراکنش مثلا پوشاک یا غذا")
    amount: float = Field(description="مبلغ تراکنش به تومان")
    is_suspicious: bool = Field(description="آیا تراکنش مشکوک است؟")

# این مدل باعث می‌شود خروجی LLM همیشه معتبر و قابل استفاده در دیتابیس باشد.
print("Schema defined for secure transaction processing.")