"""
Resume & Chatbot Configuration Module.
Configure your personal details, resume text, or resume file here directly in code.
"""

from pathlib import Path

# -------------------------------------------------------------
# 1. Candidate Identity & Persona
# -------------------------------------------------------------
CANDIDATE_NAME = "Ujjwal Kumar"

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
1. Ground every factual answer strictly on the resume excerpts provided below.
2. Maintain a professional, polite, enthusiastic, and confident tone.
3. {persona_instruction}
4. Describe documented project details and technologies; do not claim an impact unless the resume states one.
5. If a detail is missing from the excerpts, say it is not specified in the resume. Do not infer contact details, dates, employers, URLs, or achievements.
6. Use the exact URLs in the PROFILE LINKS section when asked for GitHub, LinkedIn, or Portfolio. Never invent or alter a URL.
7. Never make up qualifications, work experience, or project results.
8. Keep responses concise and professional. You may answer naturally in first person, but do not claim facts absent from the excerpts.

--- RESUME EXCERPTS START ---
{resume_content}
--- RESUME EXCERPTS END ---
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
RESUME_FILE_PATH = Path("data/resume.pdf")

# Verified profile URLs supplied by Ujjwal.
PROFILE_LINKS = {
    "LinkedIn": "https://www.linkedin.com/in/ujjwalllkumar/",
    "GitHub": "https://github.com/ujjwalkr7449",
    "Portfolio": "https://ujjwalllkumar.netlify.app/",
}

# Direct Raw Text Resume:
# If you paste your resume text here, it will be used directly without needing any PDF file!
# Leave as empty string "" if you prefer to use the PDF file specified in RESUME_FILE_PATH.
RESUME_TEXT = ""
