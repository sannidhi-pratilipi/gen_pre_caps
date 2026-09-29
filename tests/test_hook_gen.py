import argparse
from collections import deque
from dataclasses import replace
from concurrent.futures import ThreadPoolExecutor, as_completed
from itertools import islice
from pathlib import Path

from ingestion.ingest_chapter import ChapterIngestor
from pipeline.arc_planning import (
    LOOKAHEAD,
    BlueprintParseError,
    blueprint_from_xml,
    plan_precaps,
)
from pipeline.runner import process_chapter

SERIES_SLUGS = ["vnustigw45xt"]
# SERIES_SLUGS = ["wxljcrzqxhlj", "6cpqfrtqn8dk"]
# SERIES_SLUGS = ["rpe4jtpbjp5x", "gd08rcgxroxp", "63qaghm3xpbj", "sclk7xgjqn3s", "lb12rsbg841o", "br9xkihju6fq", "vmavpouo002k", "kpgvfdp2zjef", "nxycdihwjddy", "snrbplmnmuar", "kbc51zllbgp7", "mnnuddk33fl7", "yeft3rnee7uj", "stwvivx7wrgu", "7d3glqxwt1py"]
# SERIES_SLUGS = ["irvvdhrgn8o3", "g2ugjfqtym9l", "oqwvwnirc6xl", "ndcf5cftvv4m", "hmuztbpiopyu", "2kg6qrkloftc", "6gp9qqxd7m6n", "h19ea8tnjkju", "lenmlr14efys"]
LANGUAGE = "hi"
NUM_CHAPTERS = 10  # number of hooks to generate (chapters 1..10 by default)
# How many chapters are fetched and planned over, matching main.py. The planner
# reads the whole window in one prompt, so this is what it sees when it picks
# each chapter's peak — a script reading a different number of chapters than
# main.py produces a different blueprint from the same series and settings, and
# the two stop being comparable. Chapters past the last one asked for are still
# in the window because a precap may target up to LOOKAHEAD chapters ahead.
CHAPTER_LIMIT = 15
RECENT_PRECAP_WINDOW = 3  # how many just-written precaps each new one is shown
OUTPUT_ROOT = Path("output-latest-rq")


def generate_sequentially(series_slug, mappings, chapters, language):
    """Every precap for the series, in chapter order, one at a time.

    Each is handed every earlier precap aimed at the same scene, plus the last
    few the listener heard whatever scene they were about, so it can repeat
    neither their content nor their shape. That dependency is why it cannot be
    parallelised."""
    results, failed = [], []
    run_precaps = []
    recent_precaps = deque(maxlen=RECENT_PRECAP_WINDOW)
    previous_mapping = None

    for mapping in sorted(mappings, key=lambda m: m.chapter_number):
        same_run = (
            previous_mapping is not None
            and previous_mapping.target_chapter == mapping.target_chapter
            and previous_mapping.chapter_number + 1 == mapping.chapter_number
        )
        if not same_run:
            run_precaps = []          # a new scene starts with nothing said about it
        try:
            hook = process_chapter(
                book_id=f"{series_slug}_chapter_{mapping.chapter_number}",
                chapter_read_text=chapters[mapping.chapter_number - 1],
                target_chapter_text=chapters[mapping.target_chapter - 1],
                mapping=mapping,
                language=language,
                previous_reveal=previous_mapping.reveal if same_run else None,
                same_scene_precaps=list(run_precaps),
                recent_precaps=list(recent_precaps),
            )
        except Exception as e:
            # one failure must not stop the chain — later chapters simply
            # compare against the last precaps that did succeed
            print(f"[{series_slug}] Chapter {mapping.chapter_number} failed — {e}")
            failed.append(mapping.chapter_number)
            previous_mapping = None
            continue

        results.append((mapping.chapter_number, mapping.target_chapter, hook))
        write_markdown(series_slug, language, results)
        run_precaps.append(hook)
        recent_precaps.append(hook)
        previous_mapping = mapping
        print(f"\n{'-' * 50}")
        print(f"[{series_slug}] Chapter {mapping.chapter_number} -> {mapping.target_chapter}")
        print(f"{'-' * 50}\nHook: {hook}\n{'-' * 50}")

    return results, failed


def plan_window(chapters, chapter_numbers, language, blueprint_file):
    """Pass 1: one planning call over the whole window, unless a blueprint for
    this window is already on disk.

    Pass 1 needs a contiguous run to plan over, but the CLI lets you ask for an
    arbitrary set of chapters. Plan over the contiguous window that starts at
    the first requested chapter and runs CHAPTER_LIMIT chapters — the same
    window main.py hands the planner — then shift the returned chapter numbers
    back into the series' own numbering.

    A blueprint already sitting at `blueprint_file` is reused rather than
    re-planned, exactly as main.py does it: the planning call reads every
    chapter in one prompt and is the single most expensive step in the run.
    Delete the .xml to force a fresh plan. The stored XML is in the WINDOW's own
    numbering, not the series', so a blueprint written for a different --start
    would be reused with every row shifted onto the wrong chapter — it parses
    cleanly and is silently wrong. The caller keys the filename to the window
    start to keep those apart; do not hand this an arbitrary path.

    Returns the shifted mappings and the shifted rejections. The blueprint XML
    is written to `blueprint_file` here rather than handed back, because the
    caller has nothing else to do with it."""
    window_start = min(chapter_numbers)

    # The tail of the window exists only to be aimed at, so the planner is told
    # to stop mapping at the last chapter actually asked for.
    precap_limit = max(chapter_numbers) - window_start + 1
    # Never let the window close before the last precap's lookahead: asking for
    # more chapters than CHAPTER_LIMIT would otherwise leave the final chapters
    # with no target to reach for.
    window_size = max(CHAPTER_LIMIT, precap_limit + LOOKAHEAD)
    window = chapters[window_start - 1 : window_start - 1 + window_size]

    mappings = rejected = blueprint_xml = None
    existing_xml = (
        blueprint_file.read_text(encoding="utf-8") if blueprint_file.exists() else ""
    )
    if existing_xml.strip():
        try:
            mappings, rejected = blueprint_from_xml(
                existing_xml,
                chapter_count=len(window),
                lookahead=LOOKAHEAD,
                precap_limit=precap_limit,
            )
            if mappings:
                blueprint_xml = existing_xml
                print(f"Pass 1 skipped — reusing blueprint XML: {blueprint_file}")
            else:
                # parsed, but nothing survived the constraint check — e.g. the
                # file was planned for a different window or chapter count
                print("Stored blueprint has no usable mappings — planning again")
        except BlueprintParseError as e:
            # a truncated or hand-broken file is not a reason to stop; fall
            # through and plan again rather than run with no mappings
            print(f"Stored blueprint unusable ({e}) — planning again")

    if blueprint_xml is None:
        mappings, rejected, blueprint_xml = plan_precaps(
            window, language=language, lookahead=LOOKAHEAD, precap_limit=precap_limit
        )
        # Persist the planner's raw response straight away, so the blueprint
        # survives even if Pass 2 blows up.
        blueprint_file.write_text(blueprint_xml, encoding="utf-8")
        print(f"Pass 1 blueprint XML stored: {blueprint_file}")

    offset = window_start - 1
    # replace() rather than rebuilding field by field: listing the fields by
    # hand silently dropped dominant_emotion when it was added, which left the
    # emotion rotation inert on this path while looking fine. Any field added
    # to ChapterMapping now carries across on its own.
    shifted = [
        replace(
            m,
            chapter_number=m.chapter_number + offset,
            target_chapter=m.target_chapter + offset,
        )
        for m in mappings
    ]
    return shifted, [(n + offset, reason) for n, reason in rejected]


# Usage examples (run from project root):
#   python -m tests.test_hook_gen                                                        # defaults: SERIES_SLUGS, chapters 1-10
#   python -m tests.test_hook_gen --series wxljcrzqxhlj                                  # single series
#   python -m tests.test_hook_gen --series wxljcrzqxhlj 6cpqfrtqn8dk orqd3inphyvb        # multiple series
#   python -m tests.test_hook_gen --start 30                                             # start from chapter 30, generate 10 hooks
#   python -m tests.test_hook_gen --start 30 --count 5                                   # start from chapter 30, generate 5 hooks
#   python -m tests.test_hook_gen --chapters 15 22 38 45                                 # specific chapters only
#   python -m tests.test_hook_gen --language en                                          # different language
#   python -m tests.test_hook_gen --series wxljcrzqxhlj 6cpqfrtqn8dk --language en --start 10 --count 5
#   python -m tests.test_hook_gen --series wxljcrzqxhlj 6cpqfrtqn8dk --language en --chapters 10 20 30


def write_markdown(series_slug, language, results):
    """All hooks for one series in a single .md, chapter numbers in order.

    Rewritten after every finished precap, not once at the end. Several series
    run concurrently and each is 10+ sequential chapters deep, so an interrupt
    partway through would otherwise lose every series at once."""
    output_file = OUTPUT_ROOT / series_slug / f"{series_slug}.md"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    lines = [f"# {series_slug} ({language})", ""]
    for chapter_number, target_chapter, hook in sorted(results, key=lambda r: r[0]):
        lines.append(f"## Chapter {chapter_number}")
        lines.append("")
        lines.append(f"- **Target chapter:** {target_chapter}")
        lines.append("")
        lines.append(hook)
        lines.append("")
    output_file.write_text("\n".join(lines), encoding="utf-8")
    return output_file


def process_series(series_slug, args, ingestor):
    print(f"\n{'=' * 60}")
    print(f"SERIES: {series_slug}")
    print(f"{'=' * 60}")

    if args.chapters:
        chapter_numbers = sorted(set(args.chapters))
    else:
        start = max(1, args.start)
        chapter_numbers = list(range(start, start + args.count))

    if not chapter_numbers:
        print(f"[{series_slug}] No chapters requested — nothing to generate")
        return []

    # Fetch only as far as the planner will read, rather than pulling the whole
    # series: the window runs CHAPTER_LIMIT chapters from the first one asked
    # for, widened if more precaps than that were requested.
    window_start = min(chapter_numbers)
    precap_limit = max(chapter_numbers) - window_start + 1
    fetch_limit = window_start - 1 + max(CHAPTER_LIMIT, precap_limit + LOOKAHEAD)
    chapters = list(
        islice(
            ingestor.iter_series_chapters(series_slug, language=args.language),
            fetch_limit,
        )
    )

    if len(chapters) < 2:
        print(f"[{series_slug}] Not enough chapters to generate hooks")
        return []

    # a precap is shown at the end of chapter N, so the last chapter has none
    valid = [n for n in chapter_numbers if 1 <= n < len(chapters)]
    skipped = set(chapter_numbers) - set(valid)
    if skipped:
        print(f"[{series_slug}] Skipping out-of-range chapters: {sorted(skipped)}")
    if not valid:
        return []

    output_dir = OUTPUT_ROOT / series_slug
    output_dir.mkdir(parents=True, exist_ok=True)

    # Keyed to the window start, because a stored blueprint is numbered from
    # the start of the window it was planned for: reusing a start=1 blueprint
    # for a start=5 run parses fine and silently maps every row onto the wrong
    # chapter. A start=1 window keeps main.py's plain filename so blueprints
    # stay interchangeable between the two scripts.
    blueprint_file = output_dir / (
        f"{series_slug}_blueprint.xml"
        if window_start == 1
        else f"{series_slug}_blueprint_ch{window_start}.xml"
    )
    try:
        all_mappings, rejected = plan_window(
            chapters, valid, args.language, blueprint_file
        )
    except BlueprintParseError as e:
        # the planning call is expensive; keep what came back so it can be read
        failed_file = output_dir / f"{series_slug}_blueprint_failed.xml"
        failed_file.write_text(e.response, encoding="utf-8")
        print(
            f"[{series_slug}] Pass 1 failed — {e}\n"
            f"Raw planner response written to: {failed_file}"
        )
        return []

    requested = set(valid)
    mappings = [m for m in all_mappings if m.chapter_number in requested]
    for chapter_number, reason in rejected:
        if chapter_number in requested:
            print(f"[{series_slug}] Chapter {chapter_number} dropped by constraint check — {reason}")
    if not mappings:
        print(f"[{series_slug}] No valid mappings — nothing to generate")
        return []

    print(f"[{series_slug}] Generating {len(mappings)} precaps sequentially")
    results, failed = generate_sequentially(series_slug, mappings, chapters, args.language)

    if failed:
        print(f"\n[{series_slug}] Failed chapters: {sorted(failed)}")

    results.sort(key=lambda row: row[0])

    output_file = write_markdown(series_slug, args.language, results)

    print(
        f"\n[{series_slug}] Done — generated {len(results)} hooks. "
        f"Hooks stored in {output_file}"
    )

    return results


def main():
    parser = argparse.ArgumentParser(description="Generate hooks for one or more series")
    parser.add_argument(
        "--series",
        nargs="+",
        default=SERIES_SLUGS,
        help="One or more series slugs",
    )
    parser.add_argument("--language", default=LANGUAGE, help="Language code")
    parser.add_argument(
        "--start",
        type=int,
        default=1,
        help="Starting chapter number (the chapter a precap is shown at the end of)",
    )
    parser.add_argument(
        "--count",
        type=int,
        default=NUM_CHAPTERS,
        help="Number of consecutive hooks to generate from --start",
    )
    parser.add_argument(
        "--chapters",
        type=int,
        nargs="+",
        help="Explicit list of chapter numbers to generate hooks for (overrides --start/--count)",
    )
    args = parser.parse_args()

    ingestor = ChapterIngestor()

    hooks_by_slug = {}   # slug -> number of hooks it produced

    # Run every series concurrently — each in its own thread, with its own
    # run-level worker pool inside process_series.
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
    print(f"\nGenerated {total} hooks across {len(hooks_by_slug)} series — stored in {OUTPUT_ROOT}/")


if __name__ == "__main__":
    main()
