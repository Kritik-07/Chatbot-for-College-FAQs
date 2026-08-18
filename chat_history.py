import streamlit as st


class SessionChatHistory:
    """Simple Streamlit-only chat history. No SQLite."""

    KEY = "chat_messages"

    def __init__(self):
        if self.KEY not in st.session_state:
            st.session_state[self.KEY] = []

    @property
    def messages(self):
        return st.session_state[self.KEY]

    def add_user_message(self, content: str):
        self.messages.append({
            "role": "user",
            "content": content
        })

    def add_ai_message(self, content: str):
        self.messages.append({
            "role": "assistant",
            "content": content
        })

    def clear(self):
        st.session_state[self.KEY] = []