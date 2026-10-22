from pipeline.arc_planning import ChapterMapping
from pipeline.generator import critique_hook, generate_hook, rewrite_hook
from pipeline.validators import find_foreign_script_chars

MAX_ITERATIONS = 3


def process_chapter(
    book_id: str,
    chapter_read_text: str,
    target_chapter_text: str,
    mapping: ChapterMapping,
    language: str | None = None,
    previous_limit: str | None = None,
    same_scene_precaps: list[str] | None = None,
    recent_precaps: list[str] | None = None,
    run_id: str | None = None,
    genre: str | None = None,
) -> str:
    print(
        f"Generating precap for {book_id} "
        f"(chapter {mapping.chapter_number} -> chapter {mapping.target_chapter})..."
    )

    metadata: dict = {"book_id": book_id.split("_")[0]}
    if "_chapter_" in book_id:
        metadata["chapter_number"] = book_id.split("_chapter_")[-1]
    if run_id:
        # Carried on the generate, critique and rewrite calls alike, so all the
        # traffic for one chapter of one run groups under a single id.
        metadata["run_id"] = run_id

    hook = generate_hook(
        chapter_read_text,
        target_chapter_text,
        mapping,
        metadata=metadata,
        language=language,
        previous_limit=previous_limit,
        same_scene_precaps=same_scene_precaps,
        recent_precaps=recent_precaps,
        genre=genre,
    )

    for attempt in range(1, MAX_ITERATIONS + 1):
        bad_chars = find_foreign_script_chars(hook, language)
        if bad_chars:
            passes = False
            reason = (
                "Hook contains characters from a different script spliced into "
                f"the words: {', '.join(sorted(set(bad_chars)))}. Rewrite entirely "
                "in the target language's own script — do not mix in glyphs from "
                "another script."
            )
        else:
            passes, reason = critique_hook(
                hook,
                chapter_read_text,
                target_chapter_text,
                mapping,
                metadata=metadata,
                language=language,
                same_scene_precaps=same_scene_precaps,
                recent_precaps=recent_precaps,
            )
        if passes:
            break
        print(
            f"[{book_id}] Critique failed (attempt {attempt}/{MAX_ITERATIONS}) — {reason}. Rewriting..."
        )
        rewritten = rewrite_hook(
            hook,
            reason,
            chapter_read_text,
            target_chapter_text,
            mapping,
            metadata=metadata,
            language=language,
            previous_limit=previous_limit,
            same_scene_precaps=same_scene_precaps,
            recent_precaps=recent_precaps,
            genre=genre,
        )

        # Never let a blank rewrite replace a usable hook.
        if not rewritten.strip():
            print(f"[{book_id}] Rewrite came back empty — keeping previous hook")
            break
        hook = rewritten

    return hook
