
import sys
from pathlib import Path

import streamlit as st

# Locate the project and source directories
PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from generation.answer_generator import answer_question


# Page configuration
st.set_page_config(
    page_title="Greenfield University Assistant",
    page_icon="🎓",
    layout="centered"
)


# Custom styling
st.markdown(
    """
    <style>
    .main-title {
        text-align: center;
        font-size: 32px;
        font-weight: bold;
        color: #2563EB;
    }

    .subtitle {
        text-align: center;
        color: gray;
        font-size: 16px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Application heading
st.markdown(
    '<div class="main-title">🎓 Greenfield University</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Academic Information Assistant</div>',
    unsafe_allow_html=True
)

st.write("Ask questions about admissions, examinations, fees, scholarships, and university facilities.")

st.divider()


# Sidebar
with st.sidebar:
    st.header("About")

    st.write(
        "This assistant uses Retrieval-Augmented Generation (RAG) "
        "to answer questions using university documents."
    )

    st.caption(
        "Information is based on the fictional Greenfield University "
        "sample documents for academic year 2026–2027."
    )

    if st.button("Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()


# Initialize conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []


# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        if message["role"] == "assistant" and message.get("sources"):
            with st.expander("View retrieved sources"):
                for source in message["sources"]:
                    st.write(f"📄 {source}")


# Chat input
question = st.chat_input("Ask your university-related question...")


if question:
    # Display student question
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.markdown(question)

    # Generate answer
    with st.chat_message("assistant"):
        with st.spinner("Searching university documents and generating answer..."):
            try:
                result = answer_question(question)

                answer = result["answer"]
                sources = result["sources"]

                st.markdown(answer)

                if sources:
                    with st.expander("View retrieved sources"):
                        for source in sources:
                            st.write(f"📄 {source}")

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "sources": sources
                })

            except Exception as error:
                st.error(
                    "An error occurred while generating the answer. "
                    "Please try again."
                )
                st.exception(error)
