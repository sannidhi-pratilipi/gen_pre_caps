import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import pandas as pd

from ingestion.ingest_chapter import ChapterIngestor
from pipeline.runner import process_chapter

# SERIES_SLUGS = ["wxljcrzqxhlj", "6cpqfrtqn8dk"]
# SERIES_SLUGS = ["rznv7rywkhsv","orqd3inphyvb"]
SERIES_SLUGS = ["shrhbywypfjb", "bjhhxvpufxeb"]
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
        return

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

    df = pd.DataFrame(results, columns=["chapter_number", "hook"])
    output_dir = Path("output_new2")
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / f"{series_slug}_test_ml_gemini.xlsx"
    df.to_excel(output_file, index=False)

    # Also store all hooks as a plain-text file named after the series slug.
    local_dir = Path("local_results")
    local_dir.mkdir(exist_ok=True)
    local_file = local_dir / f"{series_slug}.txt"
    with local_file.open("w", encoding="utf-8") as f:
        for chapter_number, hook in results:
            f.write(f"Chapter {chapter_number}\n{hook}\n\n")

    print(
        f"\n[{series_slug}] Done — generated {len(results)} hooks. "
        f"Results stored in {output_file} and {local_file}"
    )


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
    args = parser.parse_args()

    ingestor = ChapterIngestor()

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
                future.result()
            except Exception as e:
                print(f"[{series_slug}] Series failed — {e}")


if __name__ == "__main__":
    main()
