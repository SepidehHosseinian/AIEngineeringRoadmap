import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever
from langchain.schema import Document

load_dotenv()

class EnterpriseHybridRetriever:
    def __init__(self, documents: list):
        """
        Initializes a Hybrid Retriever combining Vector Search (FAISS) 
        and Keyword Search (BM25).
        """
        self.embeddings = OpenAIEmbeddings()
        self.documents = documents
        
        # 1. Setup Keyword Retriever (BM25) - Excellent for exact matches
        print("--- Initializing BM25 Retriever ---")
        self.bm25_retriever = BM25Retriever.from_documents(documents)
        self.bm25_retriever.k = 3  # Top 3 results from keyword search

        # 2. Setup Vector Retriever (FAISS) - Excellent for semantic meaning
        print("--- Initializing FAISS Retriever ---")
        self.vectorstore = FAISS.from_documents(documents, self.embeddings)
        self.vector_retriever = self.vectorstore.as_retriever(search_kwargs={"k": 3})

        # 3. Create the Ensemble (Hybrid) Retriever
        # We give weights to each retriever. 
        # Usually, a 50/50 or 70/30 split works best depending on the data.
        self.ensemble_retriever = EnsembleRetriever(
            retrievers=[self.bm25_retriever, self.vector_retriever],
            weights=[0.4, 0.6]  # 40% Keyword, 60% Semantic
        )

    def retrieve(self, query: str):
        print(f"--- Executing Hybrid Search for: '{query}' ---")
        results = self.ensemble_retriever.get_relevant_documents(query)
        return results

if __name__ == "__main__":
    # Mock data for demonstration
    mock_docs = [
        Document(page_content="The bank's SWIFT code is BNK-TEH-2024.", metadata={"source": "manual"}),
        Document(page_content="Customer support is available 24/7 for premium members.", metadata={"source": "faq"}),
        Document(page_content="Our AI strategy focuses on scalability and security.", metadata={"source": "strategy_doc"})
    ]
    
    hybrid_system = EnterpriseHybridRetriever(mock_docs)
    
    # Test case 1: Exact match (Keyword)
    print("\nTest 1 (Exact Match):")
    res1 = hybrid_system.retrieve("What is the SWIFT code?")
    for doc in res1:
        print(f"- {doc.page_content}")

    # Test case 2: Semantic match
    print("\nTest 2 (Semantic):")
    res2 = hybrid_system.retrieve("How can I get help at night?")
    for doc in res2:
        print(f"- {doc.page_content}")