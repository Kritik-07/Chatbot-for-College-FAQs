import os

import streamlit as st

from chat_history import SessionChatHistory
from rag_chain import RAGChain


st.set_page_config(
    page_title="College FAQ Chatbot",
    page_icon="🎓",
    layout="centered",
)

st.title("🎓 College FAQ Chatbot")
st.caption("Ask questions about your college, courses, fees, exams, placements, and more.")


# ---------------------------------------------------------
# Check vector database
# ---------------------------------------------------------
if not os.path.exists("./chroma_db"):
    st.error("Vector database not found.")
    st.info("Run this once before starting Streamlit:")
    st.code("python create_vector_db.py")
    st.stop()


# ---------------------------------------------------------
# Initialize once per Streamlit session
# ---------------------------------------------------------
@st.cache_resource
def load_rag():
    return RAGChain()


try:
    rag = load_rag()
except Exception as exc:
    st.error("Could not initialize the RAG system.")
    st.exception(exc)
    st.stop()


history = SessionChatHistory()


# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------
with st.sidebar:
    st.header("🎓 College FAQ")
    st.write("Ask questions from the college knowledge base.")

    if st.button("🗑️ Clear Chat", use_container_width=True):
        history.clear()
        st.rerun()


# ---------------------------------------------------------
# Display conversation
# ---------------------------------------------------------
for message in history.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# ---------------------------------------------------------
# Chat input
# ---------------------------------------------------------
question = st.chat_input("Ask your college question...")

if question:
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Searching the college FAQ..."):
            try:
                result = rag.get_response(
                    question,
                    chat_history=history.messages,
                )

                answer = result["answer"]
                sources = result["sources"]

                st.markdown(answer)

                if sources:
                    with st.expander("📚 Sources"):
                        for source in sources:
                            category = source.get("category", "Unknown")
                            faq_question = source.get("question", "")
                            faq_id = source.get("faq_id", "")

                            st.write(
                                f"**FAQ {faq_id} — {category}**"
                            )
                            st.caption(faq_question)

                history.add_user_message(question)
                history.add_ai_message(answer)

            except Exception as exc:
                st.error("Something went wrong while processing your question.")
                st.exception(exc)