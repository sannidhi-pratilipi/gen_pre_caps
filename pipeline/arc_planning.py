import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass, replace

from llm.tfy_client import complete
from prompts.arc_prompt import ALL_EMOTION_LABELS, build_blueprint_prompt

# Every precap chapter points at the same event chapter K. K must be above the last
# precap chapter and a chapter whose text was actually fetched (K <= chapter_count).

# The feeling a precap is built to land. Planned per chapter rather than left to
# generation, because "don't repeat the last one's emotion" is a constraint
# across chapters and Pass 2 only ever sees one. Anything outside this set is
# dropped to "" so a mis-spelled label cannot silently become the instruction.
EMOTIONS = ALL_EMOTION_LABELS

@dataclass
class ChapterMapping:
    """One row of the Pass 1 blueprint: the precap shown at the end of
    `chapter_number` is written about `scene_description`, the single event that
    lives in `target_chapter`.

    Every row shares ONE target and ONE `scene_description`. `limit` is how much
    of the event this particular precap may show, and is the field that changes
    from row to row."""

    chapter_number: int
    target_chapter: int
    scene_description: str
    bridge_reasoning: str
    limit: str = ""
    dominant_emotion: str = ""
    path: str = ""
    curiosity: str = ""

    @property
    def distance(self) -> int:
        """Chapters between this precap and the event. 1 means the reader
        arrives in the very next chapter."""
        return self.target_chapter - self.chapter_number


def _format_chapters_block(chapters: list[str]) -> str:
    body = "\n\n".join(f"Chapter {n}:\n{text}" for n, text in enumerate(chapters, start=1))
    return f"<chapters>\n{body}\n</chapters>"


class BlueprintParseError(ValueError):
    """Nothing usable came back from Pass 1. Carries the raw response so the
    caller can write it out — a planning call is expensive and the text is the
    only way to see what the model actually did."""

    def __init__(self, message: str, response: str):
        super().__init__(message)
        self.response = response


def _mapping_blocks(response: str) -> list[str]:
    """Every <mapping>...</mapping> block in the response, as raw text.

    Deliberately not a document parse. One mismatched tag anywhere in a
    twenty-mapping blueprint makes ElementTree reject the whole document, which
    costs every chapter its precap over a single malformed row. Slicing the
    blocks out first means a broken row costs only itself."""
    return re.findall(r"<mapping>.*?</mapping>", response, flags=re.DOTALL)


def _field(block: str, tag: str) -> str:
    """One field out of a mapping block, without parsing the block as XML.

    The fallback path for rows ElementTree refuses: an unescaped & or a stray
    tag inside prose is common in generated XML and does not make the field
    itself unreadable.

    The closing tag is not required to match the opening one. Generators get it
    wrong often enough (<chapter_id>4</target_chapter_id>) that insisting on a
    matching close silently drops a row whose content is perfectly good — and a
    dropped row reads downstream as a gap in the plan, which costs a whole
    re-planning call. Prefer the matching close where it exists; fall back to
    whatever close comes first."""
    match = re.search(rf"<{tag}>(.*?)</{tag}>", block, flags=re.DOTALL)
    if match is None:
        match = re.search(rf"<{tag}>(.*?)</\w+>", block, flags=re.DOTALL)
    return match.group(1).strip() if match else ""


def _text(el: ET.Element, tag: str) -> str:
    child = el.find(tag)
    if child is None or not child.text:
        return ""
    return child.text.strip()


def _optional_int(el: ET.Element, tag: str) -> int | None:
    value = _text(el, tag)
    return int(value) if value.isdigit() else None


def _call_metadata(stage: str, language: str | None, run_id: str | None = None) -> dict:
    metadata = {"stage": stage}
    if language:
        metadata["language"] = language
    if run_id:
        # Tags every call made on behalf of one series' run, so a blueprint call
        # and the precap calls that followed from it can be found together —
        # several series run concurrently and otherwise only differ by book_id.
        metadata["run_id"] = run_id
    return metadata


def _parse_blueprint(response: str) -> list[ChapterMapping]:
    blocks = _mapping_blocks(response)
    if not blocks:
        raise BlueprintParseError(
            "Response contained no <mapping> elements — Pass 1 returned nothing usable",
            response,
        )

    parsed: list[ChapterMapping] = []
    unreadable = 0
    for block in blocks:
        try:
            el = ET.fromstring(block)
            get = lambda tag: _text(el, tag)  # noqa: E731
        except ET.ParseError:
            # malformed row: read the fields out of the text instead of losing it
            unreadable += 1
            get = lambda tag: _field(block, tag)  # noqa: E731

        chapter_number = int(get("chapter_id")) if get("chapter_id").isdigit() else None
        target_chapter = (
            int(get("target_chapter_id")) if get("target_chapter_id").isdigit() else None
        )
        scene_description = get("scene_description")
        if chapter_number is None or target_chapter is None or not scene_description:
            continue
        emotion = get("dominant_emotion").upper()
        parsed.append(
            ChapterMapping(
                chapter_number=chapter_number,
                target_chapter=target_chapter,
                scene_description=scene_description,
                bridge_reasoning=get("bridge_reasoning"),
                # <reveal> is what this field was called before it was renamed.
                # Blueprints written then are still on disk and still worth
                # reusing, and a row read without its limit is worse than a
                # stale tag name: the precap is written with no ceiling at all.
                limit=get("limit") or get("reveal"),
                dominant_emotion=emotion if emotion in EMOTIONS else "",
                path=get("path"),
                curiosity=get("curiosity"),
            )
        )

    if unreadable:
        print(
            f"[blueprint] {unreadable} of {len(blocks)} mappings were not valid XML — "
            "their fields were read out of the text instead"
        )
    if not parsed:
        print(
            f"[blueprint] none of the {len(blocks)} mappings had a usable chapter_id, "
            "target_chapter_id and scene_description"
        )
    return parsed


_INDIC = "\u0900-\u0d7f"  # Devanagari through Malayalam: names are copied in the story's own script
_NOT_A_NAME = {
    "The", "A", "An", "In", "On", "At", "He", "She", "They", "His", "Her", "Their", "It",
    "Then", "When", "While", "After", "Before", "As", "And", "But", "With", "Into", "From",
}


def _scene_names(scene: str) -> list[str]:
    """The proper nouns in a scene_description. The planner writes everything in
    English except names, which it copies in the chapters' own script, so those
    script tokens are the names. For an English story, fall back to capitalised
    words that are not common sentence openers."""
    tokens = [re.sub(r"['’]s$", "", t) for t in re.split(rf"[^\w{_INDIC}]+", scene) if t]
    script = [t for t in tokens if re.search(f"[{_INDIC}]", t)]
    if script:
        return list(dict.fromkeys(script))
    return list(dict.fromkeys(t for t in tokens if t[:1].isupper() and t not in _NOT_A_NAME))


def _appears(name: str, text: str) -> bool:
    boundary = rf"(?<![\w{_INDIC}]){re.escape(name)}(?![\w{_INDIC}])"
    return re.search(boundary, text, flags=re.IGNORECASE if name.isascii() else 0) is not None


def enforce_constraints(
    mappings: list[ChapterMapping],
    chapter_count: int,
    precap_limit: int | None = None,
    chapters: list[str] | None = None,
) -> tuple[list[ChapterMapping], list[tuple[int, str]]]:
    """The rules in the Pass 1 prompt can be violated by the model, so re-check
    every mapping here rather than trusting the response.

    Every chapter must point at the SAME event chapter: the first target a row
    names. That target must be ahead of its own chapter, past `precap_limit` (an
    event inside the chapters that get precaps is no event to promise) and a
    chapter whose text was fetched (<= chapter_count). A row that breaks one of
    these is rejected, not repaired, because its scene_description describes a
    scene in the target it named. A row whose scene_description differs from the
    first row's is repaired, since the whole run shares one target chapter and
    one scene.

    With `chapters` given, the event must also be about someone the reader has met:
    at least one name in its scene_description has to appear in chapters 1..precap_limit.
    If none does, the chapters after them are probably a different story (an
    anthology), and every row is rejected rather than teased.

    Returns the surviving mappings plus (chapter_number, reason) for each
    rejection, so the caller can report what was dropped instead of silently
    shipping fewer precaps than expected."""
    if precap_limit is None:
        precap_limit = chapter_count - 1
    precap_limit = min(precap_limit, chapter_count - 1)

    kept: list[ChapterMapping] = []
    rejected: list[tuple[int, str]] = []

    by_chapter: dict[int, ChapterMapping] = {}
    for mapping in sorted(mappings, key=lambda m: m.chapter_number):
        n = mapping.chapter_number
        if not 1 <= n <= precap_limit:
            rejected.append((n, f"source chapter out of range 1..{precap_limit}"))
        elif n in by_chapter:
            rejected.append((n, "duplicate mapping for this chapter"))
        else:
            by_chapter[n] = mapping

    event_chapter: int | None = None
    event_scene = ""
    drifted: list[tuple[int, str, str]] = []
    precap_text = "\n".join((chapters or [])[:precap_limit])

    for n in range(1, precap_limit + 1):
        mapping = by_chapter.get(n)
        if mapping is None:
            continue

        k = mapping.target_chapter
        if k <= n:
            rejected.append((n, f"target {k} is not ahead of chapter {n}"))
            continue
        if k > chapter_count:
            rejected.append(
                (n, f"target {k} is past the last chapter fetched ({chapter_count})")
            )
            continue
        if k <= precap_limit:
            rejected.append(
                (n, f"target {k} is inside the chapters that get precaps (1..{precap_limit})")
            )
            continue
        if event_chapter is not None and k != event_chapter:
            rejected.append((n, f"target {k} is not the event's chapter ({event_chapter})"))
            continue

        if event_chapter is None:
            names = _scene_names(mapping.scene_description) if chapters else []
            if names and not any(_appears(name, precap_text) for name in names):
                reason = (
                    f"none of the event's characters ({', '.join(names)}) appear in chapters "
                    f"1..{precap_limit} — chapter {k} looks like a different story"
                )
                rejected.extend((m, reason) for m in sorted(by_chapter) if m >= n)
                break
            event_chapter = k
            event_scene = mapping.scene_description
        elif mapping.scene_description != event_scene:
            drifted.append((n, event_scene, mapping.scene_description))
            mapping = replace(mapping, scene_description=event_scene)
        kept.append(mapping)

    repeated = [
        (b.chapter_number, b.dominant_emotion)
        for a, b in zip(kept, kept[1:])
        if a.dominant_emotion and a.dominant_emotion == b.dominant_emotion
        and a.chapter_number + 1 == b.chapter_number
    ]
    for n, emotion in repeated:
        print(
            f"[blueprint] chapter {n}: dominant emotion {emotion} repeats the chapter before it "
            "— consecutive precaps will land the same feeling"
        )

    for n, expected, got in drifted:
        print(
            f"[blueprint] chapter {n}: scene drifted from the event's scene — "
            f"snapped back.\n    event scene: {expected}\n    returned:   {got}"
        )

    return kept, rejected


def blueprint_from_xml(
    response: str,
    chapter_count: int,
    precap_limit: int | None = None,
    chapters: list[str] | None = None,
) -> tuple[list[ChapterMapping], list[tuple[int, str]]]:
    """Turn a blueprint XML into mappings, without calling the planner.

    The same parse and constraint check Pass 1 runs on a fresh response, split
    out so a blueprint already sitting on disk can be reused. The constraints
    are re-checked rather than trusted: a stored blueprint may have been written
    against a different chapter count, or edited by hand.

    Raises BlueprintParseError if the XML holds no usable mappings, so a
    truncated or half-written file falls back to a real planning call instead of
    silently producing no precaps."""
    kept, rejected = enforce_constraints(
        _parse_blueprint(response), chapter_count, precap_limit, chapters
    )
    _report_blueprint(kept)
    return kept, rejected


def plan_precaps(
    chapters: list[str],
    language: str | None = None,
    precap_limit: int | None = None,
    run_id: str | None = None,
    genre: str | None = None,
) -> tuple[list[ChapterMapping], list[tuple[int, str]], str]:
    """Pass 1: one LLM call over the full chapter text (no summarization step —
    the planner reads the chapters themselves) that picks one event from the
    chapters after `precap_limit` and maps every precap chapter to it, one new
    beat each.

    `genre` swaps out the peak-event vocabulary in the prompt (see
    prompts/genre/<genre>/arc_planner.py).

    Returns the kept mappings, the rejections, and the planner's raw response
    so the caller can persist the blueprint XML alongside the hooks."""
    chapter_count = len(chapters)
    if precap_limit is None:
        precap_limit = chapter_count - 1
    precap_limit = min(precap_limit, chapter_count - 1)

    messages = [
        {
            "role": "system",
            "content": build_blueprint_prompt(precap_limit, chapter_count, genre),
        },
        {"role": "user", "content": _format_chapters_block(chapters)},
    ]
    response = complete(
        messages, metadata=_call_metadata("precap_blueprint", language, run_id)
    )
    kept, rejected = blueprint_from_xml(response, chapter_count, precap_limit, chapters)
    return kept, rejected, response


def _report_blueprint(kept: list[ChapterMapping]) -> None:
    """How far ahead the event sits. Advisory — nothing here rejects a mapping."""
    if kept:
        print(f"[blueprint] event in chapter {kept[0].target_chapter}, {len(kept)} precaps")
