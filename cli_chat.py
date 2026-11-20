"""
CLI & Script Interface for Personal Resume Chatbot.
Use this to query your resume chatbot directly from terminal or import into other Python scripts.

Usage:
  Interactive Mode:
    python cli_chat.py

  Single Question Mode:
    python cli_chat.py "What are your top technical skills?"
"""

import sys
from dotenv import load_dotenv

from app.resume_config import CANDIDATE_NAME, PERSONA_MODE, SYSTEM_PROMPT
from app.resume_loader import get_resume_data, format_system_prompt
from app.qa import stream_resume_chat, DEFAULT_MODEL

load_dotenv()


def main():
    print("=" * 60)
    print(f"🤖 {CANDIDATE_NAME}'s AI Career Assistant (CLI Mode)")
    print("=" * 60)

    # 1. Load resume data from code configuration
    resume_info = get_resume_data()
    print(f"📄 Resume Source: {resume_info['source']}")
    print(f"📊 Words: {resume_info['word_count']} | Characters: {resume_info['char_count']}")
    print(f"🎭 Persona: {PERSONA_MODE}")
    print("=" * 60)

    # 2. Build system prompt
    formatted_prompt = format_system_prompt(
        candidate_name=CANDIDATE_NAME,
        persona_mode=PERSONA_MODE,
        custom_system_prompt=SYSTEM_PROMPT,
        resume_content=resume_info["text"],
    )

    history = []

    # Check if a question was passed as command line arguments
    if len(sys.argv) > 1:
        question = " ".join(sys.argv[1:])
        print(f"\n❓ Question: {question}\n")
        print("💡 Answer: ", end="", flush=True)
        full_ans = []
        for chunk in stream_resume_chat(question, formatted_prompt, chat_history=[]):
            print(chunk, end="", flush=True)
            full_ans.append(chunk)
        print("\n")
        return

    # Interactive Loop
    print("Ask any question about your resume! (Type 'exit' or 'quit' to stop)\n")
    while True:
        try:
            user_input = input("You > ").strip()
            if not user_input:
                continue
            if user_input.lower() in ["exit", "quit", "q"]:
                print("Goodbye!")
                break

            print("\nAI > ", end="", flush=True)
            answer_parts = []
            for chunk in stream_resume_chat(
                question=user_input,
                system_prompt=formatted_prompt,
                chat_history=history,
            ):
                print(chunk, end="", flush=True)
                answer_parts.append(chunk)
            print("\n")

            # Update conversation history
            complete_answer = "".join(answer_parts)
            history.append({"role": "user", "content": user_input})
            history.append({"role": "assistant", "content": complete_answer})

        except KeyboardInterrupt:
            print("\nSession interrupted. Exiting.")
            break
        except Exception as exc:
            print(f"\n[Error]: {exc}\n")


if __name__ == "__main__":
    main()
