import json
import shutil
from pathlib import Path

from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

from config import Config


def create_vector_database():
    """Create the Chroma vector database from faqs.json.

    Each FAQ remains one complete Document:
    Question + Answer + Category.
    No text chunking is applied to the FAQ pairs.
    """
    faq_path = Path(Config.FAQ_JSON_PATH)

    if not faq_path.exists():
        raise FileNotFoundError(f"FAQ file not found: {faq_path}")

    with faq_path.open("r", encoding="utf-8") as file:
        faqs = json.load(file)

    if not isinstance(faqs, list) or not faqs:
        raise ValueError("faqs.json must contain a non-empty JSON list.")

    documents = []

    for item in faqs:
        required = ("id", "category", "question", "answer")
        missing = [key for key in required if key not in item]

        if missing:
            raise ValueError(
                f"FAQ item {item.get('id', 'unknown')} is missing: {missing}"
            )

        content = (
            f"Category: {item['category']}\n"
            f"Question: {item['question']}\n"
            f"Answer: {item['answer']}"
        )

        documents.append(
            Document(
                page_content=content,
                metadata={
                    "faq_id": str(item["id"]),
                    "category": item["category"],
                    "question": item["question"],
                },
            )
        )

    # Remove the old database so a rebuild never leaves stale documents.
    vector_path = Path(Config.VECTOR_STORE_PATH)
    if vector_path.exists():
        shutil.rmtree(vector_path)

    embeddings = HuggingFaceEmbeddings(
        model_name=Config.EMBEDDING_MODEL
    )

    Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=Config.VECTOR_STORE_PATH,
        collection_name="college_faq",
    )

    print(f"Created vector database with {len(documents)} FAQ documents.")
    print(f"Location: {Config.VECTOR_STORE_PATH}")


if __name__ == "__main__":
    create_vector_database()