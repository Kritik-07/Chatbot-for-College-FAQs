


from typing import List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from rag_chain import RAGChain


app = FastAPI(
    title="College FAQ Chatbot API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# One RAG instance shared by API requests.
rag_chain = RAGChain()


class ChatRequest(BaseModel):
    message: str
    chat_history: Optional[List[dict]] = None


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/api/chat")
def chat(request: ChatRequest):
    """Answer a college FAQ question using the RAG pipeline."""
    if not request.message.strip():
        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty.",
        )

    try:
        result = rag_chain.get_response(
            request.message,
            chat_history=request.chat_history or [],
        )

        return {
            "status": "success",
            "response": result["answer"],
            "sources": result["sources"],
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc