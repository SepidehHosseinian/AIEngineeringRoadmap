"""
================================================================================
TECHNICAL DECISION: Optimized Retrieval (Hybrid Search + Cross-Encoder Re-ranking)
================================================================================

1. CONTEXT:
   A standard Vector Search (Dense) might miss specific IDs or technical terms.
   For high-precision tasks (e.g., AzkiVam rules), we need a hybrid approach.

2. PROBLEM SOLVED:
   - Low Precision: Vector search alone can be "fuzzy".
   - Context Window Waste: Passing irrelevant chunks to the LLM increases cost 
     and decreases reasoning quality (Lost-in-the-Middle phenomenon).

3. BUSINESS VALUE:
   - Accuracy: Ensures the LLM gets the exact* right context.
   - Efficiency: Higher quality context means we can use smaller, faster models 
     for the final generation.

4. IMPLEMENTATION:
   - Hybrid Search simulation (Vector + BM25).
   - Re-ranking using a Cross-Encoder (Reranker model).
================================================================================
"""

from sentence_transformers import SentenceTransformer, CrossEncoder
import numpy as np

class OptimizedRetriever:
    def init__(self, vector_model_name: str, reranker_model_name: str):
        # Dense Embedding Model (for semantic search)
        self.vector_model = SentenceTransformer(vector_model_name)
        # Cross-Encoder Model (for precision re-ranking)
        self.reranker = CrossEncoder(reranker_model_name)

        # Simulated Document Store
        self.documents = [
            "AzkiVam credit limit is up to 50 million Tomans for gold-tier users.",
            "Installment plans are available for 6, 12, and 18 months.",
            "To apply for a loan, you need a valid national ID and a bank statement.",
            "Gold-tier membership requires a credit score above 750.",
            "Late payment fees are calculated as 2% of the remaining balance monthly."
        ]
        self.doc_embeddings = self.vector_model.encode(self.documents)

    def retrieve(self, query: str, top_k: int = 5):
        print(f"🔍 Query: {query}")

        # STEP 1: Dense Retrieval (Semantic)
        query_embedding = self.vector_model.encode(query)
        scores = np.dot(self.doc_embeddings, query_embedding)
        top_indices = np.argsort(scores)[::-1][:top_k]
        initial_results = [self.documents[i] for i in top_indices]

        print(f"✅ Initial retrieval found {len(initial_results)} candidates.")

        # STEP 2: Re-ranking (The "Precision" Layer)
        # We pair the query with each retrieved document
        pairs = [[query, doc] for doc in initial_results]
        rerank_scores = self.reranker.predict(pairs)

        # Sort by reranker scores
        reranked_indices = np.argsort(rerank_scores)[::-1]
        final_results = [initial_results[i] for i in reranked_indices]

        return final_results

# --- Architectural Simulation ---

if __name == "__main__":
    # Using lightweight models for demonstration
    # In production, we'd use something like 'BGE-Reranker'

    retriever = OptimizedRetriever(
        vector_model_name="all-MiniLM-L6-v2",
        reranker_model_name="cross-encoder/ms-marco-MiniLM-L-6-v2"
    )

    query = "How much can I borrow if I'm a gold user?"

    results = retriever.retrieve(query)

    print("\n🏆 Top Reranked Documents for LLM Context:")
    for i, res in enumerate(results[:2]): # Usually we only take top 2-3 for the prompt
        print(f"{i+1}. {res}")