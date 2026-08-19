import os
import streamlit as st


# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(
    page_title="TJIT CollegeAI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Hello! 👋 I'm TJIT CollegeAI, your T. John Institute "
                "of Technology assistant. How can I help you?"
            ),
            "source": None,
        }
    ]


# ---------------------------------------------------------
# LOGO
# ---------------------------------------------------------
logo_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "tjohn_logo.jpg"
)


# ---------------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------------
st.markdown(
    """
    <style>

    /* ---------- GLOBAL ---------- */

    .stApp {
        background: #ffffff;
        color: #111827;
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        visibility: hidden;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 1.5rem;
        max-width: 1400px;
    }


    /* ---------- SIDEBAR ---------- */

    section[data-testid="stSidebar"] {
        background: #f8f9fc;
        border-right: 1px solid #e5e7eb;
    }

    section[data-testid="stSidebar"] > div {
        padding: 1.5rem 1.2rem;
    }

    .logo-container {
        text-align: center;
        padding: 0.5rem 0 0.8rem 0;
    }

    .logo-container img {
        width: 105px;
        height: 105px;
        object-fit: contain;
        border-radius: 50%;
    }

    .brand-name {
        text-align: center;
        font-size: 24px;
        font-weight: 700;
        color: #111a3a;
        margin-top: 8px;
    }

    .brand-subtitle {
        text-align: center;
        color: #68708a;
        font-size: 14px;
        line-height: 1.4;
        margin-top: 4px;
        margin-bottom: 22px;
    }

    .sidebar-divider {
        height: 1px;
        background: #e5e7eb;
        margin: 15px 0 20px 0;
    }

    .about-title {
        color: #2738b8;
        font-size: 16px;
        font-weight: 600;
        margin-bottom: 10px;
    }

    .about-card {
        background: #ffffff;
        border: 1px solid #e3e6ee;
        border-radius: 14px;
        padding: 16px;
        box-shadow: 0 2px 8px rgba(20, 30, 70, 0.04);
    }

    .about-heading {
        color: #111827;
        font-size: 15px;
        font-weight: 650;
        margin-bottom: 13px;
    }

    .about-item {
        display: flex;
        gap: 9px;
        margin: 10px 0;
        color: #4b5563;
        font-size: 12.5px;
        line-height: 1.45;
    }

    .about-icon {
        color: #3548d4;
        min-width: 16px;
        font-size: 14px;
    }

    .trust-box {
        margin-top: 22px;
        padding: 12px 10px;
        color: #69728a;
        font-size: 12px;
        line-height: 1.4;
        border-top: 1px solid #e5e7eb;
    }

    .trust-title {
        color: #4b5563;
        font-weight: 600;
    }


    /* ---------- MAIN HEADER ---------- */

    .main-header {
        padding: 0.3rem 1rem 1rem 1rem;
    }

    .main-title {
        font-size: 40px;
        font-weight: 750;
        letter-spacing: -1px;
        color: #111a3a;
        margin-bottom: 3px;
    }

    .main-subtitle {
        color: #737b91;
        font-size: 16px;
    }


    /* ---------- CHAT AREA ---------- */

    .chat-area {
        max-width: 1050px;
        margin: 35px auto 0 auto;
        padding: 0 20px;
    }

    .user-message {
        display: flex;
        justify-content: flex-end;
        margin: 20px 0 28px 0;
    }

    .user-bubble {
        max-width: 570px;
        background: #f0f3ff;
        border: 1px solid #e1e6ff;
        border-radius: 16px 16px 5px 16px;
        padding: 17px 20px;
        color: #18213d;
        font-size: 15px;
        line-height: 1.6;
    }

    .assistant-row {
        display: flex;
        align-items: flex-start;
        gap: 14px;
        margin-bottom: 8px;
    }

    .bot-icon {
        width: 38px;
        height: 38px;
        min-width: 38px;
        border-radius: 50%;
        background: #eef1ff;
        border: 1px solid #dce2ff;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #3449d5;
        font-size: 18px;
    }

    .assistant-bubble {
        max-width: 720px;
        background: #ffffff;
        border: 1px solid #e4e7ee;
        border-radius: 5px 16px 16px 16px;
        padding: 18px 22px;
        color: #1b243b;
        font-size: 15px;
        line-height: 1.7;
        box-shadow: 0 3px 12px rgba(20, 30, 70, 0.035);
    }

    .source-label {
        margin-left: 52px;
        margin-top: 9px;
        color: #3147d3;
        font-size: 13px;
        font-weight: 600;
    }

    .source-text {
        margin-left: 52px;
        margin-top: 4px;
        color: #7a8297;
        font-size: 12px;
    }


    /* ---------- INPUT ---------- */

    .input-wrapper {
        max-width: 1050px;
        margin: 70px auto 0 auto;
        padding: 0 20px;
    }

    div[data-testid="stForm"] {
        border: 1px solid #e1e4eb !important;
        border-radius: 16px !important;
        padding: 10px !important;
        background: #ffffff !important;
        box-shadow: 0 5px 20px rgba(20, 30, 70, 0.05) !important;
    }

    div[data-testid="stForm"] input {
        border: 1px solid #e1e4eb !important;
        border-radius: 10px !important;
        height: 48px !important;
        font-size: 15px !important;
        padding-left: 15px !important;
    }

    div[data-testid="stForm"] input:focus {
        border-color: #5265dc !important;
        box-shadow: 0 0 0 1px #5265dc !important;
    }

    div[data-testid="stForm"] button {
        height: 48px !important;
        border-radius: 10px !important;
        background: #4054d8 !important;
        color: white !important;
        border: none !important;
        font-weight: 600 !important;
        font-size: 15px !important;
    }

    div[data-testid="stForm"] button:hover {
        background: #3347c7 !important;
    }


    /* ---------- MOBILE-ish STREAMLIT WIDTH ---------- */

    @media (max-width: 900px) {

        .main-title {
            font-size: 30px;
        }

        .chat-area {
            padding: 0 5px;
        }

        .input-wrapper {
            padding: 0 5px;
        }

        .assistant-bubble {
            max-width: 100%;
        }

        .user-bubble {
            max-width: 85%;
        }
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------
with st.sidebar:

    if os.path.exists(logo_path):
        st.markdown('<div class="logo-container">', unsafe_allow_html=True)
        st.image(logo_path, width=105)
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.warning("TJIT logo not found.")

    st.markdown(
        '<div class="brand-name">TJIT CollegeAI</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="brand-subtitle">'
        "T. John Institute of Technology Assistant"
        "</div>",
        unsafe_allow_html=True,
    )

    if st.button(
        "＋  New Chat",
        use_container_width=True,
        key="new_chat",
    ):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": (
                    "Hello! 👋 I'm TJIT CollegeAI, your T. John Institute "
                    "of Technology assistant. How can I help you?"
                ),
                "source": None,
            }
        ]
        st.rerun()

    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)

    st.markdown(
        '<div class="about-title">ⓘ &nbsp; About College</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="about-card">

            <div class="about-heading">
                T. John Institute of Technology
            </div>

            <div class="about-item">
                <span class="about-icon">⌖</span>
                <span>
                    Gottigere, Bannerghatta Road,<br>
                    Bengaluru – 560083, Karnataka
                </span>
            </div>

            <div class="about-item">
                <span class="about-icon">▣</span>
                <span>
                    Affiliated to Visvesvaraya
                    Technological University (VTU)
                </span>
            </div>

            <div class="about-item">
                <span class="about-icon">▤</span>
                <span>
                    AICTE approved institution
                </span>
            </div>

            <div class="about-item">
                <span class="about-icon">⌂</span>
                <span>
                    20-acre campus with modern
                    academic facilities
                </span>
            </div>

            <div class="about-item">
                <span class="about-icon">▦</span>
                <span>
                    Engineering and postgraduate
                    programs across multiple disciplines
                </span>
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="trust-box">
            <span class="trust-title">✓ Trusted Campus Information</span><br>
            Powered by the TJIT College FAQ knowledge base.
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------
# MAIN HEADER
# ---------------------------------------------------------
st.markdown(
    """
    <div class="main-header">
        <div class="main-title">TJIT CollegeAI</div>
        <div class="main-subtitle">
            Your T. John Institute of Technology Assistant
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# CHAT DISPLAY
# ---------------------------------------------------------
st.markdown('<div class="chat-area">', unsafe_allow_html=True)

for message in st.session_state.messages:

    if message["role"] == "user":

        st.markdown(
            f"""
            <div class="user-message">
                <div class="user-bubble">
                    {message["content"]}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    else:

        st.markdown(
            f"""
            <div class="assistant-row">
                <div class="bot-icon">✦</div>
                <div class="assistant-bubble">
                    {message["content"]}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if message.get("source"):
            st.markdown(
                '<div class="source-label">▤ &nbsp; Sources</div>',
                unsafe_allow_html=True,
            )

            st.markdown(
                f'<div class="source-text">{message["source"]}</div>',
                unsafe_allow_html=True,
            )

st.markdown("</div>", unsafe_allow_html=True)


# ---------------------------------------------------------
# CHAT INPUT
# ---------------------------------------------------------
st.markdown('<div class="input-wrapper">', unsafe_allow_html=True)

with st.form("chat_form", clear_on_submit=True):

    col1, col2 = st.columns([7, 1])

    with col1:
        question = st.text_input(
            "Question",
            placeholder="Ask your question about TJIT...",
            label_visibility="collapsed",
        )

    with col2:
        send = st.form_submit_button(
            "➤  Send",
            use_container_width=True,
        )


# ---------------------------------------------------------
# TEMPORARY FRONTEND RESPONSE
# ---------------------------------------------------------
if send and question.strip():

    user_question = question.strip()

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_question,
            "source": None,
        }
    )

    # Temporary response.
    # We will replace this section with your RAG/API response later.
    temporary_answer = (
        "I'm ready to help with questions about T. John Institute "
        "of Technology, including admissions, academics, fees, "
        "placements, hostel, campus facilities and more."
    )

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": temporary_answer,
            "source": "TJIT College FAQ Knowledge Base",
        }
    )

    st.rerun()

st.markdown("</div>", unsafe_allow_html=True)