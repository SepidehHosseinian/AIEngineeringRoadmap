import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
# Importing from our previous module
# from enterprise_rag import EnterpriseRAGSystem 

app = FastAPI(
    title="Enterprise AI Agent API",
    description="Production-ready API for RAG and Document Intelligence",
    version="1.0.0"
)

# Define request schema for strict validation
class QueryRequest(BaseModel):
    question: str
    user_id: Optional[str] = "anon_user"

# Define response schema for consistency
class QueryResponse(BaseModel):
    answer: str
    sources: List[str]
    status: str

@app.get("/health")
async def health_check():
    """Endpoint for monitoring systems (K8s/Docker) to verify service health."""
    return {"status": "healthy", "timestamp": "2026-05-07"}

@app.post("/ask", response_model=QueryResponse)
async def ask_agent(request: QueryRequest):
    """
    Main endpoint to interact with the RAG system.
    Handles user questions and returns validated responses.
    """
    try:
        # Business Logic: In a real scenario, we initialize the RAG class here
        # For now, we simulate the logic to keep the example runnable
        
        if not request.question:
            raise HTTPException(status_code=400, detail="Question cannot be empty")

        # Mocking the RAG response based on our 05-production-ready-rag logic
        # In production: answer, sources = rag_sys.ask(request.question)
        simulated_answer = "Internal transfer limit is 500 million Rials for verified users."
        simulated_sources = ["Protocol C: Internal User Daily Limits"]

        return QueryResponse(
            answer=simulated_answer,
            sources=simulated_sources,
            status="success"
        )

    except Exception as e:
        # Proper error handling to prevent leaking system details
        raise HTTPException(status_code=500, detail="Internal AI Engine Error")

if __name__ == "__main__":
    # Standard entry point for launching the API service
    uvicorn.run(app, host="0.0.0.0", port=8000)
