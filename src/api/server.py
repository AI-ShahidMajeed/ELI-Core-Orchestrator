from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import uvicorn

app = FastAPI(title="ELI-Core: Enterprise RAG API")

class QueryRequest(BaseModel):
    query: str
    top_k: int = 5

class QueryResponse(BaseModel):
    response: str
    sources: List[Dict[str, Any]]

@app.get("/health")
async def health_check():
    """
    Endpoint for monitoring system health.
    """
    return {"status": "healthy", "service": "ELI-Core-Orchestrator"}

@app.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """
    Processes a user query by retrieving relevant context and generating a response.
    """
    if not request.query:
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    
    # Placeholder for RAGOrchestrator logic
    # In a real scenario, we'd invoke the orchestrator instance
    return QueryResponse(
        response=f"Answer to '{request.query}' based on context.",
        sources=[{"id": 1, "source": "example_doc.pdf"}]
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
