import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import pandas as pd

from ingestion.ingest_chapter import ChapterIngestor
from pipeline.runner import process_chapter

# SERIES_SLUGS = ["wxljcrzqxhlj", "6cpqfrtqn8dk"]
# SERIES_SLUGS = ["rpe4jtpbjp5x", "gd08rcgxroxp", "63qaghm3xpbj", "sclk7xgjqn3s", "lb12rsbg841o", "br9xkihju6fq", "vmavpouo002k", "kpgvfdp2zjef", "nxycdihwjddy", "snrbplmnmuar", "kbc51zllbgp7", "mnnuddk33fl7", "yeft3rnee7uj", "stwvivx7wrgu", "7d3glqxwt1py"]
SERIES_SLUGS = ["irvvdhrgn8o3", "g2ugjfqtym9l", "oqwvwnirc6xl", "ndcf5cftvv4m", "hmuztbpiopyu", "2kg6qrkloftc", "6gp9qqxd7m6n", "h19ea8tnjkju", "lenmlr14efys"]
LANGUAGE = "ml"
NUM_CHAPTERS = 20  # number of hooks to generate
MAX_WORKERS = 5


def hook_worker(series_slug, chapter_number, prev_text, curr_text, language):
    hook = process_chapter(
        book_id=f"{series_slug}_chapter_{chapter_number}",
        previous_chapter_text=prev_text,
        current_chapter_text=curr_text,
        language=language,
    )
    return chapter_number, hook


# Usage examples (run from project root):
#   python -m tests.test_hook_gen                                                        # defaults: SERIES_SLUGS, chapter 2, 20 hooks
#   python -m tests.test_hook_gen --series wxljcrzqxhlj                                  # single series
#   python -m tests.test_hook_gen --series wxljcrzqxhlj 6cpqfrtqn8dk orqd3inphyvb        # multiple series
#   python -m tests.test_hook_gen --start 30                                             # start from chapter 30, generate 20 hooks
#   python -m tests.test_hook_gen --start 30 --count 10                                  # start from chapter 30, generate 10 hooks
#   python -m tests.test_hook_gen --chapters 15 22 38 45                                 # specific chapters only
#   python -m tests.test_hook_gen --language en                                          # different language
#   python -m tests.test_hook_gen --series wxljcrzqxhlj 6cpqfrtqn8dk --language en --start 10 --count 5
#   python -m tests.test_hook_gen --series wxljcrzqxhlj 6cpqfrtqn8dk --language en --chapters 10 20 30


def process_series(series_slug, args, ingestor):
    print(f"\n{'=' * 60}")
    print(f"SERIES: {series_slug}")
    print(f"{'=' * 60}")

    chapters = list(ingestor.iter_series_chapters(series_slug, language=args.language))

    if len(chapters) < 2:
        print(f"[{series_slug}] Not enough chapters to generate hooks")
        return []

    if args.chapters:
        chapter_numbers = sorted(set(args.chapters))
    else:
        start = max(2, args.start)
        chapter_numbers = list(range(start, start + args.count))

    # chapter N needs chapters[N-2] (prev) and chapters[N-1] (curr)
    valid = [n for n in chapter_numbers if 2 <= n <= len(chapters)]
    skipped = set(chapter_numbers) - set(valid)
    if skipped:
        print(f"[{series_slug}] Skipping out-of-range chapters: {sorted(skipped)}")

    pairs = [(n, chapters[n - 2], chapters[n - 1]) for n in valid]

    results = []
    failed = []

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_chapter = {
            executor.submit(
                hook_worker, series_slug, chapter_number, prev_text, curr_text, args.language
            ): chapter_number
            for chapter_number, prev_text, curr_text in pairs
        }

        for future in as_completed(future_to_chapter):
            chapter_num = future_to_chapter[future]
            try:
                chapter_number, hook = future.result()
                results.append((chapter_number, hook))
                print(f"\n{'─' * 50}")
                print(f"[{series_slug}] Chapter {chapter_number}")
                print(f"{'─' * 50}")
                print(f"Hook: {hook}")
                print(f"{'─' * 50}")
            except Exception as e:
                print(f"[{series_slug}] Chapter {chapter_num}: hook generation failed — {e}")
                failed.append(chapter_num)

    if failed:
        print(f"\n[{series_slug}] Failed chapters: {sorted(failed)}")

    results.sort(key=lambda x: x[0])

    # Also store all hooks as a plain-text file named after the series slug.
    local_dir = Path("local_results")
    local_dir.mkdir(exist_ok=True)
    local_file = local_dir / f"{series_slug}.txt"
    with local_file.open("w", encoding="utf-8") as f:
        for chapter_number, hook in results:
            f.write(f"Chapter {chapter_number}\n{hook}\n\n")

    print(
        f"\n[{series_slug}] Done — generated {len(results)} hooks. "
        f"Hooks also stored in {local_file}"
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
        default=2,
        help="Starting chapter number (min 2, needs a previous chapter)",
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
        "--output",
        default=None,
        help="Path of the combined Excel sheet (default: output_new2/hooks_<language>.xlsx)",
    )
    args = parser.parse_args()

    ingestor = ChapterIngestor()

    # slug -> {chapter_number: hook}, one column per slug in the combined sheet.
    hooks_by_slug = {}

    # Run every series concurrently — each in its own thread, with its own
    # chapter-level worker pool inside process_series.
    with ThreadPoolExecutor(max_workers=len(args.series)) as executor:
        futures = {
            executor.submit(process_series, series_slug, args, ingestor): series_slug
            for series_slug in args.series
        }
        for future in as_completed(futures):
            series_slug = futures[future]
            try:
                hooks_by_slug[series_slug] = dict(future.result())
            except Exception as e:
                print(f"[{series_slug}] Series failed — {e}")

    if not any(hooks_by_slug.values()):
        print("\nNo hooks generated — nothing to write")
        return

    # Excel output disabled for now — hooks are only written to local_results/<slug>.txt
    # by process_series. Uncomment to write the combined sheet (one column per slug).
    # # Keep the column order the same as the order the slugs were passed in.
    df = pd.DataFrame({slug: hooks_by_slug.get(slug, {}) for slug in args.series})
    df = df.sort_index()
    df.index.name = "chapter_number"

    output_file = Path(args.output) if args.output else Path("output_exp") / f"hooks_{args.language}.xlsx"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    df.to_excel(output_file, index=True)

    print(f"\nAll series written to {output_file} — one column per slug: {', '.join(args.series)}")

    total = sum(len(hooks) for hooks in hooks_by_slug.values())
    print(f"\nGenerated {total} hooks across {len(hooks_by_slug)} series — stored in local_results/")


if __name__ == "__main__":
    main()
