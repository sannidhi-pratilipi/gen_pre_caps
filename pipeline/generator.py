from llm.tfy_client import complete
from prompts.hook_prompt import build_hook_prompt
from prompts.critique_prompt import build_critique_prompt


def _chapter_content(previous_chapter_text: str, current_chapter_text: str) -> str:
    return (
        f"Chapter just read:\n{previous_chapter_text}\n\n"
        f"This chapter (write the hook for this):\n{current_chapter_text}"
    )


def generate_hook(previous_chapter_text: str, current_chapter_text: str, metadata: dict | None = None, language: str | None = None) -> str:
    messages = [
        {"role": "system", "content": build_hook_prompt(language)},
        {"role": "user", "content": _chapter_content(previous_chapter_text, current_chapter_text)},
    ]
    return complete(messages, metadata=metadata)


def critique_hook(hook: str, previous_chapter_text: str, current_chapter_text: str, metadata: dict | None = None, language: str | None = None) -> tuple[bool, str]:
    content = _chapter_content(previous_chapter_text, current_chapter_text)
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


def rewrite_hook(hook: str, critique: str, previous_chapter_text: str, current_chapter_text: str, metadata: dict | None = None, language: str | None = None) -> str:
    messages = [
        {"role": "system", "content": build_hook_prompt(language)},
        {"role": "user", "content": _chapter_content(previous_chapter_text, current_chapter_text)},
        {"role": "assistant", "content": hook},
        {"role": "user", "content": f"This hook was rejected for the following reason:\n{critique}\n\nRewrite it to fix the issue while keeping all other qualities intact."},
    ]
    return complete(messages, metadata=metadata)
