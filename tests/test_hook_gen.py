import argparse
import re
import uuid
from collections import deque
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from itertools import islice
from pathlib import Path

from ingestion.ingest_chapter import ChapterIngestor
from main import CHAPTER_LIMIT, NEAR_CHAPTER_LIMIT, PRECAP_LIMIT, is_non_story_opener
from pipeline.arc_planning import (
    BlueprintParseError,
    blueprint_from_xml,
    plan_precaps,
)
from pipeline.runner import process_chapter

# SERIES_SLUGS = ["vnustigw45xt", "loydb6s7xqa5", "rv5i7wqoclxs"]
SERIES_SLUGS=["nxiarydspru9", "rzmjlonhei4x", "5mtf05kjz1l8", "mukeivhakxuw", "w2iz3pb0tait", "ngixsk2ufcva", "ulknumcucepz"]
LANGUAGE = "ml"
GENRE = None  # e.g. "romance" forces the romance hook voice; None lets the planner's <romance> flag decide. --genre overrides this
RECENT_PRECAP_WINDOW = 3  # how many just-written precaps each new one is shown
OUTPUT_ROOT = Path("output-latest-rq")

# Usage examples (run from project root):
#   python -m tests.test_hook_gen                                                        # defaults: SERIES_SLUGS, 3 precaps (chapters 1-3) hinting ONE event from chapters 1-15
#   python -m tests.test_hook_gen --series wxljcrzqxhlj                                  # single series
#   python -m tests.test_hook_gen --series wxljcrzqxhlj 6cpqfrtqn8dk orqd3inphyvb        # multiple series
#   python -m tests.test_hook_gen --language en                                          # different language
#   python -m tests.test_hook_gen --genre romance                                        # force romance hook guidance on every precap
#   python -m tests.test_hook_gen --fresh                                                # throw away the stored blueprint and hooks first
#   python -m tests.test_hook_gen --series wxljcrzqxhlj --chapters 2                     # rewrite only chapter 2's precap from the stored blueprint
#   python -m tests.test_hook_gen --flow near                                            # near payoff: each chapter's own near event, files in output-latest-rq/<slug>/near-payoff/
#
# A genre run keeps its files in output-latest-rq/<slug>/<genre>/, apart from the generic
# run, so a stored blueprint or hooks from one genre are never reused by another. A run is
# incremental: a stored blueprint is reused, and chapters that already have a hook keep it.


def read_blueprint(blueprint_file, chapters, tag="", near=False, offset=0):
    """Parse the stored blueprint, or (None, None) if there is nothing usable.

    Constraint-checked on every read rather than trusted, because the file may
    have been written by an older run, by main.py, or by hand."""
    if not blueprint_file.exists():
        return None, None
    xml = blueprint_file.read_text(encoding="utf-8")
    if not xml.strip():
        return None, None
    # A blueprint planned under a different chapter 1 skip numbers its chapters differently.
    stored = re.match(r"<!-- chapter offset: (\d+) -->", xml)
    if (int(stored.group(1)) if stored else 0) != offset:
        print(f"{tag}Stored blueprint was planned with a different chapter 1 skip — planning again")
        return None, None
    try:
        return blueprint_from_xml(
            xml, chapter_count=len(chapters), precap_limit=PRECAP_LIMIT, chapters=chapters, near=near,
        )
    except BlueprintParseError as e:
        # a truncated or hand-broken file is not a reason to stop; plan again
        print(f"{tag}Stored blueprint unusable ({e}) — planning again")
        return None, None


def ensure_blueprint(chapters, language, blueprint_file, run_id=None, tag="", genre=None, near=False, offset=0):
    """Pass 1: reuse the stored blueprint when it covers every precap chapter,
    otherwise plan again. Nothing missing means no planning call at all, which is
    the point — Pass 1 reads every chapter in one prompt and is the most
    expensive single step."""
    mappings, rejected = read_blueprint(blueprint_file, chapters, tag, near, offset)
    if mappings and len(mappings) == PRECAP_LIMIT:
        print(f"{tag}Pass 1 skipped — reusing {blueprint_file.name}")
        return mappings, rejected

    print(f"{tag}Pass 1 planning chapters 1-{len(chapters)}")
    _, _, xml = plan_precaps(
        chapters, language=language, run_id=run_id, precap_limit=PRECAP_LIMIT, genre=genre, near=near,
    )
    # Persist straight away, so the blueprint survives even if Pass 2 blows up.
    offset_header = f"<!-- chapter offset: {offset} -->\n" if offset else ""
    blueprint_file.write_text(offset_header + xml, encoding="utf-8")
    print(f"{tag}Pass 1 blueprint XML stored: {blueprint_file}")

    mappings, rejected = read_blueprint(blueprint_file, chapters, tag, near, offset)
    return mappings or [], rejected or []


def read_existing_hooks(output_file, offset=0):
    """{chapter_number: (target_chapter, hook)} already written to the .md.

    Read back out of the markdown rather than from a sidecar, so the file a run
    produces is the same file the next run resumes from — fix a hook by hand and
    the next run keeps your edit instead of overwriting it."""
    if not output_file.exists():
        return {}
    blocks = re.split(
        r"^## Chapter (\d+)\s*$", output_file.read_text(encoding="utf-8"), flags=re.M
    )
    hooks = {}
    for i in range(1, len(blocks) - 1, 2):
        body = blocks[i + 1]
        found = re.search(r"^- \*\*Target chapter:\*\* (\d+)\s*$", body, flags=re.M)
        hook = re.sub(r"^- \*\*Target chapter:\*\* \d+\s*$", "", body, flags=re.M).strip()
        if hook:
            hooks[int(blocks[i]) - offset] = ((int(found.group(1)) - offset) if found else 0, hook)
    return hooks


def series_output_dir(series_slug, genre=None, near=False):
    """Where one series' blueprint and hooks live."""
    base = OUTPUT_ROOT / series_slug
    if near:
        base = base / "near-payoff"
    return base / genre.lower() if genre else base


def write_markdown(series_slug, language, results, genre=None, near=False, offset=0):
    """All hooks for one series in a single .md, chapter numbers in order.

    Rewritten after every finished precap, not once at the end, so an interrupt
    partway through does not lose every series at once."""
    output_file = series_output_dir(series_slug, genre, near) / f"{series_slug}.md"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    title = f"{series_slug} ({language}, {genre})" if genre else f"{series_slug} ({language})"
    lines = [f"# {title}", ""]
    for chapter_number, target_chapter, hook in sorted(results, key=lambda r: r[0]):
        lines.append(f"## Chapter {chapter_number + offset}")
        lines.append("")
        lines.append(f"- **Target chapter:** {target_chapter + offset}")
        lines.append("")
        lines.append(hook)
        lines.append("")
    output_file.write_text("\n".join(lines), encoding="utf-8")
    return output_file


def generate_sequentially(series_slug, mappings, chapters, language, existing_hooks, wanted, run_id=None, genre=None, redo=frozenset(), near=False, offset=0):
    """Pass 2: every precap in chapter order, one at a time, skipping the done.

    Each precap is handed every earlier one written for the event, so it can
    repeat neither their content nor their shape. A chapter that already has a
    hook is not regenerated, but its hook still feeds the context the next one is
    written against. A chapter with neither a stored hook nor a place in `wanted`
    breaks that chain, so the context resets there rather than carrying a gap."""
    tag = f"[{series_slug} {run_id}] " if run_id else f"[{series_slug}] "
    results = [(n, target, hook) for n, (target, hook) in existing_hooks.items()]
    failed = []
    event_precaps = []
    recent_precaps = deque(maxlen=RECENT_PRECAP_WINDOW)
    previous_mapping = None

    for mapping in sorted(mappings, key=lambda m: m.chapter_number):
        chapter_number = mapping.chapter_number
        if chapter_number not in wanted and chapter_number not in existing_hooks:
            previous_mapping = None
            event_precaps = []
            recent_precaps.clear()
            continue

        continues = (
            previous_mapping is not None
            and previous_mapping.target_chapter == mapping.target_chapter
            and previous_mapping.chapter_number + 1 == chapter_number
        )
        if not continues:
            event_precaps = []

        if chapter_number in existing_hooks and chapter_number not in redo:
            hook = existing_hooks[chapter_number][1]
        else:
            try:
                hook = process_chapter(
                    book_id=f"{series_slug}_chapter_{chapter_number}",
                    chapter_read_text=chapters[chapter_number - 1],
                    target_chapter_text=chapters[mapping.target_chapter - 1],
                    mapping=mapping,
                    language=language,
                    previous_limit=previous_mapping.limit if continues else None,
                    same_scene_precaps=list(event_precaps),
                    recent_precaps=list(recent_precaps),
                    run_id=run_id,
                    genre=genre,
                )
            except Exception as e:
                # one failure must not stop the chain — later chapters simply
                # compare against the last precaps that did succeed
                print(f"{tag}Chapter {chapter_number} failed — {e}")
                failed.append(chapter_number)
                previous_mapping = None
                continue

            results = [r for r in results if r[0] != chapter_number]
            results.append((chapter_number, mapping.target_chapter, hook))
            write_markdown(series_slug, language, results, genre=genre, near=near, offset=offset)
            print(f"\n{'-' * 50}")
            print(f"{tag}Chapter {chapter_number} -> {mapping.target_chapter}")
            print(f"{'-' * 50}\nHook: {hook}\n{'-' * 50}")

        event_precaps.append(hook)
        recent_precaps.append(hook)
        previous_mapping = mapping

    return results, failed


def process_series(series_slug, args, ingestor):
    # One id for this slug's whole run — Pass 1 and every Pass 2 call under it.
    # Series run concurrently and interleave their output and their LLM traffic,
    # so book_id alone cannot separate two runs of the same book.
    run_id = f"{datetime.now():%Y%m%d-%H%M%S}-{uuid.uuid4().hex[:6]}"
    tag = f"[{series_slug} {run_id}] "

    print(f"\n{'=' * 60}")
    print(f"SERIES: {series_slug}  (run {run_id})")
    print(f"{'=' * 60}")

    chapter_iter = ingestor.iter_series_chapters(series_slug, language=args.language)
    chapters = list(islice(chapter_iter, NEAR_CHAPTER_LIMIT if args.flow == "near" else CHAPTER_LIMIT))

    # Same skip as main.py: an author's note or promo as chapter 1 has nothing to
    # bridge from. Internally chapters stay numbered from 1 as the planner sees
    # them; `offset` puts the series' own numbers back in the markdown.
    offset = 0
    if is_non_story_opener(chapters):
        offset = 1
        print(f"{tag}Chapter 1 looks like a non-story opener ({len(chapters[0])} chars) — skipping it")
        chapters = chapters[1:] + list(islice(chapter_iter, 1))
    if len(chapters) <= PRECAP_LIMIT:
        print(f"{tag}Need more than {PRECAP_LIMIT} chapters to pick an event from — nothing to generate")
        return []

    near = args.flow == "near"
    output_dir = series_output_dir(series_slug, args.genre, near)
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"{series_slug}.md"
    blueprint_file = output_dir / f"{series_slug}_blueprint.xml"

    if args.fresh:
        for path in (blueprint_file, output_file):
            if path.exists():
                path.unlink()
                print(f"{tag}--fresh: removed {path.name}")

    try:
        if args.chapters:
            mappings, rejected = read_blueprint(blueprint_file, chapters, tag, near, offset)
            if not mappings:
                print(f"{tag}--chapters needs a stored blueprint ({blueprint_file}) and found none — run without it first")
                return []
        else:
            mappings, rejected = ensure_blueprint(
                chapters, args.language, blueprint_file, run_id, tag, genre=args.genre, near=near, offset=offset,
            )
    except BlueprintParseError as e:
        # the planning call is expensive; keep what came back so it can be read
        failed_file = output_dir / f"{series_slug}_blueprint_failed.xml"
        failed_file.write_text(e.response, encoding="utf-8")
        print(f"{tag}Pass 1 failed — {e}\nRaw planner response written to: {failed_file}")
        return []

    for chapter_number, reason in rejected:
        print(f"{tag}Chapter {chapter_number} dropped by constraint check — {reason}")

    existing_hooks = read_existing_hooks(output_file, offset)
    planned = {m.chapter_number for m in mappings}
    redo = {n - offset for n in args.chapters or ()}
    if redo - planned:
        print(f"{tag}Chapters {sorted(redo - planned)} have no mapping in the blueprint — skipping them")
        redo &= planned
    wanted = (planned - set(existing_hooks)) | redo
    if args.chapters and not redo:
        print(f"{tag}Nothing left to generate")
        return [(n, target, hook) for n, (target, hook) in existing_hooks.items()]
    kept = (set(existing_hooks) & planned) - redo
    if kept:
        print(f"{tag}Chapters {sorted(kept)} already have hooks — keeping them")

    if not wanted:
        print(f"{tag}Nothing left to generate")
        return [(n, target, hook) for n, (target, hook) in existing_hooks.items()]

    print(f"{tag}Generating {len(wanted)} precaps sequentially: {sorted(wanted)}")
    results, failed = generate_sequentially(
        series_slug, mappings, chapters, args.language, existing_hooks, wanted, run_id,
        genre=args.genre, redo=redo, near=near, offset=offset,
    )

    if failed:
        print(f"\n{tag}Failed chapters: {sorted(failed)}")

    results.sort(key=lambda row: row[0])
    output_file = write_markdown(series_slug, args.language, results, genre=args.genre, near=near, offset=offset)

    print(
        f"\n{tag}Done — {len(results)} hooks on file "
        f"({len(results) - len(existing_hooks)} new). Stored in {output_file}"
    )

    return results


def main():
    parser = argparse.ArgumentParser(description="Generate precaps for one or more series")
    parser.add_argument("--series", nargs="+", default=SERIES_SLUGS, help="One or more series slugs")
    parser.add_argument("--language", default=LANGUAGE, help="Language code")
    parser.add_argument(
        "--genre",
        default=GENRE,
        help="Genre, e.g. romance — forces that genre's hook-writing guidance. Without it, the romance voice is used only when the planner picks a romantic event",
    )
    parser.add_argument(
        "--flow", choices=("event", "near"), default="event",
        help="event: every precap points at one big event; near: each chapter may point at its own near event (files go to output-latest-rq/<slug>/near-payoff/)",
    )
    parser.add_argument(
        "--fresh",
        action="store_true",
        help="Delete the stored blueprint and hooks first, and redo the series from scratch",
    )
    parser.add_argument(
        "--chapters",
        type=int,
        nargs="+",
        help="Rewrite only these chapters' precaps (e.g. 2 or 1 3) from the stored blueprint, without planning again; the other chapters' hooks stay and still feed the context",
    )
    args = parser.parse_args()
    if args.chapters and args.fresh:
        parser.error("--chapters keeps the stored blueprint and the other hooks, so it cannot be used with --fresh")

    ingestor = ChapterIngestor()

    hooks_by_slug = {}   # slug -> number of hooks on file

    # Run every series concurrently — each in its own thread; chapters within a
    # series stay sequential.
    with ThreadPoolExecutor(max_workers=len(args.series)) as executor:
        futures = {
            executor.submit(process_series, series_slug, args, ingestor): series_slug
            for series_slug in args.series
        }
        for future in as_completed(futures):
            series_slug = futures[future]
            try:
                hooks_by_slug[series_slug] = len(future.result())
            except Exception as e:
                print(f"[{series_slug}] Series failed — {e}")

    if not any(hooks_by_slug.values()):
        print("\nNo hooks generated — nothing to write")
        return

    total = sum(hooks_by_slug.values())
    print(f"\n{total} hooks on file across {len(hooks_by_slug)} series — stored in {OUTPUT_ROOT}/")


if __name__ == "__main__":
    main()
