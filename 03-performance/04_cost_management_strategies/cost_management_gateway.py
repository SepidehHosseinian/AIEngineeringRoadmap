"""
================================================================================
TECHNICAL DECISION: Cost Optimization Gateway (Caching, Compression, Routing)
================================================================================

1. CONTEXT:
   LLM calls are expensive (tokens) and slow. We need a "Gateway" that 
   intercepts requests to minimize unnecessary computations.

2. PROBLEM SOLVED:
   - Duplicate Requests: Semantic Caching avoids re-generating answers for 
     similar user questions.
   - High Latency/Cost: Prompt Compression reduces the token count.
   - Resource Overkill: Tiered Routing prevents using a 70B model for a 
     "Hello" or simple classification task.

3. BUSINESS VALUE:
   - Burn Rate Reduction: Drastically lowers the monthly cloud/API bill.
   - Faster Response: Cached results return in milliseconds (not seconds).

4. IMPLEMENTATION:
   - Semantic Cache logic.
   - Model Router based on query complexity.
   - Conceptual Prompt Compression.
================================================================================
"""

import numpy as np
from sentence_transformers import SentenceTransformer, util

class AICostGateway:
    def __init__(self):
        # Model for semantic similarity
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')

        # Simple Semantic Cache: {embedding: response}
        self.cache = [] # List of tuples (embedding, response)
        self.cache_threshold = 0.92 # Similarity threshold

    def compress_prompt(self, prompt: str) -> str:
        """
        Removes redundant words/filler text to save tokens.
        In production, we use LLMLingua or similar techniques.
        """
        # Conceptual: Removing common fillers
        fillers = ["please", "could you", "I would like to know", "thank you"]
        compressed = prompt
        for word in fillers:
            compressed = compressed.replace(word, "")
        return compressed.strip()

    def route_request(self, query: str) -> str:
        """
        TIERED ROUTING:
        Decides which model should handle the query based on complexity.
        """
        words_count = len(query.split())

        # Logic: Simple queries go to a small/cheap model
        if words_count < 5 or "hello" in query.lower():
            return "Small-Model (e.g., Llama-3-8B / GPT-4o-mini)"

        # Complex reasoning tasks go to a large model
        return "Large-Model (e.g., Llama-3-70B / GPT-4o)"

    def get_response(self, user_query: str):
        # 1. Prompt Compression
        clean_query = self.compress_prompt(user_query)
        query_embedding = self.embedder.encode(clean_query)

        # 2. Semantic Caching Check
        for cached_embedding, cached_response in self.cache:
            similarity = util.cos_sim(query_embedding, cached_embedding)
            if similarity > self.cache_threshold:
                print("⚡ [Cache Hit] Returning cached response...")
                return cached_response

        # 3. Routing & LLM Call (Simulation)
        target_model = self.route_request(clean_query)
        print(f"📡 [Routing] Sending request to: {target_model}")

        # Simulated LLM Response
        final_response = f"Simulated response from {target_model} for: {clean_query}"

        # 4. Update Cache

        self.cache.append((query_embedding, final_response))
        return final_response

# --- Simulation ---

if name == "__main__":
    gateway = AICostGateway()

    print("--- Request 1 ---")
    print(gateway.get_response("Could you please tell me how much I can borrow?"))

    print("\n--- Request 2 (Similar Query) ---")
    # This should trigger a Semantic Cache Hit
    print(gateway.get_response("how much can I borrow?"))

    print("\n--- Request 3 (Simple Query) ---")
    # This should trigger the Small Model
    print(gateway.get_response("Hello!"))