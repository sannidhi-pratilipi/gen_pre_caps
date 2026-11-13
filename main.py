import argparse
import re
from collections import deque
from itertools import islice
from pathlib import Path

# import pandas as pd  # only needed for the Excel dump (currently disabled)

from ingestion.ingest_chapter import ChapterIngestor
from pipeline.arc_planning import (
    BlueprintParseError,
    blueprint_from_xml,
    plan_precaps,
)
from pipeline.runner import process_chapter

# Precaps are generated for chapters 1..PRECAP_LIMIT only. Every one of them hints at ONE
# event picked from the chapters after PRECAP_LIMIT, so CHAPTER_LIMIT must exceed
# PRECAP_LIMIT by enough that the event has chapters to be picked from.
PRECAP_LIMIT = 3
CHAPTER_LIMIT = 15
NEAR_CHAPTER_LIMIT = 10  # --flow near: the planner sees only the first 10 chapters

# Pass 2 is sequential because each precap is shown the ones written before it:
# every earlier precap aimed at the same target scene, plus the last few the
# listener heard whatever scene they were about.

# How many recent precaps each new one is written against. A phrase reused three
# chapters later is as audible as one reused in the next chapter, so the window
# is several precaps wide rather than one.
RECENT_PRECAP_WINDOW = 3

# A first chapter far shorter than the ones after it is an author's note, a promo
# or a pitch-style prologue rather than a scene. It has nothing a precap can
# bridge from, so it is skipped and the precaps go to the next PRECAP_LIMIT
# chapters instead. Only chapter 1 is checked.
NON_STORY_LENGTH_RATIO = 0.25


def is_non_story_opener(chapters):
    following = sorted(len(text) for text in chapters[1:6])
    if len(chapters) < 3 or not following:
        return False
    median = following[len(following) // 2]
    return len(chapters[0]) < NON_STORY_LENGTH_RATIO * median


def write_markdown(output_file, series_slug, language, results, offset=0):
    """Rewrite the whole .md from the results so far.

    Called after every finished precap rather than once at the end: a
    sequential run is 20 chapters long, each costing a generate plus a critique
    plus up to 3 rewrites, so a crash or an interrupt at chapter 18 would
    otherwise throw away everything. Rewriting the file each time keeps the
    chapters in order for the cost of a few kilobytes."""
    lines = [f"# {series_slug} ({language})", ""]
    for chapter_number, target_chapter, _scene, hook in sorted(results, key=lambda r: r[0]):
        lines.append(f"## Chapter {chapter_number + offset}")
        lines.append("")
        lines.append(f"- **Target chapter:** {target_chapter + offset}")
        lines.append("")
        lines.append(hook)
        lines.append("")
    output_file.write_text("\n".join(lines), encoding="utf-8")


def parse_args(argv=None):
    """CLI over the few things that change between runs.

    Every default is the value this script carried hardcoded, so `python
    main.py` with no arguments behaves exactly as it did before."""
    parser = argparse.ArgumentParser(description="Generate precaps for one series.")
    parser.add_argument("-s", "--series", default="gjrvhkgosiyn", help="series slug")
    parser.add_argument("-l", "--language", default="ml", help="language code, e.g. hi or ml")
    parser.add_argument(
        "-g", "--genre", default=None,
        help="genre, e.g. romance — forces that genre's hook-writing guidance. Without it, the romance voice is used only when the planner picks a romantic event",
    )
    parser.add_argument(
        "--precap-limit", type=int, default=PRECAP_LIMIT,
        help=f"generate precaps for chapters 1..N (default {PRECAP_LIMIT})",
    )
    parser.add_argument(
        "--chapter-limit", type=int, default=None,
        help=f"fetch N chapters; must exceed --precap-limit so late precaps have a target "
        f"(default {CHAPTER_LIMIT}, or {NEAR_CHAPTER_LIMIT} with --flow near)",
    )
    parser.add_argument(
        "--flow", choices=("event", "near"), default="event",
        help="event: every precap points at one big event after --precap-limit; "
        "near: each chapter may point at its own event, as near as the next chapter",
    )
    parser.add_argument(
        "-o", "--output-dir", default="output-latest-rq",
        help="directory the per-series output folder is created under "
        "(--flow near writes into <series>/near-payoff/ inside it)",
    )
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    series_slug = args.series
    language = args.language
    genre = args.genre
    precap_limit = args.precap_limit
    near = args.flow == "near"
    chapter_limit = args.chapter_limit or (NEAR_CHAPTER_LIMIT if near else CHAPTER_LIMIT)
    ingestor = ChapterIngestor()

    chapter_iter = ingestor.iter_series_chapters(series_slug, language=language)
    chapters = list(islice(chapter_iter, chapter_limit))

    # Everything below runs on the chapters after a skipped opener, numbered from 1
    # as the planner sees them; `offset` turns those numbers back into the
    # series' own wherever they are shown. One more chapter is fetched so the
    # event still has as many chapters to be picked from.
    offset = 0
    if is_non_story_opener(chapters):
        offset = 1
        print(f"Chapter 1 looks like a non-story opener ({len(chapters[0])} chars) — skipping it")
        chapters = chapters[1:] + list(islice(chapter_iter, 1))

    if len(chapters) < 2:
        print("Not enough chapters to generate precaps")
        return

    output_dir = Path(args.output_dir) / series_slug
    if near:
        output_dir = output_dir / "near-payoff"
    output_dir.mkdir(parents=True, exist_ok=True)

    # ── Pass 1: one planning call over the full chapter text — unless a
    # blueprint for this series is already on disk. The planning call reads
    # every chapter in one prompt, so it is the single most expensive step in
    # the run; when a previous run already produced a usable blueprint there is
    # nothing to gain from asking for it again. Delete the .xml to force a
    # fresh plan.
    blueprint_file = output_dir / f"{series_slug}_blueprint.xml"
    mappings = rejected = blueprint_xml = None

    # The blueprint's chapter numbers are the planner's, so a skipped opener is
    # recorded in the file; one planned under a different skip is not reused.
    offset_header = f"<!-- chapter offset: {offset} -->\n" if offset else ""
    existing_xml = (
        blueprint_file.read_text(encoding="utf-8") if blueprint_file.exists() else ""
    )
    stored = re.match(r"<!-- chapter offset: (\d+) -->", existing_xml)
    if existing_xml.strip() and (int(stored.group(1)) if stored else 0) != offset:
        print("Stored blueprint was planned with a different chapter 1 skip — planning again")
        existing_xml = ""
    if existing_xml.strip():
        try:
            mappings, rejected = blueprint_from_xml(
                existing_xml,
                chapter_count=len(chapters),
                precap_limit=precap_limit,
                chapters=chapters,
                near=near,
            )
            if mappings:
                blueprint_xml = existing_xml
                print(f"Pass 1 skipped — reusing blueprint XML: {blueprint_file}")
            else:
                # parsed, but nothing survived the constraint check — e.g. the
                # file was planned for a different chapter count
                print("Stored blueprint has no usable mappings — planning again")
        except BlueprintParseError as e:
            # a truncated or hand-broken file is not a reason to stop; fall
            # through and plan again rather than run with no mappings
            print(f"Stored blueprint unusable ({e}) — planning again")

    if blueprint_xml is None:
        try:
            mappings, rejected, blueprint_xml = plan_precaps(
                chapters, language=language, precap_limit=precap_limit, genre=genre, near=near,
            )
        except BlueprintParseError as e:
            # the planning call is expensive; keep what came back so it can be read
            failed_file = output_dir / f"{series_slug}_blueprint_failed.xml"
            failed_file.write_text(e.response, encoding="utf-8")
            print(f"Pass 1 failed — {e}\nRaw planner response written to: {failed_file}")
            return

        # Persist the planner's raw response straight away, so the blueprint
        # survives even if Pass 2 blows up.
        blueprint_file.write_text(offset_header + blueprint_xml, encoding="utf-8")
        print(f"Pass 1 blueprint XML stored: {blueprint_file}")

    # The blueprint itself is not printed — it is already on disk as the raw
    # planner XML above. Only the count and anything that went wrong is logged.
    print(f"\nBlueprint: {len(mappings)}/{precap_limit} chapters mapped")
    if rejected:
        print("\nDropped by constraint check (no precap generated for these):")
        for chapter_number, reason in rejected:
            print(f"  chapter {chapter_number + offset}: {reason}")

    if not mappings:
        print("\nNo valid mappings — nothing to generate.")
        return

    # ── Pass 2: strictly sequential, in chapter order. Each precap sees every
    # earlier one aimed at the same scene, plus the one immediately before it —
    # so it can be written to repeat neither their content nor their shape.
    # That dependency is why this cannot be parallelised.
    output_file = output_dir / f"{series_slug}.md"
    print(f"Generating {len(mappings)} precaps sequentially into {output_file}")

    results = []
    failed = []
    run_precaps: list[str] = []
    recent_precaps: deque[str] = deque(maxlen=RECENT_PRECAP_WINDOW)
    previous_mapping = None

    for mapping in sorted(mappings, key=lambda m: m.chapter_number):
        # A run is the set of chapters reaching for one scene, so its precaps
        # are the ones that can literally repeat each other. Everything else the
        # listener heard recently can only repeat a shape.
        same_run = (
            previous_mapping is not None
            and previous_mapping.target_chapter == mapping.target_chapter
            and previous_mapping.chapter_number + 1 == mapping.chapter_number
        )
        if not same_run:
            run_precaps = []          # a new scene starts with nothing said about it
        try:
            hook = process_chapter(
                book_id=f"{series_slug}_chapter_{mapping.chapter_number + offset}",
                chapter_read_text=chapters[mapping.chapter_number - 1],
                target_chapter_text=chapters[mapping.target_chapter - 1],
                mapping=mapping,
                language=language,
                previous_limit=previous_mapping.limit if same_run else None,
                same_scene_precaps=list(run_precaps),
                recent_precaps=list(recent_precaps),
                genre=genre,
            )
        except Exception as e:
            # one failure must not stop the chain — the next chapter simply
            # compares against the last precaps that did succeed
            print(f"Chapter {mapping.chapter_number + offset}: precap generation failed — {e}")
            failed.append(mapping.chapter_number + offset)
            previous_mapping = None
            continue

        results.append(
            (mapping.chapter_number, mapping.target_chapter, mapping.scene_description, hook)
        )
        write_markdown(output_file, series_slug, language, results, offset)
        print(f"  chapter {mapping.chapter_number + offset} written ({len(results)}/{len(mappings)})")
        run_precaps.append(hook)
        recent_precaps.append(hook)
        previous_mapping = mapping

    if failed:
        print(f"\nFailed chapters: {sorted(failed)}")

    # ── Excel dump disabled for now; markdown is the working output format.
    # df = pd.DataFrame(results, columns=["chapter_number", "target_chapter", "target_scene", "hook"])
    # output_dir = Path("output")
    # output_dir.mkdir(exist_ok=True)
    # output_file = output_dir / f"{series_slug}_hindi.xlsx"
    # df.to_excel(output_file, index=False)
    # print(f"Results stored in Excel sheet: {output_file}")

    print(f"Results stored in markdown: {output_file} ({len(results)} precaps)")


if __name__ == "__main__":
    main()
