from llm.tfy_client import complete
from pipeline.arc_planning import ChapterMapping
from prompts.critique_prompt import build_critique_prompt
from prompts.hook_prompt import build_bridge_context, build_hook_prompt


def _chapter_content(
    chapter_read_text: str,
    target_chapter_text: str,
    mapping: ChapterMapping,
    bridge_context: str,
) -> str:
    return (
        f"CHAPTER JUST READ (chapter {mapping.chapter_number}):\n{chapter_read_text}\n\n"
        f"TARGET CHAPTER (chapter {mapping.target_chapter}, contains the target scene):\n"
        f"{target_chapter_text}"
        f"{bridge_context}"
    )


def generate_hook(
    chapter_read_text: str,
    target_chapter_text: str,
    mapping: ChapterMapping,
    metadata: dict | None = None,
    language: str | None = None,
    previous_reveal: str | None = None,
    same_scene_precaps: list[str] | None = None,
    previous_precap: str | None = None,
) -> str:
    bridge_context = build_bridge_context(mapping, previous_reveal, same_scene_precaps, previous_precap)
    messages = [
        {"role": "system", "content": build_hook_prompt(language)},
        {
            "role": "user",
            "content": _chapter_content(chapter_read_text, target_chapter_text, mapping, bridge_context),
        },
    ]
    return complete(messages, metadata=metadata)


def critique_hook(
    hook: str,
    chapter_read_text: str,
    target_chapter_text: str,
    mapping: ChapterMapping,
    metadata: dict | None = None,
    language: str | None = None,
) -> tuple[bool, str]:
    # the predecessor inputs are deliberately not passed here — no
    # critique criterion checks either (only generation uses them, to steer away
    # from the previous precap), so sending them would just be inert context.
    bridge_context = build_bridge_context(mapping)
    content = _chapter_content(chapter_read_text, target_chapter_text, mapping, bridge_context)
    messages = [
        {"role": "system", "content": build_critique_prompt(language)},
        {"role": "user", "content": f"{content}\n\nHook to evaluate:\n{hook}"},
    ]
    response = complete(messages, metadata=metadata)

    passes = "VERDICT: PASS" in response.upper()
    reason = ""
    for line in response.splitlines():
        if line.upper().startswith("REASON:"):
            reason = line.split(":", 1)[1].strip()
            break
    return passes, reason


def rewrite_hook(
    hook: str,
    critique: str,
    chapter_read_text: str,
    target_chapter_text: str,
    mapping: ChapterMapping,
    metadata: dict | None = None,
    language: str | None = None,
    previous_reveal: str | None = None,
    same_scene_precaps: list[str] | None = None,
    previous_precap: str | None = None,
) -> str:
    bridge_context = build_bridge_context(mapping, previous_reveal, same_scene_precaps, previous_precap)
    messages = [
        {"role": "system", "content": build_hook_prompt(language)},
        {
            "role": "user",
            "content": _chapter_content(chapter_read_text, target_chapter_text, mapping, bridge_context),
        },
        {"role": "assistant", "content": hook},
        {
            "role": "user",
            "content": (
                f"This hook was rejected for the following reason:\n{critique}\n\n"
                "Rewrite it to fix the issue while keeping all other qualities intact."
            ),
        },
    ]
    return complete(messages, metadata=metadata)
