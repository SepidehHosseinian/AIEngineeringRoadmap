import logging
from datetime import datetime
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename=f"rag_logs_{datetime.now().strftime('%Y%m%d')}.log"
)
logger = logging.getLogger(__name__)

class EnterpriseRAGSystem:
    def __init__(self, vector_db_path="faiss_index"):
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.vector_db_path = vector_db_path
        
        
        self.prompt_template = """
        Use the following pieces of context to answer the question at the end. 
        If you don't know the answer, just say that you don't know, don't try to make up an answer.
        Always cite the source if available.

        Context: {context}
        Question: {question}

        Helpful Answer in Persian:"""
        
    def load_brain(self):
        logger.info("Loading Vector Database and LLM...")
        vector_store = FAISS.load_local(
            self.vector_db_path, 
            self.embeddings, 
            allow_dangerous_deserialization=True
        )
        
        prompt = PromptTemplate(
            template=self.prompt_template, 
            input_variables=["context", "question"]
        )

        
        return RetrievalQA.from_chain_type(
            llm=ChatOpenAI(model_name="gpt-4o", temperature=0),
            chain_type="stuff",
            retriever=vector_store.as_retriever(search_kwargs={"k": 2}),
            return_source_documents=True,
            chain_type_kwargs={"prompt": prompt}
        )

    def ask(self, query):
        logger.info(f"User Query: {query}")
        rag_chain = self.load_brain()
        
        
        response = rag_chain.invoke({"query": query})
        
        answer = response["result"]
        sources = [doc.page_content for doc in response["source_documents"]]
        
        logger.info("Response generated successfully.")
        return answer, sources

if __name__ == "__main__":
    
    rag_sys = EnterpriseRAGSystem()
    
    user_question = "سقف انتقال وجه داخلی چقدر است؟"
    answer, ref_sources = rag_sys.ask(user_question)
    
    print(f"\n🤖 پاسخ سیستم:\n{answer}")
    print(f"\n📚 منابع استخراج شده:\n{ref_sources}")