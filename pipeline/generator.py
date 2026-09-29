from llm.tfy_client import complete
from pipeline.arc_planning import ChapterMapping
from prompts.critique_prompt import build_critique_prompt, build_predecessor_block
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
    recent_precaps: list[str] | None = None,
) -> str:
    bridge_context = build_bridge_context(mapping, previous_reveal, same_scene_precaps, recent_precaps)
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
    same_scene_precaps: list[str] | None = None,
    recent_precaps: list[str] | None = None,
) -> tuple[bool, str]:
    # The predecessors go in as their own block rather than through
    # build_bridge_context: that one is written at the hook's author ("yours must
    # go past all of these"), which is the wrong voice for an editor. They are
    # sent at all only because repetition is the single failure that cannot be
    # judged from the hook and the chapters alone.
    bridge_context = build_bridge_context(mapping)
    predecessors = build_predecessor_block(same_scene_precaps, recent_precaps)
    content = _chapter_content(chapter_read_text, target_chapter_text, mapping, bridge_context)
    messages = [
        {
            "role": "system",
            "content": build_critique_prompt(language, has_predecessors=bool(predecessors)),
        },
        {"role": "user", "content": f"{content}{predecessors}\n\nHook to evaluate:\n{hook}"},
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
    recent_precaps: list[str] | None = None,
) -> str:
    bridge_context = build_bridge_context(mapping, previous_reveal, same_scene_precaps, recent_precaps)
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
