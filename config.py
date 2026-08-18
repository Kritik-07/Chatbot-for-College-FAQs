class Config:
    """Simple application configuration."""

    VECTOR_STORE_PATH = "./chroma_db"
    FAQ_JSON_PATH = "./faqs.json"

    # Hugging Face embedding model
    EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

    # Local LLM through Ollama
    OLLAMA_MODEL = "phi3:mini"

    # Number of FAQ documents retrieved for each question
    RETRIEVER_K = 3