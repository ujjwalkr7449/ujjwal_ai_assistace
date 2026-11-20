"""
Resume & Chatbot Configuration Module.
Configure your personal details, resume text, or resume file here directly in code.
"""

from pathlib import Path

# -------------------------------------------------------------
# 1. Candidate Identity & Persona
# -------------------------------------------------------------
CANDIDATE_NAME = "Ujjwal"

# Persona mode:
# - "first_person": Bot answers as the candidate ("I worked at...", "My skills are...")
# - "assistant": Bot answers as a personal AI representative ("Ujjwal has experience in...", "His key skills are...")
PERSONA_MODE = "first_person"

# -------------------------------------------------------------
# 2. System Prompt
# Customize how the chatbot behaves, its tone, and guardrails.
# -------------------------------------------------------------
SYSTEM_PROMPT = """You are the personal AI Assistant and representative for {candidate_name}.
Your mission is to answer questions from recruiters, hiring managers, and interviewers about {candidate_name}'s background, skills, work experience, projects, education, and career aspirations.

Guidelines:
1. Ground your answers strictly on the provided Resume content below.
2. Maintain a professional, polite, enthusiastic, and confident tone.
3. {persona_instruction}
4. When describing achievements and projects, highlight technologies, problem-solving, and impact.
5. If an interviewer asks about a skill, framework, or detail that is NOT present in the resume:
   - State honestly that it is not explicitly listed in the resume.
   - Mention relevant transferable skills or related technologies that {candidate_name} knows.
6. Never make up fake degrees, fake companies, or fraudulent work experience.
7. Keep responses concise, well-structured, and easy to read using bullet points when discussing technical skills or projects.

--- RESUME START ---
{resume_content}
--- RESUME END ---
"""

# -------------------------------------------------------------
# 3. Resume Source Configuration
# You can provide your resume in CODE using EITHER:
#
# Option A: Place your resume file (PDF or TXT) inside the 'data/' folder
#           (e.g., data/resume.pdf or data/resume.txt)
# Option B: Paste your raw resume text directly into the RESUME_TEXT variable below.
# -------------------------------------------------------------

# Path to local resume file (if using a PDF/TXT file)
RESUME_FILE_PATH = Path("data/resume.pdf")  # Change this path if your resume file is located elsewhere

# Direct Raw Text Resume:
# If you paste your resume text here, it will be used directly without needing any PDF file!
# Leave as empty string "" if you prefer to use the PDF file specified in RESUME_FILE_PATH.
RESUME_TEXT = """
Ujjwal
Software Engineer & Full Stack / AI Developer
Email: ujjwal@example.com | Phone: +91-XXXXXXXXXX
LinkedIn: linkedin.com/in/ujjwal | GitHub: github.com/ujjwal

SUMMARY:
Results-driven Software Engineer with experience in building AI-powered applications, full-stack web platforms, and scalable backend APIs. Proficient in Python, FastAPI, Streamlit, LangChain, RAG architectures, and modern cloud deployment. Passionate about machine learning, generative AI, and efficient system design.

TECHNICAL SKILLS:
- Languages: Python, JavaScript/TypeScript, SQL, HTML/CSS
- AI & LLM: LangChain, Groq, OpenAI API, RAG, FAISS, Sentence-Transformers, Vector Databases
- Web & Backend: FastAPI, Streamlit, Flask, REST APIs, SSE (Server-Sent Events)
- Databases: PostgreSQL, SQLite, FAISS Vector Store
- Tools & Cloud: Git, GitHub, Docker, Streamlit Community Cloud, Linux

PROJECTS:
1. RAG-Powered AI Resume & Document Chatbot
   - Developed an intelligent retrieval-augmented generation (RAG) chatbot using LangChain, Groq (Llama-3.3-70B), and Streamlit.
   - Implemented real-time token streaming and FAISS vector similarity search for instant question answering.
   - Designed code-configured resume grounding and customizable persona system prompts for automated technical interviews.

2. Full-Stack Web Application & API Service
   - Built modular backend REST APIs using FastAPI with asynchronous request handling.
   - Integrated secure token authentication, database persistence, and automated documentation via OpenAPI/Swagger.

EDUCATION:
- Bachelor of Technology (B.Tech) in Computer Science & Engineering
- Relevant Coursework: Data Structures & Algorithms, Database Management Systems, Machine Learning, Operating Systems.
"""
