import xml.etree.ElementTree as ET
from dataclasses import dataclass, replace

from llm.tfy_client import complete
from prompts.arc_prompt import build_blueprint_prompt

# At most this many chapters may aim at one target chapter.
MAX_TARGET_REUSE = 3

# How far ahead of chapter N a precap is allowed to reach: the target chapter K
# must satisfy N < K <= N + LOOKAHEAD.
#
# This equals MAX_TARGET_REUSE, and not by coincidence. Under the sticky-anchor
# rule a run anchored on K and starting at chapter A covers chapters A..K-1, so
# the run's length IS the first chapter's distance. A lookahead wider than the
# reuse cap could only ever produce runs that the cap then rejects.
LOOKAHEAD = MAX_TARGET_REUSE

# The feeling a precap is built to land. Planned per chapter rather than left to
# generation, because "don't repeat the last one's emotion" is a constraint
# across chapters and Pass 2 only ever sees one. Anything outside this set is
# dropped to "" so a mis-spelled label cannot silently become the instruction.
EMOTIONS = {
    "IDENTITY", "FEAR", "REVENGE", "HOPE", "BETRAYAL", "SACRIFICE",
    "LOVE", "MYSTERY", "GUILT", "GRIEF", "SHAME", "LOYALTY", "PRIDE", "DESPERATION",
}


@dataclass
class ChapterMapping:
    """One row of the Pass 1 blueprint: the precap shown at the end of
    `chapter_number` is written about `scene_description`, a scene that lives in
    `target_chapter`.

    Every chapter in an anchor run shares ONE `scene_description` — the run does
    not tease a different moment each time, it peels back the same moment layer
    by layer. `reveal` is what this particular precap is allowed to expose about
    it, and is the only field that changes down the run."""

    chapter_number: int
    target_chapter: int
    scene_description: str
    bridge_reasoning: str
    reveal: str = ""
    dominant_emotion: str = ""

    @property
    def distance(self) -> int:
        """Chapters between this precap and the scene it reaches for. 1 means
        the reader arrives in the very next chapter.

        A run counts down to its anchor (1->5, 2->5, 3->5, 4->5), so this is
        also the precap's position in its run: distance - 1 is exactly how many
        more precaps still reach for the same scene."""
        return self.target_chapter - self.chapter_number


def _format_chapters_block(chapters: list[str]) -> str:
    body = "\n\n".join(f"Chapter {n}:\n{text}" for n, text in enumerate(chapters, start=1))
    return f"<chapters>\n{body}\n</chapters>"


def _extract_root(response: str, tag: str) -> ET.Element:
    start = response.find(f"<{tag}")
    close_tag = f"</{tag}>"
    end = response.rfind(close_tag)
    if start == -1 or end == -1:
        raise ValueError(f"Response did not contain a <{tag}> root element:\n{response}")
    return ET.fromstring(response[start : end + len(close_tag)])


def _text(el: ET.Element, tag: str) -> str:
    child = el.find(tag)
    if child is None or not child.text:
        return ""
    return child.text.strip()


def _optional_int(el: ET.Element, tag: str) -> int | None:
    value = _text(el, tag)
    return int(value) if value.isdigit() else None


def _call_metadata(stage: str, language: str | None) -> dict:
    metadata = {"stage": stage}
    if language:
        metadata["language"] = language
    return metadata


def _parse_turning_points(root: ET.Element) -> list[int]:
    """The chapters the planner itself called the story's peaks. Parsed so the
    blueprint can be checked against them: an anchor staircase that drifts past
    a peak is the failure that makes precaps tease filler, and it is invisible
    unless the planner is made to name the peaks up front."""
    container = root.find("turning_points")
    if container is None:
        return []
    return sorted(
        int(c.text.strip())
        for c in container.findall("chapter")
        if c.text and c.text.strip().isdigit()
    )


def _parse_blueprint(response: str) -> list[ChapterMapping]:
    root = _extract_root(response, "blueprint")
    parsed: list[ChapterMapping] = []
    for el in root.findall("mapping"):
        chapter_number = _optional_int(el, "chapter_id")
        target_chapter = _optional_int(el, "target_chapter_id")
        scene_description = _text(el, "scene_description")
        if chapter_number is None or target_chapter is None or not scene_description:
            continue
        emotion = _text(el, "dominant_emotion").upper()
        parsed.append(
            ChapterMapping(
                chapter_number=chapter_number,
                target_chapter=target_chapter,
                scene_description=scene_description,
                bridge_reasoning=_text(el, "bridge_reasoning"),
                reveal=_text(el, "reveal"),
                dominant_emotion=emotion if emotion in EMOTIONS else "",
            )
        )
    return parsed


def enforce_constraints(
    mappings: list[ChapterMapping],
    chapter_count: int,
    lookahead: int = LOOKAHEAD,
    precap_limit: int | None = None,
    max_target_reuse: int = MAX_TARGET_REUSE,
) -> tuple[list[ChapterMapping], list[tuple[int, str]]]:
    """The window, anchor and monotonicity rules are instructions in the Pass 1
    prompt, so the model can violate them. Re-check every mapping here rather
    than trusting the response.

    The load-bearing rule is the ANCHOR: once chapter A points at chapter K,
    every chapter from A up to K-1 must keep pointing at K, and the horizon is
    only free to move once the reader has actually reached K. Letting chapter A
    promise chapter 5 and chapter A+1 silently jump to chapter 7 abandons a
    promise the reader is still holding, which reads as the story dropping its
    own setup. Enforcing it here rather than only in the prompt means a single
    stray target cannot desync the whole run behind it.

    A mapping is rejected — not repaired — when it breaks a rule: its
    scene_description describes a scene in the target chapter it named, so
    rewriting the target to a legal value would leave the scene pointing at the
    wrong chapter. A rejected chapter gets no precap, and critically does not
    release the anchor, so the chapters after it stay locked on the same
    promise.

    Returns the surviving mappings plus (chapter_number, reason) for each
    rejection, so the caller can report what was dropped instead of silently
    shipping fewer precaps than expected."""
    # Chapters past precap_limit are fetched only to be aimed at, so they are
    # not valid sources. Defaulting to chapter_count - 1 keeps the plain
    # "plan everything that has a chapter after it" behaviour.
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

    anchor: int | None = None
    anchor_scene = ""
    floor = 0
    uses_of_target: dict[int, int] = {}
    drifted: list[tuple[int, str, str]] = []

    # Walk chapters rather than mappings: a chapter with no surviving mapping
    # still has to advance the run, or the anchor would outlive its payoff.
    for n in range(1, precap_limit + 1):
        if anchor is not None and n >= anchor:
            anchor = None  # the reader has reached it; the horizon is free again

        mapping = by_chapter.get(n)
        if mapping is None:
            continue

        k = mapping.target_chapter
        if k <= n:
            reason = f"target {k} is not ahead of chapter {n}"
        elif k > n + lookahead:
            reason = f"target {k} is beyond the {lookahead}-chapter lookahead window"
        elif k > chapter_count:
            reason = f"target {k} is past the last chapter fetched ({chapter_count})"
        elif anchor is not None and k != anchor:
            reason = (
                f"jumps to {k} while chapter {anchor} is still promised and unreached — "
                f"the anchor holds until chapter {anchor}"
            )
        elif k < floor:
            reason = f"target {k} moves backward from the previous target ({floor})"
        elif uses_of_target.get(k, 0) >= max_target_reuse:
            # counted over kept mappings rather than inferred from the distance,
            # so a run that lost a chapter to an earlier rejection still cannot
            # quietly grow past the cap
            reason = (
                f"target {k} is already used by {max_target_reuse} chapters, the most allowed"
            )
        else:
            if anchor is None:
                anchor = k
                anchor_scene = mapping.scene_description
            elif mapping.scene_description != anchor_scene:
                # A run peels back ONE scene, so every chapter in it must name
                # the same one. Unlike a bad target this is safe to repair: the
                # whole run shares a target chapter, so the anchor's scene is
                # valid for every chapter in it. Repair rather than reject, and
                # say so, because dropping the row would cost a precap over a
                # difference Pass 2 cannot even see.
                drifted.append((n, anchor_scene, mapping.scene_description))
                mapping = replace(mapping, scene_description=anchor_scene)
            floor = k
            uses_of_target[k] = uses_of_target.get(k, 0) + 1
            kept.append(mapping)
            continue

        rejected.append((n, reason))

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

    if drifted:
        for n, expected, got in drifted:
            print(
                f"[blueprint] chapter {n}: scene drifted from the run's anchor scene — "
                f"snapped back.\n    run scene: {expected}\n    returned:  {got}"
            )

    return kept, rejected


def plan_precaps(
    chapters: list[str],
    language: str | None = None,
    lookahead: int = LOOKAHEAD,
    precap_limit: int | None = None,
    max_target_reuse: int = MAX_TARGET_REUSE,
) -> tuple[list[ChapterMapping], list[tuple[int, str]], str]:
    """Pass 1: one LLM call over the full chapter text (no summarization step —
    the planner reads the chapters themselves) that maps every chapter N to a
    look-ahead target chapter K and the scene inside K to tease.

    Because the whole blueprint comes back in a single response, the planner
    sees every chapter at once and can pace the targets and the emotions across
    the series — neither of which a per-chapter call could do.

    Returns the kept mappings, the rejections, and the planner's raw response
    so the caller can persist the blueprint XML alongside the hooks."""
    chapter_count = len(chapters)
    if precap_limit is None:
        precap_limit = chapter_count - 1
    precap_limit = min(precap_limit, chapter_count - 1)

    messages = [
        {
            "role": "system",
            "content": build_blueprint_prompt(
                lookahead, precap_limit, chapter_count, max_target_reuse
            ),
        },
        {"role": "user", "content": _format_chapters_block(chapters)},
    ]
    response = complete(messages, metadata=_call_metadata("precap_blueprint", language))
    kept, rejected = enforce_constraints(
        _parse_blueprint(response), chapter_count, lookahead, precap_limit, max_target_reuse
    )

    peaks = _parse_turning_points(_extract_root(response, "blueprint"))
    if peaks:
        targeted = {m.target_chapter for m in kept}
        missed = [p for p in peaks if p not in targeted]
        # how much of the blueprint is actually spent on the story's peaks —
        # the number worth watching, since a peak given a one-chapter run is a
        # peak mostly wasted
        on_peak = sum(1 for m in kept if m.target_chapter in peaks)
        share = round(100 * on_peak / len(kept)) if kept else 0
        print(
            f"[blueprint] turning points {peaks}: {on_peak}/{len(kept)} precaps "
            f"aim at one ({share}%)"
        )
        if missed:
            print(
                f"[blueprint] never aimed at {missed} — those precaps tease filler "
                "instead of the peak"
            )

    return kept, rejected, response
