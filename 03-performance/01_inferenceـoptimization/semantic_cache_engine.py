"""
================================================================================
TECHNICAL DECISION: Semantic Caching for Cost & Latency Optimization
================================================================================

1. CONTEXT:
   In production, many users ask similar questions (e.g., "How to reset my 
   password?" vs "I forgot my password"). Standard caches miss these because 
   the strings aren't identical.

2. PROBLEM SOLVED:
   - High API Costs: Reduces redundant calls to expensive models (GPT-4/Claude).
   - High Latency: Returns answers in <50ms instead of waiting seconds for an LLM.
   - Rate Limiting: Saves API quota for unique, complex queries.

3. BUSINESS VALUE (The "Lead" Perspective):
   - Cost Reduction: Can reduce LLM spend by 30-60% depending on query redundancy.
   - Scalability: Handles peak traffic by serving common queries from a fast vector DB.

4. IMPLEMENTATION:
   - Uses Vector Similarity (Cosine Similarity) to find "semantically close" 
     queries in the cache.
================================================================================
"""

import numpy as np
from typing import Optional, Tuple
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

class SemanticCache:
    def init__(self, threshold: float = 0.90):
        # Using a lightweight model for fast embedding generation
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
        self.cache_data = []  # In production, use Redis with Vector Search
        self.cache_embeddings = []
        self.threshold = threshold

    def get_from_cache(self, query: str) -> Optional[str]:
        """Checks if a semantically similar query exists in the cache."""
        if not self.cache_data:
            return None

        query_embedding = self.encoder.encode([query])

        # Calculate similarity with all cached queries
        similarities = cosine_similarity(query_embedding, self.cache_embeddings)[0]
        max_idx = np.argmax(similarities)

        if similarities[max_idx] >= self.threshold:
            print(f"✨ [CACHE HIT] Similarity: {similarities[max_idx]:.4f}")
            return self.cache_data[max_idx]["answer"]

        return None

    def add_to_cache(self, query: str, answer: str):
        """Stores a new query and its embedding in the cache."""
        embedding = self.encoder.encode([query])
        self.cache_data.append({"query": query, "answer": answer})
        if len(self.cache_embeddings) == 0:
            self.cache_embeddings = embedding
        else:
            self.cache_embeddings = np.vstack([self.cache_embeddings, embedding])
        print(f"💾 [CACHE STORE] Query added to semantic cache.")

# --- Demo Scenario ---

if __name == "__main__":
    cache_sys = SemanticCache(threshold=0.85)

    # First time: LLM is called (Simulated)

    q1 = "How can I increase my credit limit at AzkiVam?"
    a1 = "To increase your limit, upload your latest 3-month bank statement in the app."
    cache_sys.add_to_cache(q1, a1)

    # Second time: Similar query (Different wording)
    q2 = "Tell me the process for a higher loan limit"

    cached_answer = cache_sys.get_from_cache(q2)
    if cached_answer:
        print(f"Result: {cached_answer}")
    else:
        print("Calling LLM...") # This won't happen in this case!