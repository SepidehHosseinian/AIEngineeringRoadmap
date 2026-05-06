import os
from dotenv import load_dotenv
from 01_ingestion_pipeline import EnterpriseIngestion
from 02_hybrid_retriever import EnterpriseHybridRetriever
from 03_reranker_logic import EnterpriseReranker
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

load_dotenv()

class RAGOrchestrator:
    def __init__(self, pdf_path=None):
        print("--- Initializing Enterprise RAG System ---")
        self.ingestor = EnterpriseIngestion()
        self.reranker = EnterpriseReranker()
        self.llm = ChatOpenAI(model_name="gpt-4-turbo", temperature=0)
        
        self.retriever = None
        if pdf_path:
            self.setup_system(pdf_path)

    def setup_system(self, pdf_path):
        """Step 1 & 2: Ingest and setup Hybrid Retriever"""
        # Ingest documents using Parent-Document strategy
        parent_retriever = self.ingestor.process_document(pdf_path)
        
        # In an Enterprise setup, we'd pull all docs for the Hybrid search
        # For this orchestrator, we use the vectorstore created during ingestion
        all_docs = self.ingestor.store.mget(self.ingestor.store.yield_keys())
        self.hybrid_retriever = EnterpriseHybridRetriever(all_docs)

    def ask(self, query: str):
        """The full RAG Pipeline: Search -> Hybrid -> Rerank -> Generation"""
        
        # 1. Hybrid Retrieval
        initial_docs = self.hybrid_retriever.retrieve(query)
        
        # 2. Reranking (The Precision Layer)
        final_context_docs = self.reranker.rerank(query, initial_docs, top_n=3)
        
        # 3. Augmentation & Generation
        context_text = "\n\n".join([doc.page_content for doc in final_context_docs])
        
        prompt_template = f"""
        You are a professional AI Assistant for an Enterprise Organization.
        Use the following pieces of context to answer the user's question accurately.
        If you don't know the answer based on the context, say you don't know. 
        Do not make up information.

        CONTEXT:
        {context_text}

        USER QUESTION: {query}
        
        PROFESSIONAL ANSWER:"""

        response = self.llm.invoke(prompt_template)
        return response.content

if __name__ == "__main__":
    # Example usage:
    # orchestrator = RAGOrchestrator("company_policy.pdf")
    # answer = orchestrator.ask("What is the policy for remote work?")
    # print(answer)
    print("Orchestrator is ready to handle complex queries.")