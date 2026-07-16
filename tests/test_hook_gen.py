import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import pandas as pd

from ingestion.ingest_chapter import ChapterIngestor
from pipeline.runner import process_chapter

# SERIES_SLUG = "wxljcrzqxhlj"
# SERIES_SLUG = "6cpqfrtqn8dk"
# SERIES_SLUG = "orqd3inphyvb"
SERIES_SLUG = "rznv7rywkhsv"
# SERIES_SLUG = "shrhbywypfjb"
# SERIES_SLUG = "bjhhxvpufxeb"
LANGUAGE = "hi"
NUM_CHAPTERS = 5  # number of hooks to generate
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
#   python -m tests.test_hook_gen                                                        # defaults: SERIES_SLUG, chapter 2, 20 hooks
#   python -m tests.test_hook_gen --series wxljcrzqxhlj                                  # different series
#   python -m tests.test_hook_gen --start 30                                             # start from chapter 30, generate 20 hooks
#   python -m tests.test_hook_gen --start 30 --count 10                                  # start from chapter 30, generate 10 hooks
#   python -m tests.test_hook_gen --chapters 15 22 38 45                                 # specific chapters only
#   python -m tests.test_hook_gen --language en                                          # different language
#   python -m tests.test_hook_gen --series wxljcrzqxhlj --language en --start 10 --count 5
#   python -m tests.test_hook_gen --series wxljcrzqxhlj --language en --chapters 10 20 30


def main():
    parser = argparse.ArgumentParser(description="Generate hooks for a series")
    parser.add_argument("--series", default=SERIES_SLUG, help="Series slug")
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
    chapters = list(ingestor.iter_series_chapters(args.series, language=args.language))

    if len(chapters) < 2:
        print("Not enough chapters to generate hooks")
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
        print(f"Skipping out-of-range chapters: {sorted(skipped)}")

    pairs = [(n, chapters[n - 2], chapters[n - 1]) for n in valid]

    results = []
    failed = []

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_chapter = {
            executor.submit(
                hook_worker, args.series, chapter_number, prev_text, curr_text, args.language
            ): chapter_number
            for chapter_number, prev_text, curr_text in pairs
        }

        for future in as_completed(future_to_chapter):
            chapter_num = future_to_chapter[future]
            try:
                chapter_number, hook = future.result()
                results.append((chapter_number, hook))
                print(f"\n{'─' * 50}")
                print(f"Chapter {chapter_number}")
                print(f"{'─' * 50}")
                print(f"Hook: {hook}")
                print(f"{'─' * 50}")
            except Exception as e:
                print(f"Chapter {chapter_num}: hook generation failed — {e}")
                failed.append(chapter_num)

    if failed:
        print(f"\nFailed chapters: {sorted(failed)}")

    results.sort(key=lambda x: x[0])

    df = pd.DataFrame(results, columns=["chapter_number", "hook"])
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / f"{args.series}_gemini_fixed_test.xlsx"
    df.to_excel(output_file, index=False)

    print(f"\nDone — generated {len(results)} hooks. Results stored in {output_file}")


if __name__ == "__main__":
    main()
