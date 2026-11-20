from pathlib import Path
import pymupdf

from app.resume_config import (
    CANDIDATE_NAME,
    PERSONA_MODE,
    SYSTEM_PROMPT,
    RESUME_FILE_PATH,
    RESUME_TEXT,
)


def load_resume_from_pdf(pdf_path: Path) -> str:
    """Extract text from a PDF file using PyMuPDF."""
    if not pdf_path.exists():
        raise FileNotFoundError(f"Resume PDF not found at {pdf_path}")

    doc = pymupdf.open(str(pdf_path))
    pages_text = []
    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text("text")
        if text.strip():
            pages_text.append(text.strip())

    if not pages_text:
        raise ValueError(f"No extractable text found in PDF: {pdf_path}")

    return "\n\n".join(pages_text)


def load_resume_from_txt(txt_path: Path) -> str:
    """Read raw text from a text file."""
    if not txt_path.exists():
        raise FileNotFoundError(f"Resume file not found at {txt_path}")
    return txt_path.read_text(encoding="utf-8")


def get_resume_data() -> dict:
    """
    Load resume text based on code configuration.
    Priority:
    1. Direct RESUME_TEXT string in app/resume_config.py (if provided and not empty).
    2. RESUME_FILE_PATH file (if exists, supports .pdf and .txt).
    3. Look for any *.pdf or *.txt in the 'data/' directory.
    """
    # 1. Direct text in code
    if RESUME_TEXT and RESUME_TEXT.strip():
        text = RESUME_TEXT.strip()
        return {
            "text": text,
            "source": "Configured in app/resume_config.py (RESUME_TEXT)",
            "char_count": len(text),
            "word_count": len(text.split()),
        }

    # 2. Configured file path
    project_root = Path(__file__).resolve().parent.parent
    configured_path = Path(RESUME_FILE_PATH)
    file_path = configured_path if configured_path.is_absolute() else project_root / configured_path
    if not file_path.exists() and configured_path == Path("data/resume.pdf"):
        app_data_path = project_root / "app" / "data" / "resume.pdf"
        if app_data_path.exists():
            file_path = app_data_path
    if file_path.exists() and file_path.is_file():
        suffix = file_path.suffix.lower()
        if suffix == ".pdf":
            text = load_resume_from_pdf(file_path)
        else:
            text = load_resume_from_txt(file_path)

        return {
            "text": text,
            "source": f"Local file: {file_path}",
            "char_count": len(text),
            "word_count": len(text.split()),
        }

    # 3. Check data/ directory for any resume file
    data_dir = project_root / "data"
    if data_dir.exists():
        for candidate in data_dir.glob("*"):
            if candidate.is_file() and candidate.suffix.lower() in [".pdf", ".txt", ".md"]:
                if candidate.suffix.lower() == ".pdf":
                    text = load_resume_from_pdf(candidate)
                else:
                    text = load_resume_from_txt(candidate)
                return {
                    "text": text,
                    "source": f"Found in data/: {candidate.name}",
                    "char_count": len(text),
                    "word_count": len(text.split()),
                }

    raise FileNotFoundError(
        f"Resume not found. Add a PDF or TXT file at {project_root / RESUME_FILE_PATH}."
    )


def format_system_prompt(
    candidate_name: str = CANDIDATE_NAME,
    persona_mode: str = PERSONA_MODE,
    custom_system_prompt: str | None = None,
    resume_content: str = "",
) -> str:
    """Format the system prompt with candidate name, persona rules, and resume text."""
    template = custom_system_prompt or SYSTEM_PROMPT

    if persona_mode == "first_person":
        persona_rule = (
            f"Speak in the first person ('I', 'me', 'my') as {candidate_name}. "
            f"Represent yourself confidently and professionally as if you are in an interview."
        )
    else:
        persona_rule = (
            f"Speak in the third person as an AI Assistant representing {candidate_name} "
            f"(e.g., '{candidate_name} is experienced in...', 'His/Her technical skills include...')."
        )

    formatted = template.format(
        candidate_name=candidate_name,
        persona_instruction=persona_rule,
        resume_content=resume_content,
    )
    return formatted
