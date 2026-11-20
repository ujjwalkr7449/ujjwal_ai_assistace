import os
from typing import Generator, List, Dict, Any

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

load_dotenv()

DEFAULT_MODEL = "openai/gpt-oss-120b"


def get_llm(
    api_key: str | None = None,
    model: str = DEFAULT_MODEL,
    streaming: bool = False,
    temperature: float = 0.2,
) -> ChatGroq:
    resolved_api_key = api_key or os.getenv("GROQ_API_KEY")
    if not resolved_api_key:
        raise RuntimeError("GROQ_API_KEY is not configured. Please check your .env or enter it in the sidebar.")

    return ChatGroq(
        model=model or DEFAULT_MODEL,
        api_key=resolved_api_key,
        temperature=temperature,
        streaming=streaming,
    )


def build_messages(
    system_prompt: str,
    question: str,
    chat_history: List[Dict[str, str]] | None = None,
) -> List[Any]:
    """Assemble LangChain messages including system prompt, previous conversation, and latest question."""
    messages: List[Any] = [SystemMessage(content=system_prompt)]

    # Add historical messages (excluding the current turn)
    if chat_history:
        for turn in chat_history:
            role = turn.get("role")
            content = turn.get("content", "")
            if role == "user":
                messages.append(HumanMessage(content=content))
            elif role == "assistant":
                messages.append(AIMessage(content=content))

    # Append current user question
    messages.append(HumanMessage(content=question))
    return messages


def stream_resume_chat(
    question: str,
    system_prompt: str,
    chat_history: List[Dict[str, str]] | None = None,
    api_key: str | None = None,
    model: str = DEFAULT_MODEL,
) -> Generator[str, None, None]:
    """Stream token-by-token response based on the system prompt and resume."""
    llm = get_llm(api_key=api_key, model=model, streaming=True)
    messages = build_messages(system_prompt, question, chat_history)

    for chunk in llm.stream(messages):
        if chunk.content:
            yield chunk.content


def answer_resume_chat(
    question: str,
    system_prompt: str,
    chat_history: List[Dict[str, str]] | None = None,
    api_key: str | None = None,
    model: str = DEFAULT_MODEL,
) -> str:
    """Non-streaming response generator based on the system prompt and resume."""
    llm = get_llm(api_key=api_key, model=model, streaming=False)
    messages = build_messages(system_prompt, question, chat_history)
    response = llm.invoke(messages)
    return response.content


# --------------------------------------------------------------------
# Backward compatibility helpers for document/RAG querying
# --------------------------------------------------------------------
def stream_answer(
    question: str,
    context: str,
    api_key: str | None = None,
    model: str = DEFAULT_MODEL,
) -> Generator[str, None, None]:
    sys_prompt = f"Answer the question using only the provided context:\n\n{context}"
    return stream_resume_chat(
        question=question,
        system_prompt=sys_prompt,
        chat_history=None,
        api_key=api_key,
        model=model,
    )


def answer_question(
    question: str,
    context: str,
    api_key: str | None = None,
    model: str = DEFAULT_MODEL,
) -> str:
    sys_prompt = f"Answer the question using only the provided context:\n\n{context}"
    return answer_resume_chat(
        question=question,
        system_prompt=sys_prompt,
        chat_history=None,
        api_key=api_key,
        model=model,
    )
