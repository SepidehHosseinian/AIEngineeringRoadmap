"""
================================================================================
STRATEGIC ASSET: Cost-Effective Tiered Inference
================================================================================
Logic:
1. Short/Simple queries -> Llama-3-8B (Cheap & Fast)
2. Complex/Reasoning queries -> GPT-4o or Llama-3-70B (Expensive & Smart)
================================================================================
"""

def route_query(query: str):
    # Simple heuristic: Length and keyword-based routing
    # In production, this can be a small classifier model.
    if len(query.split()) < 10 and "analyze" not in query.lower():
        return "Routing to SMALL_MODEL (Llama-3-8B) - Cost: $0.0001"
    else:
        return "Routing to LARGE_MODEL (GPT-4o) - Cost: $0.01"

if __name__ == "__main__":
    q1 = "سلام، موجودی من چقدر است؟"
    q2 = "لطفاً تراکنش‌های سه ماه اخیر من را تحلیل کن و نمودار مخارج من را بگو."
    
    print(f"Query 1: {route_query(q1)}")
    print(f"Query 2: {route_query(q2)}")
