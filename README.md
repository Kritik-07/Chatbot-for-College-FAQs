# 🎓 College FAQ Chatbot

A simple **Retrieval-Augmented Generation (RAG)** chatbot for answering
questions about a college using a verified FAQ knowledge base.

The project is designed for a hackathon and focuses on one thing:

> **Ask a college-related question → retrieve the relevant FAQ →
> generate a grounded answer.**

------------------------------------------------------------------------

## 📌 What This Project Does

Students often need information about:

-   Admissions
-   Courses and departments
-   Attendance
-   Examinations
-   Fees
-   Placements
-   Hostel
-   Library
-   Scholarships
-   Internships
-   College facilities
-   Rules and regulations
-   Important contacts

Instead of searching through multiple documents manually, the chatbot
allows students to ask questions in natural language.

### Example

**User:**

> What is the minimum attendance requirement?

**System:**

1.  Converts the question into an embedding.
2.  Searches the college FAQ knowledge base using ChromaDB.
3.  Retrieves the most relevant FAQ entries.
4.  Sends the retrieved context to the LLM.
5.  Generates an answer using only that context.
6.  Displays the answer in Streamlit.

------------------------------------------------------------------------

# 🏗️ Architecture

``` text
                    User
                     │
                     ▼
                Streamlit UI
                     │
                     ▼
                RAGChain
                     │
             ┌───────┴────────┐
             │                │
             ▼                ▼
       Hugging Face       ChromaDB
        Embeddings        Vector Store
             │                │
             │         Retrieved FAQs
             │                │
             └───────┬────────┘
                     ▼
              Retrieved Context
                     │
                     ▼
                Ollama LLM
                 phi3:mini
                     │
                     ▼
             Grounded Answer
                     │
                     ▼
              Answer + Sources
```

### Optional API

FastAPI exposes the same RAG pipeline for other clients:

``` text
Other Client
     │
     ▼
  FastAPI
     │
     ▼
 RAGChain
     │
     ▼
ChromaDB + Ollama
```

FastAPI is optional. **The main application is Streamlit.**

------------------------------------------------------------------------

# ✨ Main Features

-   🔎 Semantic search over college FAQs
-   🤗 Hugging Face embeddings
-   🦜 LangChain RAG pipeline
-   🗄️ ChromaDB vector store
-   🤖 Local Ollama `phi3:mini` LLM
-   📚 Retrieved FAQ source display
-   💬 Simple Streamlit chat interface
-   🧠 Current-session conversation history using Streamlit session
    state
-   🚫 No SQLite
-   🔌 Optional FastAPI API
-   🛡️ Prompt instructs the LLM not to invent information outside the
    retrieved context

------------------------------------------------------------------------

# 🧠 Important Design Decision: FAQ Chunking

The main dataset is made of **individual Question & Answer pairs**.

Therefore:

> **1 FAQ = 1 LangChain Document = 1 vector entry**

We do **not** apply `RecursiveCharacterTextSplitter` to individual FAQ
records.

For example:

``` text
Question:
What is the minimum attendance requirement?

Answer:
Students must maintain ...

Category:
Attendance
```

is stored as one complete document.

This keeps the question and its answer together during retrieval.

### What about long PDFs?

If long unstructured PDFs are added later, they can be processed
separately using a text splitter such as
`RecursiveCharacterTextSplitter`.

------------------------------------------------------------------------

# 📁 Project Structure

``` text
college_faqs/
│
├── app.py                  # Main Streamlit application
├── api.py                  # Optional FastAPI backend
├── rag_chain.py            # RAG retrieval + LLM response
├── create_vector_db.py     # Creates ChromaDB from faqs.json
├── config.py               # Application configuration
├── chat_history.py         # Streamlit session-only chat history
│
├── faqs.json               # College FAQ knowledge base
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
├── .gitignore              # Git ignored files
│
└── chroma_db/              # Local generated vector database
```

### Important

`chroma_db/` is **generated locally** and should **not** be committed to
GitHub.

The database can always be recreated from `faqs.json`.

------------------------------------------------------------------------

# 🛠️ Technology Stack

  Technology              Purpose
  ----------------------- ----------------------------
  Python                  Main programming language
  Streamlit               Chatbot user interface
  LangChain               RAG pipeline orchestration
  Hugging Face            Text embeddings
  Sentence Transformers   Embedding model
  ChromaDB                Vector database
  Ollama                  Local LLM runtime
  `phi3:mini`             Local language model
  FastAPI                 Optional API layer
  Uvicorn                 FastAPI server

------------------------------------------------------------------------

# 🚀 Setup From Scratch

## 1. Clone the repository

``` bash
git clone https://github.com/Kritik-07/Chatbot-for-College-FAQs.git
cd Chatbot-for-College-FAQs
```

------------------------------------------------------------------------

## 2. Create a virtual environment

### Windows

``` powershell
python -m venv env
```

Activate it:

``` powershell
.\env\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can run the project using the
environment's Python directly.

Verify:

``` powershell
python -c "import sys; print(sys.executable)"
```

It should point to something similar to:

``` text
...\Chatbot-for-College-FAQs\env\python.exe
```

------------------------------------------------------------------------

## 3. Install dependencies

Use:

``` powershell
python -m pip install -r requirements.txt
```

The important Chroma integration package is:

``` text
langchain-chroma
```

This is separate from:

``` text
chromadb
```

Both are required by the current implementation.

------------------------------------------------------------------------

# 🤖 Install and Start Ollama

The project currently uses:

``` text
phi3:mini
```

Install Ollama and then download the model:

``` powershell
ollama pull phi3:mini
```

You can also test it directly:

``` powershell
ollama run phi3:mini
```

Keep Ollama available while running the chatbot.

------------------------------------------------------------------------

# 🗄️ Create the Vector Database

The source data is:

``` text
faqs.json
```

Run:

``` powershell
python create_vector_db.py
```

This will:

1.  Read `faqs.json`.
2.  Validate the FAQ records.
3.  Convert each FAQ into one LangChain `Document`.
4.  Generate Hugging Face embeddings.
5.  Store the vectors in ChromaDB.
6.  Create the local `chroma_db/` directory.

Expected output:

``` text
Created vector database with XXX FAQ documents.
Location: ./chroma_db
```

------------------------------------------------------------------------

# ▶️ Run the Streamlit Application

The main application is Streamlit.

Run:

``` powershell
python -m streamlit run app.py
```

Streamlit will provide a local URL, usually:

``` text
http://localhost:8501
```

Open that URL in your browser.

------------------------------------------------------------------------

# 🔌 Run FastAPI (Optional)

FastAPI is included only to expose the same RAG pipeline through an API.

Run:

``` powershell
python -m uvicorn api:app --reload
```

The API will normally be available at:

``` text
http://127.0.0.1:8000
```

Swagger documentation:

``` text
http://127.0.0.1:8000/docs
```

------------------------------------------------------------------------

# 📡 FastAPI Endpoints

## Health check

``` http
GET /health
```

Response:

``` json
{
  "status": "healthy"
}
```

## Chat

``` http
POST /api/chat
```

Request:

``` json
{
  "message": "What is the attendance requirement?",
  "chat_history": []
}
```

Response:

``` json
{
  "status": "success",
  "response": "....",
  "sources": [
    {
      "faq_id": "1",
      "category": "Attendance",
      "question": "What is the attendance requirement?"
    }
  ]
}
```

### Conversation history

FastAPI does **not** store chat history in SQLite or another database.

If an API client wants to maintain conversation context, it can send
previous messages in:

``` json
"chat_history": [
  {
    "role": "user",
    "content": "Who is the HOD of AI & ML?"
  },
  {
    "role": "assistant",
    "content": "..."
  }
]
```

------------------------------------------------------------------------

# 💾 Chat History

There is intentionally **no SQLite support** in this version.

For Streamlit:

``` text
st.session_state
```

stores the conversation for the current session.

This means:

-   Chat works during the current Streamlit session.
-   Refreshing/restarting the application can clear the session.
-   Conversations are not permanently stored.
-   No `chat_history.db` is created.

This keeps the hackathon implementation simple.

------------------------------------------------------------------------

# 🧩 RAG Pipeline

The core implementation is in:

``` text
rag_chain.py
```

The flow is:

``` text
User Question
      │
      ▼
Retriever
      │
      ▼
Top-K FAQ Documents
      │
      ▼
Context
      │
      ▼
Prompt
      │
      ▼
Ollama phi3:mini
      │
      ▼
Answer
```

The retriever currently uses:

``` text
RETRIEVER_K = 3
```

in `config.py`.

------------------------------------------------------------------------

# 🛡️ Hallucination Control

The prompt instructs the LLM to answer using only the retrieved college
FAQ context.

If the required information is not present, the model is instructed to
say:

``` text
I don't have information about that in the college FAQ.
```

This is important because the chatbot should not invent:

-   Fees
-   Attendance rules
-   Exam dates
-   Faculty information
-   Placement statistics
-   Contact details
-   Admission requirements

The quality of the final answer therefore depends heavily on the quality
and accuracy of `faqs.json`.

------------------------------------------------------------------------

# 📚 FAQ Dataset Format

The expected `faqs.json` structure is a list of FAQ objects.

Example:

``` json
[
  {
    "id": 1,
    "category": "Attendance",
    "question": "What is the minimum attendance requirement?",
    "answer": "Students must maintain the required minimum attendance according to the current academic regulations."
  },
  {
    "id": 2,
    "category": "Admissions",
    "question": "What documents are required for admission?",
    "answer": "The required documents are listed in the official admission guidelines."
  }
]
```

Each FAQ becomes one vector document.

------------------------------------------------------------------------

# 📝 Updating the Knowledge Base

If `faqs.json` is changed:

1.  Stop Streamlit if it is running.
2.  Stop any Python process using Chroma.
3.  Remove the old local `chroma_db/` directory.
4.  Recreate the database:

``` powershell
python create_vector_db.py
```

5.  Start Streamlit again:

``` powershell
python -m streamlit run app.py
```

### Why?

Chroma contains embeddings generated from the previous version of
`faqs.json`.

If the FAQ data changes, the vector database should be rebuilt.

------------------------------------------------------------------------

# ⚠️ Common Errors and Fixes

## Error 1: `PermissionError: [WinError 32]`

Example:

``` text
PermissionError: [WinError 32]
The process cannot access the file because it is being used by another process
```

This usually happens when `chroma_db` is still being used by Python,
Streamlit, Jupyter, or another Chroma process.

### Fix

Stop Streamlit/Jupyter/Python processes.

If you are not running another Python project:

``` powershell
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force
```

Then remove the old database:

``` powershell
Remove-Item -Recurse -Force .\chroma_db
```

Recreate it:

``` powershell
python create_vector_db.py
```

### Important

Do not commit `chroma_db/` to GitHub.

It is a generated local directory.

------------------------------------------------------------------------

## Error 2: `No module named 'langchain_chroma'`

Example:

``` text
ModuleNotFoundError: No module named 'langchain_chroma'
```

Install the missing LangChain integration:

``` powershell
python -m pip install langchain-chroma
```

Verify:

``` powershell
python -c "from langchain_chroma import Chroma; print('langchain_chroma OK')"
```

Expected:

``` text
langchain_chroma OK
```

------------------------------------------------------------------------

## Error 3: Streamlit uses the wrong Python environment

Example:

``` text
...\env\python.exe: No module named streamlit
```

This means packages were installed into a different Python environment.

Check the Python being used:

``` powershell
python -c "import sys; print(sys.executable)"
```

Then install Streamlit into that exact environment:

``` powershell
python -m pip install streamlit
```

Verify:

``` powershell
python -c "import streamlit; import langchain_chroma; print('Both working')"
```

Then start Streamlit using:

``` powershell
python -m streamlit run app.py
```

### Recommended rule

For this project, prefer:

``` powershell
python -m pip install <package>
python -m streamlit run app.py
python -m uvicorn api:app --reload
```

instead of relying on separate `pip`, `streamlit`, or `uvicorn`
executables.

This reduces Python environment mismatch problems.

------------------------------------------------------------------------

## Error 4: `NameError: name 'null' is not defined` in `chat_history.py`

If you see:

``` text
"cells": [
    {
        "cell_type": "code",
        "execution_count": null
```

then `chat_history.py` was accidentally replaced with Jupyter Notebook
JSON content.

Delete/replace that file with the actual Python `SessionChatHistory`
implementation.

Do not rename a `.ipynb` file to `.py`.

------------------------------------------------------------------------

# 🔐 GitHub and `chroma_db`

The local vector database should not be pushed to GitHub.

Your `.gitignore` should contain:

``` gitignore
chroma_db/
__pycache__/
*.pyc
.env
```

If `chroma_db` was previously tracked by Git, remove it from Git
tracking without deleting the local directory:

``` powershell
git rm -r --cached chroma_db
```

Then:

``` powershell
git add .
git commit -m "Update college FAQ chatbot"
git push origin main
```

------------------------------------------------------------------------

# 🔄 Recommended Git Workflow

Before committing:

``` powershell
git status
```

Add changes:

``` powershell
git add .
```

Check what is staged:

``` powershell
git status
```

Commit:

``` powershell
git commit -m "Update college FAQ chatbot"
```

Push:

``` powershell
git push origin main
```

If Git says:

``` text
! [rejected] main -> main (fetch first)
```

do not immediately force-push.

Use:

``` powershell
git pull --rebase origin main
```

Then:

``` powershell
git push origin main
```

If a merge/rebase conflict occurs, resolve the conflict before pushing.

------------------------------------------------------------------------

# 🧪 Basic Testing Checklist

Before the hackathon demo, test:

### Normal FAQ

``` text
What is the attendance requirement?
```

### Different wording

``` text
How much attendance do students need?
```

### Follow-up

``` text
What is the attendance requirement?
```

Then:

``` text
What happens if I don't meet it?
```

### Out-of-scope question

Ask something that is not present in the college FAQ.

Expected behavior:

``` text
I don't have information about that in the college FAQ.
```

### Empty question

The application should ask the user to enter a question instead of
crashing.

------------------------------------------------------------------------

# 🚫 Project Scope

This project intentionally does **not** include:

-   SQLite
-   Persistent conversation database
-   Complex query decomposition
-   Complex agent workflows
-   Multiple backend services
-   Authentication
-   Admin dashboard
-   Microservices
-   Kubernetes
-   Redis
-   PostgreSQL

The goal is a **simple, working RAG chatbot** suitable for a 24-hour
hackathon.

------------------------------------------------------------------------

# 🔮 Possible Future Improvements

These are outside the current hackathon scope:

-   Admin document upload
-   Automatic knowledge-base updates
-   Multilingual support
-   Voice input
-   Better evaluation using RAG evaluation frameworks
-   User authentication
-   Persistent conversation history
-   Cloud deployment
-   Feedback analytics
-   More advanced retrieval/reranking

------------------------------------------------------------------------

# 👥 Team Responsibilities

  -----------------------------------------------------------------------
  Role                                Responsibility
  ----------------------------------- -----------------------------------
  AI / LLM                            RAG pipeline, embeddings,
                                      retrieval, prompting, LLM

  Data / Knowledge Base               College information, FAQs,
                                      verification, sources

  UI / UX                             Streamlit interface and user
                                      experience

  Integration / QA                    Integration, testing, deployment,
                                      GitHub, documentation
  -----------------------------------------------------------------------

------------------------------------------------------------------------

# 🎯 Final Goal

The project should provide a simple experience:

``` text
Open College FAQ Chatbot
          ↓
Ask a college question
          ↓
Search the verified FAQ knowledge base
          ↓
Retrieve relevant information
          ↓
Generate a grounded response
          ↓
Display answer + source
```

The priority is:

> **Accuracy → Reliability → Simplicity → User Experience**

rather than adding unnecessary features.
