from functools import lru_cache
import re

def retrieve_context(
    document_id: str,
    question: str,
    k: int = 4,
):
    from app.vector_store import load_vector_store

    store = load_vector_store(document_id)

    results = store.similarity_search(
        question,
        k=k,
    )

    context = "\n\n".join(
        result.page_content for result in results
    )

    sources = [
        {
            **result.metadata,
            "snippet": result.page_content[:300].strip() + ("..." if len(result.page_content) > 300 else ""),
        }
        for result in results
    ]

    return context, sources


_STOP_WORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "can", "describe",
    "did", "do", "for", "from", "give", "have", "how", "i", "in", "is",
    "it", "me", "my", "of", "on", "or", "please", "tell", "that", "the",
    "their", "them", "there", "this", "to", "what", "when", "where", "which",
    "who", "why", "with", "you", "your",
}


@lru_cache(maxsize=2)
def _resume_chunks(resume_text: str) -> tuple[str, ...]:
    """Split the short resume into cached, readable passages without model loading."""
    chunks: list[str] = []
    current: list[str] = []
    current_length = 0
    for line in resume_text.splitlines():
        line = line.strip()
        if not line:
            continue
        # Keep unusually long lines bounded while preserving their full text.
        lines = [line[i:i + 700] for i in range(0, len(line), 700)]
        for part in lines:
            if current and current_length + len(part) > 700:
                chunks.append("\n".join(current))
                current, current_length = [], 0
            current.append(part)
            current_length += len(part)
    if current:
        chunks.append("\n".join(current))
    return tuple(chunks)


def retrieve_resume_context(resume_text: str, question: str, k: int = 4) -> str:
    """Return relevant resume passages using fast, dependency-free term search."""
    query_terms = {
        term for term in re.findall(r"[a-z0-9+#.]+", question.lower())
        if len(term) > 1 and term not in _STOP_WORDS
    }
    chunks = _resume_chunks(resume_text)
    if not query_terms:
        return "\n\n".join(chunks[:k])

    ranked = []
    for index, chunk in enumerate(chunks):
        chunk_terms = set(re.findall(r"[a-z0-9+#.]+", chunk.lower()))
        overlap = query_terms & chunk_terms
        if overlap:
            # Reward coverage of the question; prefer focused passages on ties.
            score = len(overlap) / len(query_terms) + len(overlap) / max(len(chunk_terms), 1)
            ranked.append((score, index, chunk))
    ranked.sort(key=lambda item: (-item[0], item[1]))
    selected = [item[2] for item in ranked[:k]]
    return "\n\n".join(selected or chunks[:min(k, 2)])
