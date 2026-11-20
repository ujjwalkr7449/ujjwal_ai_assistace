import os

import streamlit as st
from dotenv import load_dotenv

# Load local environment variables (.env)
load_dotenv()

from app.resume_config import (
    CANDIDATE_NAME,
    PERSONA_MODE,
    SYSTEM_PROMPT,
)
from app.resume_loader import get_resume_data, format_system_prompt
from app.retrieval import retrieve_resume_context
from app.qa import stream_resume_chat, DEFAULT_MODEL


# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title=f"{CANDIDATE_NAME} - AI Resume Chatbot",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded",
)


# -----------------------------
# Custom Styling
# -----------------------------
st.markdown(
    """
    <style>
        .main-header {
            font-size: 2.2rem;
            font-weight: 700;
            color: #1E293B;
            margin-bottom: 0.2rem;
        }
        .sub-header {
            font-size: 1.05rem;
            color: #64748B;
            margin-bottom: 1.5rem;
        }
        .status-pill {
            display: inline-block;
            background-color: #ECFDF5;
            color: #065F46;
            border: 1px solid #A7F3D0;
            padding: 4px 10px;
            border-radius: 9999px;
            font-size: 0.85rem;
            font-weight: 500;
            margin-bottom: 12px;
        }
        .starter-card {
            background-color: #F8FAFC;
            border: 1px solid #E2E8F0;
            border-radius: 8px;
            padding: 12px 16px;
            margin-bottom: 10px;
            cursor: pointer;
            transition: all 0.2s ease;
        }
        .starter-card:hover {
            border-color: #6366F1;
            background-color: #EEF2FF;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# -----------------------------
# Session State Initialization
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "custom_prompt" not in st.session_state:
    st.session_state.custom_prompt = SYSTEM_PROMPT

if "persona_mode" not in st.session_state:
    st.session_state.persona_mode = PERSONA_MODE


# -----------------------------
# API Key Helper
# -----------------------------
def get_configured_api_key() -> str:
    """Retrieve Groq API key from Streamlit secrets, environment, or user input."""
    try:
        if "GROQ_API_KEY" in st.secrets and st.secrets["GROQ_API_KEY"]:
            return st.secrets["GROQ_API_KEY"]
    except Exception:
        pass

    env_key = os.getenv("GROQ_API_KEY", "")
    if env_key:
        return env_key

    return ""


# -----------------------------
# Load Resume from Code / Data
# -----------------------------
resume_info = get_resume_data()
resume_text = resume_info["text"]
resume_source = resume_info["source"]


# -----------------------------
# Sidebar Configuration
# -----------------------------
with st.sidebar:
    st.title("💼 AI Portfolio Bot")
    st.caption("Powered by Groq & Llama-3.3")

    # API Key Handling
    detected_key = get_configured_api_key()
    if detected_key:
        groq_api_key = detected_key
        st.success("✅ Groq API Key Connected")
    else:
        groq_api_key = st.text_input(
            "Groq API Key",
            type="password",
            placeholder="gsk_...",
            help="Add your Groq API key in .env, Streamlit Secrets, or here.",
        )
        if not groq_api_key:
            st.warning("⚠️ Enter your Groq API Key to chat.")

    st.divider()

    # Active Resume Status
    st.markdown("### 📄 Active Resume")
    st.markdown(
        f"""
        <div class="status-pill">
            🟢 Active in Code
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.caption(f"**Source:** {resume_source}")
    st.caption(f"**Word Count:** {resume_info['word_count']} words (~{resume_info['char_count']} chars)")

    with st.expander("👀 View Active Resume Text", expanded=False):
        st.text_area(
            "Resume Content",
            value=resume_text,
            height=220,
            disabled=True,
            help="To change this, edit app/resume_config.py or place your resume.pdf into the data/ folder.",
        )

    st.divider()

    # Persona & Model Customization
    st.markdown("### 🎭 Persona & Behavior")
    selected_persona = st.radio(
        "Chatbot Persona",
        options=["first_person", "assistant"],
        format_func=lambda x: "First Person ('I', 'My skills')" if x == "first_person" else f"Third Person ('{CANDIDATE_NAME}'s AI Assistant')",
        index=0 if st.session_state.persona_mode == "first_person" else 1,
    )
    st.session_state.persona_mode = selected_persona

    

    with st.expander("⚙️ System Prompt (Code-Configured)", expanded=False):
        prompt_input = st.text_area(
            "Customize Prompt Template",
            value=st.session_state.custom_prompt,
            height=200,
            help="Variables: {candidate_name}, {persona_instruction}, {resume_content}",
        )
        if st.button("Apply Prompt Changes", use_container_width=True):
            st.session_state.custom_prompt = prompt_input
            st.success("System prompt updated!")

    st.divider()

    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()


# -----------------------------
# Main Chat Interface
# -----------------------------
st.markdown(
    f'<div class="main-header">👋 Meet {CANDIDATE_NAME}\'s AI Assistant</div>',
    unsafe_allow_html=True,
)
st.markdown(
    f'<div class="sub-header">Ask me anything about my experience, skills, projects, and education directly. '
    f'Answers are generated strictly according to my resume and system prompt.</div>',
    unsafe_allow_html=True,
)

# -----------------------------
# Starter Questions (When chat is empty)
# -----------------------------
if not st.session_state.messages:
    st.info("💡 **Click any question below or type your own question to start:**")

    starter_col1, starter_col2 = st.columns(2)
    sample_q1 = "What are your top technical skills and areas of expertise?"
    sample_q2 = "Can you describe your most significant project and its impact?"
    sample_q3 = "What is your educational background and qualifications?"
    sample_q4 = f"Why would you be a strong candidate for an engineering role?"

    with starter_col1:
        if st.button(f"🛠️ {sample_q1}", use_container_width=True):
            st.session_state.pending_question = sample_q1
            st.rerun()
        if st.button(f"🎓 {sample_q3}", use_container_width=True):
            st.session_state.pending_question = sample_q3
            st.rerun()

    with starter_col2:
        if st.button(f"🚀 {sample_q2}", use_container_width=True):
            st.session_state.pending_question = sample_q2
            st.rerun()
        if st.button(f"🌟 {sample_q4}", use_container_width=True):
            st.session_state.pending_question = sample_q4
            st.rerun()


# -----------------------------
# Chat History Replay
# -----------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# -----------------------------
# Handle Pending / New Input
# -----------------------------
user_prompt = st.chat_input(f"Ask anything about {CANDIDATE_NAME}'s background...")

# Check if a starter question was clicked
if "pending_question" in st.session_state and st.session_state.pending_question:
    user_prompt = st.session_state.pending_question
    del st.session_state.pending_question

if user_prompt:
    if not groq_api_key:
        st.error("Please provide a Groq API key in the sidebar to chat.")
        st.stop()

    # Append user question to session state
    st.session_state.messages.append({
        "role": "user",
        "content": user_prompt,
    })
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # Stream Assistant Response
    with st.chat_message("assistant"):
        try:
            with st.spinner("Finding relevant resume details..."):
                resume_context = retrieve_resume_context(resume_text, user_prompt)
                formatted_system_prompt = format_system_prompt(
                    candidate_name=CANDIDATE_NAME,
                    persona_mode=st.session_state.persona_mode,
                    custom_system_prompt=st.session_state.custom_prompt,
                    resume_content=resume_context,
                )

            # We exclude the message just added to avoid duplicate user turns
            history_context = st.session_state.messages[:-1]

            token_stream = stream_resume_chat(
                question=user_prompt,
                system_prompt=formatted_system_prompt,
                chat_history=history_context,
                api_key=groq_api_key,
                model=DEFAULT_MODEL
            )

            full_response = st.write_stream(token_stream)

            # Save assistant response
            st.session_state.messages.append({
                "role": "assistant",
                "content": full_response,
            })

        except Exception as exc:
            st.error(f"Error generating answer: {exc}")
