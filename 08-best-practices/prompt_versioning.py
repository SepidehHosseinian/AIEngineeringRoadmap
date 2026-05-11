"""
BEST PRACTICE #1: Prompt Versioning
Goal: Decouple prompts from logic and track versions.
"""

PROMPT_REGISTRY = {
    "v1.0": "Answer the following question: {query}",
    "v1.1": "You are a helpful assistant. Answer the following query: {query}",
    "v1.2": "You are a Senior Financial Expert. Provide a detailed analysis for: {query}"
}

def run_inference(query, version="v1.2"):
    template = PROMPT_REGISTRY.get(version, PROMPT_REGISTRY["v1.0"])
    formatted_prompt = template.format(query=query)
    
    print(f"--- [LOG] Executing Prompt Version: {version} ---")
    print(f"--- [LOG] Prompt String: {formatted_prompt} ---")
    # LLM Call Logic would go here
    return "LLM Response based on " + version

if __name__ == "__main__":
    run_inference("How to diversify my investment portfolio?")