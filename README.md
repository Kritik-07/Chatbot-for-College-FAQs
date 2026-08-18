# 🎓 College FAQ Chatbot (Multi-Turn RAG Pipeline)

A robust, production-ready Retrieval-Augmented Generation (RAG) system built with **LangChain**, **ChromaDB**, **Ollama (`phi3:mini`)**, and **SQLite**.

This system acts as an intelligent college assistant capable of resolving multi-part questions, remembering conversation history across sessions, and providing accurate context-bounded answers from institutional document knowledge bases.

---

## 📌 Architecture & Features

```
User Query ──► [Query Decomposition & History Rewriter] ──► Sub-Queries
                                                               │
                                                               ▼
LLM Response ◄── [QA Generation] ◄── [Deduplication] ◄── [Vector Search (ChromaDB)]
```

- **Multi-Question Decomposition:** Automatically detects and splits complex queries containing multiple questions (e.g., _"Who is the HOD of AI & ML and what are the B.E. fees?"_) into individual sub-queries using JSON array output.
- **Contextual Memory Rewriting:** Re-writes follow-up queries containing implicit pronouns or context dependencies (e.g., _"What is her email?"_ $\rightarrow$ _"What is Dr. Asha S. Manek's email?"_) based on chat history.
- **Persistent Session Memory:** Uses **SQLite** (`SQLChatMessageHistory`) to store and retrieve multi-turn chat records per user `session_id`, ensuring zero context loss across app restarts.
- **Strict Context Bounding:** Prompt engineering ensures the LLM responds **ONLY** using retrieved context chunks from `faqs.json`, preventing hallucinations or external knowledge leakage.
- **Local & Privacy-Preserving:** Fully runnable locally without third-party API keys using local vector databases and Ollama model serving.

---

## 📁 Repository Structure

```
college_faqs/
├── college_faq_rag.ipynb  # Comprehensive Jupyter Notebook containing full pipeline
├── faqs.json             # Source JSON dataset containing college Q&A pairs/chunks
├── .gitignore            # Excludes heavy local vector indices and SQLite databases
└── README.md             # Project documentation and pipeline specifications
```

---

## 🚀 Setup & Installation

### 1. Prerequisites

- **Python 3.10+**
- **Ollama** installed and running locally ([ollama.ai](https://ollama.ai))

### 2. Download LLM Model

Ensure the `phi3:mini` model is available locally:

```bash
ollama run phi3:mini
```

### 3. Install Python Dependencies

```bash
pip install langchain langchain-community langchain-core chromadb pydantic
```

---

## ⚙️ Core Pipeline Implementation

### Pipeline Flow Explanation for Developers / LLM Context

1. **Vector Store Initialization:** Source data (`faqs.json`) is embedded and stored in **ChromaDB**. The retriever retrieves top $k=2$ matching chunks per question.
2. **Decomposition & History Integration (`process_and_retrieve_docs`):**
   - Combines user query and `chat_history`.
   - Prompts the LLM to return a raw JSON array of rephrased standalone sub-questions.
   - Executes vector store retrieval for **each** sub-question individually.
   - Merges and deduplicates retrieved context snippets.
3. **Question Answering Chain (`rag_chain`):**
   - Passes aggregated contexts and full `chat_history` into the final QA prompt.
   - Generates bulleted/structured answers using `phi3:mini`.
4. **Session History Manager (`get_chat_response`):**
   - Reads/writes past `HumanMessage` and `AIMessage` objects to a local SQLite database (`sqlite:///chat_history.db`) keyed by `session_id`.

---

## 🐍 Python Source Code Summary

```python
import json
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_community.llms import Ollama
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# 1. Initialize LLM & Retriever
llm = Ollama(model="phi3:mini")
# Assume vector_store is initialized from faqs.json via ChromaDB
retriever = vector_store.as_retriever(search_kwargs={"k": 2})

# 2. Query Decomposition & Re-writer Prompt
decompose_system_prompt = """You are a query analyzer for a college chatbot.
Analyze the user's input alongside the chat history.
If the user asks multiple questions, split them into standalone questions.
If the question relies on context (e.g. "what is her email?"), rewrite it using the chat history to be standalone.

Output ONLY a JSON array of strings containing the individual questions. No explanations or extra text."""

decompose_prompt = ChatPromptTemplate.from_messages([
    ("system", decompose_system_prompt),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
])

decompose_chain = decompose_prompt | llm | StrOutputParser()

# 3. Context Processing & Deduplication Helper
def process_and_retrieve_docs(input_dict):
    raw_user_input = input_dict["input"]
    chat_history = input_dict.get("chat_history", [])

    try:
        decomposition_output = decompose_chain.invoke({"input": raw_user_input, "chat_history": chat_history})
        questions = json.loads(decomposition_output.strip())
        if not isinstance(questions, list):
            questions = [raw_user_input]
    except Exception:
        questions = [raw_user_input]

    all_docs = []
    seen_contents = set()

    for q in questions:
        docs = retriever.invoke(q)
        for doc in docs:
            if doc.page_content not in seen_contents:
                seen_contents.add(doc.page_content)
                all_docs.append(doc)

    return "\n\n".join(doc.page_content for doc in all_docs)

# 4. Answer Generation Prompt & LCEL Chain
qa_system_prompt = """You are a helpful College FAQ Chatbot.
Answer ALL parts of the user's query clearly using ONLY the provided context below.
Address each asked question distinctly using bullet points or concise paragraphs.
If the context doesn't contain information for a specific sub-question, explicitly state that you don't have information on that part.

Context:
{context}"""

qa_prompt = ChatPromptTemplate.from_messages([
    ("system", qa_system_prompt),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
])

rag_chain = (
    RunnablePassthrough.assign(context=process_and_retrieve_docs)
    | qa_prompt
    | llm
    | StrOutputParser()
)

# 5. Entry Point Function for Backend/Frontend APIs
def get_chat_response(session_id: str, user_message: str) -> str:
    history = SQLChatMessageHistory(
        session_id=session_id,
        connection_string="sqlite:///chat_history.db"
    )

    response = rag_chain.invoke({
        "input": user_message,
        "chat_history": history.messages
    })

    history.add_user_message(user_message)
    history.add_ai_message(response)

    return response
```

---

## 🧪 Verification & Test Examples

### Case 1: Multi-Question Handling

- **User Input:** _"Who is the HOD of AI and ML department, and what is the fee for B.E. Computer Science?"_
- **Decomposition Output:** `["Who is the HOD of AI and Machine Learning department?", "What is the fee for B.E. Computer Science?"]`
- **Bot Output:**
  > - **HOD of AI & ML:** Dr. Asha S. Manek.
  > - **B.E. Computer Science Fee:** ₹1,25,000 per annum.

### Case 2: Multi-Turn History Resolution

- **Turn 1 (User):** _"Who is the HOD of AI and Machine Learning?"_
- **Turn 1 (Bot):** _"Dr. Asha S. Manek is the Head of Department for AI & ML."_
- **Turn 2 (User):** _"What is her qualification?"_
- **Re-written Query:** _"What is the qualification of Dr. Asha S. Manek?"_
- **Turn 2 (Bot):** _"Dr. Asha S. Manek holds a Ph.D. in Computer Science and Engineering."_

---

## 🔌 API Integration Interface (FastAPI / Express backend)

To expose this pipeline to web/mobile applications, call `get_chat_response(session_id, user_message)`:

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ChatRequest(BaseModel):
    session_id: str
    message: str

@app.post("/api/chat")
def chat_endpoint(request: ChatRequest):
    reply = get_chat_response(request.session_id, request.message)
    return {"status": "success", "response": reply}
```

How to Ask Questions / Test It
Option A: Interactively in Python / Jupyter Notebook
Call get_chat_response directly using any custom session string (like "test_user_1"):

Python

# First Question

response1 = get_chat_response(
"test_user_1",
"Who is HOD of AI and ML department and what is the fee structure?",
)
print(response1)

# Follow-up Question (remembers previous turn)

response2 = get_chat_response("test_user_1", "What is her email?")
print(response2)
Option B: Running the API Server for Frontend
Save the code in a file named main.py.

Start the server in your terminal:

Bash
uvicorn main:app --reload --port 8000
Open http://localhost:8000/docs in your browser. FastAPI generates an interactive test UI where you can test your /api/chat route directly without writing frontend code.
