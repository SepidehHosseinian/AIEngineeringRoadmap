import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.storage import InMemoryStore
from langchain.retrievers import ParentDocumentRetriever
from langchain_community.document_loaders import PyPDFLoader

load_dotenv()

class EnterpriseIngestion:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings()
        # Child splitter: Small chunks for high-granularity search
        self.child_splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=50)
        # Parent splitter: Larger chunks to provide meaningful context to the LLM
        self.parent_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=200)
        
        # In-memory storage for the parent documents
        self.store = InMemoryStore()
        # FAISS vector store for the child document embeddings
        self.vectorstore = None

    def process_document(self, file_path):
        """
        Loads a PDF and indexes it using the Parent-Document strategy.
        This ensures we find the needle (child) but return the haystack (parent).
        """
        print(f"--- Starting ingestion for: {file_path} ---")
        loader = PyPDFLoader(file_path)
        documents = loader.load()

        # Initialize FAISS with a dummy doc if it's the first time
        if self.vectorstore is None:
            # We initialize the retriever structure
            from langchain_community.vectorstores import FAISS
            # Create an empty vectorstore
            self.vectorstore = FAISS.from_texts(["initialization"], self.embeddings)

        retriever = ParentDocumentRetriever(
            vectorstore=self.vectorstore,
            docstore=self.store,
            child_splitter=self.child_splitter,
            parent_splitter=self.parent_splitter,
        )

        retriever.add_documents(documents, ids=None)
        print("--- Ingestion completed successfully ---")
        return retriever

if __name__ == "__main__":
    # Example usage (Ensure you have a sample.pdf in the directory)
    ingestor = EnterpriseIngestion()
    # Path to a sample document
    # doc_path = "path/to/your/document.pdf"
    # retriever = ingestor.process_document(doc_path)
    print("Ingestion logic ready. Please provide a PDF path to test.")