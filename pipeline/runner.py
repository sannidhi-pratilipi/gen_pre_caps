from pipeline.generator import critique_hook, generate_hook, rewrite_hook

MAX_ITERATIONS = 3


def process_chapter(
    book_id: str, previous_chapter_text: str, current_chapter_text: str, language: str | None = None
) -> str:
    print(f"Generating hook for {book_id}...")

    metadata: dict = {"book_id": book_id.split("_")[0]}
    if "_chapter_" in book_id:
        metadata["chapter_number"] = book_id.split("_chapter_")[-1]

    hook = generate_hook(previous_chapter_text, current_chapter_text, metadata=metadata, language=language)

    for attempt in range(1, MAX_ITERATIONS + 1):
        passes, reason = critique_hook(
            hook, previous_chapter_text, current_chapter_text, metadata=metadata, language=language
        )
        if passes:
            break
        print(
            f"[{book_id}] Critique failed (attempt {attempt}/{MAX_ITERATIONS}) — {reason}. Rewriting..."
        )
        hook = rewrite_hook(hook, reason, previous_chapter_text, current_chapter_text, metadata=metadata, language=language)

    return hook
