import os
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings # For Local Embeddings
from langchain_core.documents import Document

class LocalKnowledgeManager:
    """
    Manages a local vector database to ensure the AI has access 
    to business data even during network disruptions.
    """
    def __init__(self, use_local_embeddings=True):
        # If internet is down, we use a local model for embeddings
        if use_local_embeddings:
            print("💾 Loading local embedding model (Sentence-Transformers)...")
            self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        else:
            self.embeddings = OpenAIEmbeddings()
        
        self.vector_db_path = "faiss_index"

    def create_index(self, data_list):
        """Converts text data into vectors and saves them locally."""
        documents = [Document(page_content=text) for text in data_list]
        vector_store = FAISS.from_documents(documents, self.embeddings)
        vector_store.save_local(self.vector_db_path)
        print(f"✅ Knowledge base saved to {self.vector_db_path}")

    def query(self, user_query, k=2):
        """Searches the local database for the most relevant information."""
        if not os.path.exists(self.vector_db_path):
            return "No local knowledge base found."
        
        vector_store = FAISS.load_local(
            self.vector_db_path, 
            self.embeddings, 
            allow_dangerous_deserialization=True
        )
        results = vector_store.similarity_search(user_query, k=k)
        return [res.page_content for res in results]

if __name__ == "__main__":
    # Simulate business data (e.g., Bank protocols or Insurance rules)
    company_data = [
        "Protocol A: In case of network failure, all transactions must be cached locally.",
        "Protocol B: User authentication requires a valid internal token in the header.",
        "Protocol C: The maximum daily transfer limit for internal users is 500 million Rials."
    ]

    manager = LocalKnowledgeManager(use_local_embeddings=True)
    
    # 1. Build the local memory
    manager.create_index(company_data)
    
    # 2. Query it (Simulating an agent looking for answers)
    query = "What is the limit for internal transfers?"
    context = manager.query(query)
    
    print(f"\n🔍 Query: {query}")
    print(f"📄 Relevant Context found in Local DB:\n{context}")