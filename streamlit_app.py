import os

import streamlit as st
from dotenv import load_dotenv

from app.qa import DEFAULT_MODEL, stream_resume_chat
from app.resume_config import CANDIDATE_NAME, PERSONA_MODE, SYSTEM_PROMPT
from app.resume_loader import format_system_prompt, get_resume_data
from app.retrieval import retrieve_resume_context

load_dotenv()

st.set_page_config(
    page_title=f"{CANDIDATE_NAME} | AI Assistant",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded",
)

if "messages" not in st.session_state:
    st.session_state.messages = []
if "custom_prompt" not in st.session_state:
    st.session_state.custom_prompt = SYSTEM_PROMPT
if "persona_mode" not in st.session_state:
    st.session_state.persona_mode = PERSONA_MODE
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False


def get_configured_api_key() -> str:
    """Read the Groq key from Streamlit secrets or the environment."""
    try:
        key = st.secrets.get("GROQ_API_KEY", "")
        if key:
            return key
    except Exception:
        pass
    return os.getenv("GROQ_API_KEY", "")


resume_info = get_resume_data()
resume_text = resume_info["text"]
detected_key = get_configured_api_key()

with st.sidebar:
    st.markdown(
        f"""
        <div class="brand-lockup">
            <div class="brand-icon">✦</div>
            <div><div class="brand-title">Ujjwal AI</div>
            <div class="brand-caption">CAREER ASSISTANT</div></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.toggle("Dark appearance", key="dark_mode", help="Switch between light and dark themes.")
    st.markdown('<div class="side-label">CONNECTION</div>', unsafe_allow_html=True)
    if detected_key:
        groq_api_key = detected_key
        st.markdown('<div class="connection-pill"><span></span> Groq connected</div>', unsafe_allow_html=True)
    else:
        groq_api_key = st.text_input(
            "Groq API key",
            type="password",
            placeholder="gsk_…",
            help="Set GROQ_API_KEY in .env or Streamlit Secrets.",
            label_visibility="collapsed",
        )
        if not groq_api_key:
            st.caption("Add a Groq key to start chatting.")

    st.markdown('<div class="side-label">YOUR RESUME</div>', unsafe_allow_html=True)
   

    
    

    if st.button("🗑️  Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()


dark = st.session_state.dark_mode
palette = {
    "page": "#0B1120" if dark else "#F5F7FB",
    "surface": "#111B2E" if dark else "#FFFFFF",
    "sidebar": "#0F1728" if dark else "#FFFFFF",
    "text": "#E7EDF7" if dark else "#172033",
    "muted": "#9AA8BD" if dark else "#68758A",
    "border": "#253149" if dark else "#E4E9F1",
    "soft": "#172338" if dark else "#F7F8FC",
    "accent": "#8B8CF8" if dark else "#5B5CE2",
    "accent_soft": "#24284A" if dark else "#F0F0FF",
}

st.markdown(
    f"""
    <style>
    :root {{
      --page: {palette['page']}; --surface: {palette['surface']}; --sidebar: {palette['sidebar']};
      --text: {palette['text']}; --muted: {palette['muted']}; --border: {palette['border']};
      --soft: {palette['soft']}; --accent: {palette['accent']}; --accent-soft: {palette['accent_soft']};
    }}
    .stApp, [data-testid="stAppViewContainer"] {{ background: var(--page); color: var(--text); }}
    [data-testid="stHeader"] {{ background: transparent; }}
    [data-testid="stSidebar"] > div:first-child {{ background: var(--sidebar); border-right: 1px solid var(--border); }}
    [data-testid="stSidebar"] {{ color: var(--text); }}
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
    [data-testid="stSidebar"] label {{ color: var(--text); }}
    [data-testid="stMain"] > div {{ padding-top: 2.2rem; }}
    .block-container {{ max-width: 1120px; padding-top: 2.3rem; padding-bottom: 7rem; }}
    .brand-lockup {{ display:flex; align-items:center; gap:12px; padding:10px 4px 22px; }}
    .brand-icon {{ width:42px; height:42px; display:grid; place-items:center; border-radius:14px;
      color:#fff; font-size:23px; background:linear-gradient(135deg,#7778F6,#4B4CCF);
      box-shadow:0 8px 22px #5556d533; }}
    .brand-title {{ color:var(--text); font-size:19px; font-weight:750; letter-spacing:-.4px; }}
    .brand-caption {{ color:var(--muted); font-size:9px; font-weight:700; letter-spacing:1.5px; margin-top:2px; }}
    .side-label {{ color:var(--muted); font-size:10px; letter-spacing:1.4px; font-weight:750;
      margin:20px 0 9px; }}
    .connection-pill {{ display:inline-flex; align-items:center; gap:8px; padding:8px 12px;
      color:{'#B6F1D0' if dark else '#166843'}; background:{'#102B27' if dark else '#EAF8F0'};
      border:1px solid {'#1E5044' if dark else '#CDEEDB'}; border-radius:999px; font-size:12px; font-weight:650; }}
    .connection-pill span {{ width:7px; height:7px; border-radius:50%; background:#36BE79;
      box-shadow:0 0 0 4px #36BE7922; }}
    .resume-card {{ border:1px solid var(--border); border-radius:14px; background:var(--soft); padding:14px; }}
    .resume-card-title {{ color:var(--text); font-size:13px; font-weight:700; }}
    .resume-card-meta {{ color:var(--muted); font-size:11px; margin-top:7px; }}
    .resume-card-source {{ color:var(--muted); font-size:10px; margin-top:5px; overflow-wrap:anywhere; }}
    .hero {{ border:1px solid var(--border); border-radius:24px; padding:30px 34px; margin:4px 0 24px;
      background:radial-gradient(ellipse at 88% 0%, {'#282954' if dark else '#EBEBFF'} 0%, transparent 38%),var(--surface);
      box-shadow:0 12px 34px {'#00000022' if dark else '#2934500A'}; }}
    .hero-eyebrow {{ color:var(--accent); font-size:11px; font-weight:750; letter-spacing:1.5px; text-transform:uppercase; }}
    .hero-title {{ color:var(--text); font-size:clamp(28px,4vw,40px); font-weight:780; letter-spacing:-1.3px;
      line-height:1.14; margin:10px 0 9px; }}
    .hero-copy {{ color:var(--muted); font-size:14px; line-height:1.65; max-width:660px; margin:0; }}
    .hero-tags {{ display:flex; gap:8px; flex-wrap:wrap; margin-top:18px; }}
    .hero-tag {{ color:var(--text); border:1px solid var(--border); background:var(--soft);
      border-radius:999px; padding:6px 10px; font-size:11px; font-weight:600; }}
    .section-title {{ color:var(--text); font-size:15px; font-weight:720; margin:22px 0 10px; }}
    div.stButton > button {{ color:var(--text); background:var(--surface); border:1px solid var(--border);
      border-radius:14px; min-height:58px; text-align:left; padding:12px 16px; font-weight:550;
      transition:all .16s ease; box-shadow:0 3px 10px {'#00000012' if dark else '#25334B08'}; }}
    div.stButton > button:hover {{ border-color:var(--accent); color:var(--accent);
      background:var(--accent-soft); transform:translateY(-1px); }}
    [data-testid="stChatMessage"] {{ background:var(--surface); border:1px solid var(--border);
      border-radius:18px; padding:16px 18px; margin:10px 0; }}
    [data-testid="stChatMessage"] p, [data-testid="stChatMessage"] li {{ color:var(--text); }}
    [data-testid="stChatInput"] {{ border-color:var(--border); background:var(--surface); border-radius:16px; }}
    [data-testid="stChatInput"] textarea {{ color:var(--text); }}
    [data-testid="stExpander"] {{ border-color:var(--border); border-radius:12px; }}
    [data-testid="stSidebar"] [data-testid="stExpander"] {{ background:var(--soft); }}
    [data-testid="stMarkdownContainer"] a {{ color:var(--accent); }}
    [data-testid="stCaptionContainer"] {{ color:var(--muted); }}
    @media (max-width: 700px) {{ .block-container {{ padding:1.2rem 1rem 6rem; }} .hero {{ padding:22px; }} }}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <section class="hero">
      <div class="hero-eyebrow">Recruiter-ready · Groq streaming</div>
      <div class="hero-title">Meet {CANDIDATE_NAME}'s AI assistant</div>
      <p class="hero-copy">Ask about experience, projects, skills, education, or profile links.
      Answers are grounded in the resume and verified profile URLs.</p>
      <div class="hero-tags"><span class="hero-tag">Resume grounded</span>
      <span class="hero-tag">Live responses</span><span class="hero-tag">Python · AI · Backend</span></div>
    </section>
    """,
    unsafe_allow_html=True,
)

if not st.session_state.messages:
    st.markdown('<div class="section-title">Try asking</div>', unsafe_allow_html=True)
    suggestions = [
        ("🧠  What are your key AI and backend skills?", "What are your top AI and backend skills?"),
        ("🚀  Tell me about your RAG chatbot project", "Tell me about your RAG chatbot project."),
        ("🎓  Summarize your education", "What is your education background?"),
        ("🔗  Share your profile links", "Can you share your GitHub, LinkedIn, and portfolio links?"),
    ]
    left, right = st.columns(2)
    for index, (label, question) in enumerate(suggestions):
        with (left if index % 2 == 0 else right):
            if st.button(label, use_container_width=True, key=f"suggestion_{index}"):
                st.session_state.pending_question = question
                st.rerun()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_prompt = st.chat_input(f"Ask {CANDIDATE_NAME} a question...")
if st.session_state.get("pending_question"):
    user_prompt = st.session_state.pop("pending_question")

if user_prompt:
    if not groq_api_key:
        st.error("Add a Groq API key in the sidebar to start chatting.")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    with st.chat_message("assistant"):
        try:
            with st.spinner("Finding relevant resume details..."):
                resume_context = retrieve_resume_context(resume_text, user_prompt)
                system_prompt = format_system_prompt(
                    candidate_name=CANDIDATE_NAME,
                    persona_mode=st.session_state.persona_mode,
                    custom_system_prompt=st.session_state.custom_prompt,
                    resume_content=resume_context,
                )
            answer = st.write_stream(
                stream_resume_chat(
                    question=user_prompt,
                    system_prompt=system_prompt,
                    chat_history=st.session_state.messages[:-1],
                    api_key=groq_api_key,
                    model=DEFAULT_MODEL,
                )
            )
            st.session_state.messages.append({"role": "assistant", "content": answer})
        except Exception as exc:
            st.error(f"Could not generate a response: {exc}")
