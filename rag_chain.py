from typing import Any, List, Optional

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.llms import Ollama
from langchain_core.messages import AIMessage, HumanMessage, BaseMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from config import Config


class RAGChain:
    """Small, direct RAG pipeline for the college FAQ chatbot."""

    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()

        embeddings = HuggingFaceEmbeddings(
            model_name=self.config.EMBEDDING_MODEL
        )

        self.vector_store = Chroma(
            collection_name="college_faq",
            persist_directory=self.config.VECTOR_STORE_PATH,
            embedding_function=embeddings,
        )

        self.retriever = self.vector_store.as_retriever(
            search_kwargs={"k": self.config.RETRIEVER_K}
        )

        self.llm = Ollama(model=self.config.OLLAMA_MODEL)

        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """You are a college FAQ assistant.

Answer ONLY from the provided college FAQ context.

Rules:
1. Do not invent or guess facts.
2. If the context does not contain the answer, say:
   "I don't have information about that in the college FAQ."
3. Keep answers concise and clear.
4. If the user asks multiple questions, answer each part separately.
5. Use conversation history only to understand follow-up questions.
6. Do not use outside knowledge.

College FAQ context:
{context}""",
                ),
                MessagesPlaceholder("chat_history"),
                ("human", "{question}"),
            ]
        )

        self.chain = self.prompt | self.llm | StrOutputParser()

    @staticmethod
    def _format_history(chat_history: Optional[List[Any]]) -> List[BaseMessage]:
        """Convert simple dictionaries or LangChain messages to LangChain messages."""
        if not chat_history:
            return []

        formatted = []

        for message in chat_history:
            if isinstance(message, BaseMessage):
                formatted.append(message)
                continue

            if isinstance(message, dict):
                role = message.get("role")
                content = message.get("content", "")

                if role == "user":
                    formatted.append(HumanMessage(content=content))
                elif role in ("assistant", "ai"):
                    formatted.append(AIMessage(content=content))

        return formatted

    def retrieve(self, question: str):
        """Retrieve FAQ documents for a question."""
        return self.retriever.invoke(question)

    def get_response(
        self,
        user_input: str,
        chat_history: Optional[List[Any]] = None,
    ) -> dict:
        """Return the answer and the retrieved FAQ sources."""
        if not user_input or not user_input.strip():
            return {
                "answer": "Please enter a question.",
                "sources": [],
            }

        history = self._format_history(chat_history)
        documents = self.retrieve(user_input)

        context = "\n\n---\n\n".join(
            document.page_content for document in documents
        )

        answer = self.chain.invoke(
            {
                "context": context,
                "chat_history": history,
                "question": user_input,
            }
        )

        sources = [
            {
                "faq_id": document.metadata.get("faq_id"),
                "category": document.metadata.get("category"),
                "question": document.metadata.get("question"),
            }
            for document in documents
        ]

        return {
            "answer": answer.strip(),
            "sources": sources,
        }