import os
from dotenv import load_dotenv
from flashrank import Ranker, RerankRequest
from langchain.schema import Document

load_dotenv()

class EnterpriseReranker:
    def __init__(self, model_name: str = "ms-marco-TinyBERT-L-2-v2"):
        """
        Initializes the FlashRank reranker. 
        This is a lightweight but powerful cross-encoder.
        """
        print(f"--- Loading Reranker Model: {model_name} ---")
        self.ranker = Ranker(model_name=model_name, cache_dir="/tmp/")

    def rerank(self, query: str, documents: list[Document], top_n: int = 3):
        """
        Reranks a list of documents based on the query.
        Returns only the top_n most relevant documents.
        """
        if not documents:
            return []

        print(f"--- Reranking {len(documents)} documents for query: '{query}' ---")
        
        # Prepare documents for FlashRank format
        passages = [
            {"id": i, "text": doc.page_content, "meta": doc.metadata}
            for i, doc in enumerate(documents)
        ]

        rerank_request = RerankRequest(query=query, passages=passages)
        results = self.ranker.rerank(rerank_request)

        # Convert back to LangChain Document format
        reranked_docs = []
        for res in results[:top_n]:
            reranked_docs.append(
                Document(page_content=res["text"], metadata=res["meta"])
            )
            
        print(f"--- Reranking complete. Top score: {results[0]['score']:.4f} ---")
        return reranked_docs

if __name__ == "__main__":
    # Test Data: Imagine these were returned by the Hybrid Search
    query = "How to reset bank password?"
    mock_results = [
        Document(page_content="To change your profile picture, go to settings.", metadata={"id": 1}),
        Document(page_content="To reset your banking password, click 'Forgot Password' on the login page.", metadata={"id": 2}),
        Document(page_content="Password policies require 8 characters.", metadata={"id": 3}),
    ]

    reranker = EnterpriseReranker()
    top_docs = reranker.rerank(query, mock_results)

    print("\nFinal Top Results after Reranking:")
    for i, doc in enumerate(top_docs):
        print(f"{i+1}. {doc.page_content}")
