import argparse
import re
import uuid
from collections import deque
from datetime import datetime
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

# SERIES_SLUGS = ["vnustigw45xt", "wxljcrzqxhlj", "loydb6s7xqa5", "rv5i7wqoclxs"]
SERIES_SLUGS = ["gjrvhkgosiyn", "py1qx8mjfdnf"]
# SERIES_SLUGS = ["rpe4jtpbjp5x", "gd08rcgxroxp", "63qaghm3xpbj", "sclk7xgjqn3s", "lb12rsbg841o", "br9xkihju6fq", "vmavpouo002k", "kpgvfdp2zjef", "nxycdihwjddy", "snrbplmnmuar", "kbc51zllbgp7", "mnnuddk33fl7", "yeft3rnee7uj", "stwvivx7wrgu", "7d3glqxwt1py"]
LANGUAGE = "hi"
NUM_CHAPTERS = 10  # number of hooks to generate (chapters 1..10 by default)
# How many chapters Pass 1 may read when --scan is not given, matching main.py.
# The planner reads the whole window in one prompt, so this is what it sees when
# it picks each chapter's peak — a script reading a different number of chapters
# than main.py produces a different blueprint from the same series and settings,
# and the two stop being comparable. Chapters past the last one asked for are
# still in the window because a precap may target up to LOOKAHEAD ahead.
CHAPTER_LIMIT = 15
RECENT_PRECAP_WINDOW = 3  # how many just-written precaps each new one is shown
OUTPUT_ROOT = Path("output-latest-rq")

# Usage examples (run from project root):
#   python -m tests.test_hook_gen                                                        # defaults: SERIES_SLUGS, chapters 1-10
#   python -m tests.test_hook_gen --series wxljcrzqxhlj                                  # single series
#   python -m tests.test_hook_gen --series wxljcrzqxhlj 6cpqfrtqn8dk orqd3inphyvb        # multiple series
#   python -m tests.test_hook_gen --start 30 --count 5                                   # chapters 30-34
#   python -m tests.test_hook_gen --chapters 15 22 38 45                                 # specific chapters only
#   python -m tests.test_hook_gen --language en                                          # different language
#
# Runs are INCREMENTAL: the blueprint and the hooks both accumulate in
# output-latest-rq/<slug>/, and each run does only the work that is missing.
#   python -m tests.test_hook_gen --series wxljcrzqxhlj --scan 1 15 --count 10
#   python -m tests.test_hook_gen --series wxljcrzqxhlj --scan 11 25 --start 11 --count 10
# The second call plans chapters 11-25, appends those rows to the SAME
# <slug>_blueprint.xml, and generates only chapters 11-20 — chapters 1-10 keep
# the hooks they already have and cost nothing.
#
#   python -m tests.test_hook_gen --series wxljcrzqxhlj --fresh --scan 1 25 --count 20
# --fresh throws both files away and redoes the range from scratch.


# ── the blueprint file, in SERIES numbering ──────────────────────────
#
# plan_precaps() is handed a window and answers in that window's own numbering:
# a plan over chapters 11-25 comes back with chapter_id 1..15. Stored raw, that
# file only means anything next to the window it was planned for, and two scans
# of one story cannot share a file — their chapter_ids collide head on.
# Renumbering to series chapters on the way in makes the file absolute, one per
# story, and lets a later scan append to it.
#
# main.py is unaffected: its window always starts at chapter 1, where the two
# numberings are identical.

_MAPPING_RE = re.compile(r"<mapping>.*?</mapping>", re.S)
_CHAPTER_ID_RE = re.compile(r"(<(?:target_)?chapter_id>)\s*(\d+)\s*(</(?:target_)?chapter_id>)")


def renumber_blueprint(xml, offset):
    """Shift every chapter_id and target_chapter_id in a raw planner response.

    Textual rather than parse-and-rebuild, so the file stays the planner's own
    output — including any row whose XML was malformed enough that the parser
    had to read its fields out of the surrounding text. Rebuilding from the
    parsed mappings would silently drop those."""
    if not offset:
        return xml
    return _CHAPTER_ID_RE.sub(
        lambda m: f"{m.group(1)}{int(m.group(2)) + offset}{m.group(3)}", xml
    )


def blueprint_rows(xml):
    """{chapter_number: raw <mapping> block} for a series-numbered blueprint."""
    rows = {}
    for block in _MAPPING_RE.findall(xml or ""):
        found = _CHAPTER_ID_RE.search(block)
        if found:
            rows[int(found.group(2))] = block.strip()
    return rows


def merge_blueprints(existing_xml, new_xml):
    """One <blueprint> holding both sets of rows, new rows winning on overlap.

    Chapter order is restored on the way out because the constraint check reads
    the target column top to bottom to verify the anchor staircase."""
    rows = blueprint_rows(existing_xml)
    rows.update(blueprint_rows(new_xml))
    body = "\n".join(rows[n] for n in sorted(rows))
    return f"<blueprint>\n{body}\n</blueprint>\n"


def scan_window(chapter_numbers, scan_range, chapter_count):
    """The chapters Pass 1 MAY read, as (start, end) inclusive, series numbers.

    `--scan START END` names that range outright; without it the window starts
    at the first requested chapter and runs CHAPTER_LIMIT chapters, which is the
    window main.py hands the planner.

    This is the range Pass 1 is allowed to read, not the range it will actually
    plan: ensure_blueprint narrows it to whatever the stored blueprint does not
    already cover."""
    first, last = min(chapter_numbers), max(chapter_numbers)
    if scan_range:
        start, end = scan_range
    else:
        # Never let the window close before the last precap's lookahead: asking
        # for more chapters than CHAPTER_LIMIT would otherwise leave the final
        # chapters with no target to reach for.
        start = first
        end = start - 1 + max(CHAPTER_LIMIT, last - start + 1 + LOOKAHEAD)
    return max(1, start), min(chapter_count, end)


def read_blueprint(blueprint_file, chapters, precap_limit, tag=""):
    """Parse the stored blueprint, or (None, None) if there is nothing usable.

    Constraint-checked on every read rather than trusted, because the file may
    have been written by an older run, by main.py, or by hand."""
    if not blueprint_file.exists():
        return None, None
    xml = blueprint_file.read_text(encoding="utf-8")
    if not xml.strip():
        return None, None
    try:
        return blueprint_from_xml(
            xml,
            chapter_count=len(chapters),
            lookahead=LOOKAHEAD,
            precap_limit=precap_limit,
        )
    except BlueprintParseError as e:
        # a truncated or hand-broken file is not a reason to stop; plan again
        print(f"{tag}Stored blueprint unusable ({e}) — planning again")
        return None, None


def ensure_blueprint(chapters, chapter_numbers, language, blueprint_file, scan, run_id=None, tag=""):
    """Pass 1, incrementally: plan only the chapters the blueprint is missing.

    Reads whatever is already on disk, works out which requested chapters have
    no row, and plans ONE window covering those — from the first gap to the end
    of the scan range. That result is renumbered into series chapters, merged
    into the same file, and the whole merged blueprint is then re-checked, so
    the join between old rows and new ones is validated rather than assumed.

    That re-check matters: the planner reads only its own window, so a run it
    anchors near the start of chapter 11's window may collide with a run the
    earlier plan already set up across the boundary. The constraint check
    surfaces that as a rejection with a reason instead of leaving a broken
    anchor staircase in place.

    Nothing missing means no planning call at all, which is the point — Pass 1
    reads every chapter in one prompt and is the most expensive single step.

    Returns mappings and rejections in series numbering."""
    scan_start, scan_end = scan
    requested = set(chapter_numbers)
    precap_limit = max(chapter_numbers)

    mappings, rejected = read_blueprint(blueprint_file, chapters, precap_limit, tag)
    covered = {m.chapter_number for m in mappings or []} | {n for n, _ in rejected or []}
    missing = sorted(requested - covered)

    if mappings is not None and not missing:
        print(f"{tag}Pass 1 skipped — every requested chapter is already in {blueprint_file.name}")
        return mappings, rejected

    # Plan from the first gap, not from the scan start: the rows before it are
    # already on disk, and re-planning them would cost a call and churn rows
    # whose hooks are already written against them.
    window_start = max(min(missing) if missing else scan_start, scan_start)
    window_end = min(scan_end, len(chapters))
    window = chapters[window_start - 1 : window_end]
    if len(window) < 2:
        print(f"{tag}Scan range {window_start}-{window_end} is too short to plan over")
        return mappings or [], rejected or []

    print(f"{tag}Pass 1 planning chapters {window_start}-{window_end} (missing: {missing})")
    _, _, new_xml = plan_precaps(
        window,
        language=language,
        lookahead=LOOKAHEAD,
        run_id=run_id,
        # window-local: the planner stops mapping at the last chapter asked for,
        # and the tail of the window exists only to be aimed at
        precap_limit=max(chapter_numbers) - window_start + 1,
    )

    existing_xml = (
        blueprint_file.read_text(encoding="utf-8") if blueprint_file.exists() else ""
    )
    merged = merge_blueprints(existing_xml, renumber_blueprint(new_xml, window_start - 1))
    # Persist straight away, so the blueprint survives even if Pass 2 blows up.
    blueprint_file.write_text(merged, encoding="utf-8")
    print(f"{tag}Pass 1 blueprint XML stored: {blueprint_file}")

    mappings, rejected = read_blueprint(blueprint_file, chapters, precap_limit, tag)
    return mappings or [], rejected or []


def read_existing_hooks(output_file):
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
            hooks[int(blocks[i])] = (int(found.group(1)) if found else 0, hook)
    return hooks


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


def generate_sequentially(series_slug, mappings, chapters, language, existing_hooks, wanted, run_id=None):
    """Pass 2: every precap in chapter order, one at a time, skipping the done.

    Each precap is handed every earlier one aimed at the same scene, plus the
    last few the listener heard whatever scene they were about, so it can repeat
    neither their content nor their shape. That dependency is why this cannot be
    parallelised — and why it walks ALL the mappings rather than only the ones
    being generated. A chapter that already has a hook is not regenerated, but
    its hook still feeds the context the next one is written against; skipping
    it outright would leave chapter 11 blind to chapter 10 and free to repeat
    it.

    A chapter with neither a stored hook nor a place in `wanted` breaks that
    chain, so the context resets there rather than carrying a gap across."""
    tag = f"[{series_slug} {run_id}] " if run_id else f"[{series_slug}] "
    results = [(n, target, hook) for n, (target, hook) in existing_hooks.items()]
    failed = []
    run_precaps = []
    recent_precaps = deque(maxlen=RECENT_PRECAP_WINDOW)
    previous_mapping = None

    for mapping in sorted(mappings, key=lambda m: m.chapter_number):
        chapter_number = mapping.chapter_number
        if chapter_number not in wanted and chapter_number not in existing_hooks:
            # no hook here, so there is nothing to carry forward past it
            previous_mapping = None
            run_precaps = []
            recent_precaps.clear()
            continue

        same_run = (
            previous_mapping is not None
            and previous_mapping.target_chapter == mapping.target_chapter
            and previous_mapping.chapter_number + 1 == chapter_number
        )
        if not same_run:
            run_precaps = []          # a new scene starts with nothing said about it

        if chapter_number in existing_hooks:
            hook = existing_hooks[chapter_number][1]
        else:
            try:
                hook = process_chapter(
                    book_id=f"{series_slug}_chapter_{chapter_number}",
                    chapter_read_text=chapters[chapter_number - 1],
                    target_chapter_text=chapters[mapping.target_chapter - 1],
                    mapping=mapping,
                    language=language,
                    previous_reveal=previous_mapping.reveal if same_run else None,
                    same_scene_precaps=list(run_precaps),
                    recent_precaps=list(recent_precaps),
                    run_id=run_id,
                )
            except Exception as e:
                # one failure must not stop the chain — later chapters simply
                # compare against the last precaps that did succeed
                print(f"{tag}Chapter {chapter_number} failed — {e}")
                failed.append(chapter_number)
                previous_mapping = None
                continue

            results.append((chapter_number, mapping.target_chapter, hook))
            write_markdown(series_slug, language, results)
            print(f"\n{'-' * 50}")
            print(f"{tag}Chapter {chapter_number} -> {mapping.target_chapter}")
            print(f"{'-' * 50}\nHook: {hook}\n{'-' * 50}")

        run_precaps.append(hook)
        recent_precaps.append(hook)
        previous_mapping = mapping

    return results, failed


def process_series(series_slug, args, ingestor):
    # One id for this slug's whole run — Pass 1 and every Pass 2 call under it.
    # Series run concurrently and interleave their output and their LLM traffic,
    # so book_id alone cannot separate two runs of the same book; the timestamp
    # makes the id sort and the suffix keeps two runs started in the same second
    # apart.
    run_id = f"{datetime.now():%Y%m%d-%H%M%S}-{uuid.uuid4().hex[:6]}"
    tag = f"[{series_slug} {run_id}] "

    print(f"\n{'=' * 60}")
    print(f"SERIES: {series_slug}  (run {run_id})")
    print(f"{'=' * 60}")

    if args.chapters:
        chapter_numbers = sorted(set(args.chapters))
    else:
        start = max(1, args.start)
        chapter_numbers = list(range(start, start + args.count))

    if not chapter_numbers:
        print(f"{tag}No chapters requested — nothing to generate")
        return []

    # Every requested chapter must sit inside the scan range, because its
    # blueprint row can only come from a plan that read it. Caught here rather
    # than left to the constraint check, which would drop the rows one by one.
    if args.scan:
        scan_start, scan_end = args.scan
        outside = [n for n in chapter_numbers if not scan_start <= n <= scan_end]
        if outside:
            print(
                f"{tag}Chapters {sorted(outside)} are outside the scan range "
                f"{scan_start}-{scan_end} — widen --scan or drop them"
            )
            return []

    # Fetch only as far as the planner may read, rather than pulling the whole
    # series. Resolved twice — once against a provisional chapter count to know
    # how far to fetch, then again against what actually came back, because a
    # series can end inside the window. The fetch always starts at chapter 1, so
    # `chapters` stays indexable by series chapter number throughout.
    provisional = scan_window(chapter_numbers, args.scan, chapter_count=10**9)
    chapters = list(
        islice(
            ingestor.iter_series_chapters(series_slug, language=args.language),
            provisional[1],
        )
    )

    if len(chapters) < 2:
        print(f"{tag}Not enough chapters to generate hooks")
        return []

    scan = scan_window(chapter_numbers, args.scan, chapter_count=len(chapters))

    # a precap is shown at the end of chapter N, so the last chapter has none
    valid = [n for n in chapter_numbers if 1 <= n < len(chapters)]
    skipped = set(chapter_numbers) - set(valid)
    if skipped:
        print(f"{tag}Skipping out-of-range chapters: {sorted(skipped)}")
    if not valid:
        return []

    print(
        f"{tag}Requested chapters {valid[0]}-{valid[-1]}, "
        f"scan range {scan[0]}-{scan[1]}"
    )

    output_dir = OUTPUT_ROOT / series_slug
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"{series_slug}.md"
    blueprint_file = output_dir / f"{series_slug}_blueprint.xml"

    if args.fresh:
        for path in (blueprint_file, output_file):
            if path.exists():
                path.unlink()
                print(f"{tag}--fresh: removed {path.name}")

    try:
        all_mappings, rejected = ensure_blueprint(
            chapters, valid, args.language, blueprint_file, scan, run_id, tag
        )
    except BlueprintParseError as e:
        # the planning call is expensive; keep what came back so it can be read
        failed_file = output_dir / f"{series_slug}_blueprint_failed.xml"
        failed_file.write_text(e.response, encoding="utf-8")
        print(
            f"{tag}Pass 1 failed — {e}\n"
            f"Raw planner response written to: {failed_file}"
        )
        return []

    requested = set(valid)
    for chapter_number, reason in rejected:
        if chapter_number in requested:
            print(f"{tag}Chapter {chapter_number} dropped by constraint check — {reason}")

    planned = {m.chapter_number for m in all_mappings}
    unplanned = sorted(requested - planned - {n for n, _ in rejected})
    if unplanned:
        print(
            f"{tag}Chapters {unplanned} still have no blueprint row — "
            "the planner did not map them"
        )

    existing_hooks = read_existing_hooks(output_file)
    wanted = (requested & planned) - set(existing_hooks)
    already = sorted((requested & planned) & set(existing_hooks))
    if already:
        print(f"{tag}Chapters {already} already have hooks — keeping them")

    if not wanted:
        print(f"{tag}Nothing left to generate")
        return [(n, target, hook) for n, (target, hook) in existing_hooks.items()]

    print(f"{tag}Generating {len(wanted)} precaps sequentially: {sorted(wanted)}")
    results, failed = generate_sequentially(
        series_slug, all_mappings, chapters, args.language, existing_hooks, wanted, run_id
    )

    if failed:
        print(f"\n{tag}Failed chapters: {sorted(failed)}")

    results.sort(key=lambda row: row[0])
    output_file = write_markdown(series_slug, args.language, results)

    print(
        f"\n{tag}Done — {len(results)} hooks on file "
        f"({len(results) - len(existing_hooks)} new). Stored in {output_file}"
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
    parser.add_argument(
        "--scan",
        type=int,
        nargs=2,
        metavar=("START", "END"),
        help=(
            "Chapters Pass 1 may plan over, inclusive. Defaults to CHAPTER_LIMIT "
            "chapters from the first chapter asked for. Only the part not already "
            "in the stored blueprint is actually planned"
        ),
    )
    parser.add_argument(
        "--fresh",
        action="store_true",
        help="Delete the stored blueprint and hooks first, and redo the range from scratch",
    )
    args = parser.parse_args()

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
