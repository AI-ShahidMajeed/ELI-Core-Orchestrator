import logging
from typing import List, Dict, Any

class RAGOrchestrator:
    """
    Core orchestrator for ELI-Core. 
    Handles the retrieval of context and generation of responses.
    """
    def __init__(self, vector_store: Any, llm_adapter: Any):
        self.vector_store = vector_store
        self.llm_adapter = llm_adapter
        self.logger = logging.getLogger(__name__)

    async def query(self, user_query: str, top_k: int = 5) -> Dict[str, Any]:
        """
        Processes a user query by retrieving relevant context and generating a response.
        """
        self.logger.info(f"Processing query: {user_query}")
        
        # 1. Retrieval Phase
        try:
            context_docs = await self.vector_store.similarity_search(user_query, k=top_k)
            context_text = "\n".join([doc.page_content for doc in context_docs])
        except Exception as e:
            self.logger.error(f"Error during retrieval: {str(e)}")
            context_text = ""

        # 2. Generation Phase
        prompt = self._build_prompt(user_query, context_text)
        try:
            response = await self.llm_adapter.generate(prompt)
        except Exception as e:
            self.logger.error(f"Error during generation: {str(e)}")
            response = "I'm sorry, I encountered an error while generating a response."

        return {
            "query": user_query,
            "response": response,
            "sources": [doc.metadata for doc in context_docs] if context_docs else []
        }

    def _build_prompt(self, query: str, context: str) -> str:
        """
        Constructs the final prompt for the LLM.
        """
        return f"""
        You are ELI, an enterprise-grade AI assistant. Use the provided context to answer the user query accurately.
        
        Context:
        {context}
        
        User Query: {query}
        
        Answer:
        """
