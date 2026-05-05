import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

load_dotenv()

class SemanticCache:
    def __init__(self, threshold=0.9):
        self.embeddings = OpenAIEmbeddings()
        self.threshold = threshold
        self.cache = None
        # In a real app, you'd load/save this from a local file
        self.cache_file = "semantic_cache_db"

    def get_cached_answer(self, user_query):
        if self.cache is None:
            return None
        
        # Search for the most similar query in the cache
        results = self.cache.similarity_search_with_relevance_scores(user_query, k=1)
        
        if results and results[0][1] >= self.threshold:
            print(f"--- Cache Hit (Score: {results[0][1]:.2f}) ---")
            return results[0][0].metadata['answer']
        
        return None

    def update_cache(self, user_query, llm_answer):
        new_doc = Document(
            page_content=user_query, 
            metadata={"answer": llm_answer}
        )
        
        if self.cache is None:
            self.cache = FAISS.from_documents([new_doc], self.embeddings)
        else:
            self.cache.add_documents([new_doc])
        
        print("--- Cache Updated ---")

# Simple Test
if __name__ == "__main__":
    my_cache = SemanticCache(threshold=0.85)

    # First time: No cache
    q1 = "How do I save energy with solar panels?"
    ans1 = "You can use battery storage systems to save excess energy."
    
    if not my_cache.get_cached_answer(q1):
        my_cache.update_cache(q1, ans1)

    # Second time: Semantic similarity (different wording)
    q2 = "Ways to store solar power for later use?"
    cached_res = my_cache.get_cached_answer(q2)
    
    if cached_res:
        print(f"Query: {q2}\nCached Answer: {cached_res}")
    else:
        print("Cache Miss - Calling LLM...")