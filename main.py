from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import pandas as pd

from ingestion.ingest_chapter import ChapterIngestor
from pipeline.runner import process_chapter


def hook_worker(series_slug, idx, prev_text, curr_text, language):
    chapter_number = idx + 1

    hook = process_chapter(
        book_id=f"{series_slug}_chapter_{chapter_number}",
        previous_chapter_text=prev_text,
        current_chapter_text=curr_text,
        language=language,
    )
    return chapter_number, hook


def main():
    series_slug = "wxljcrzqxhlj"
    language = "hi"
    ingestor = ChapterIngestor()

    chapters = list(ingestor.iter_series_chapters(series_slug, language=language))
    # chapters =fetch_chapters_from_html_file(
    #     "orqd3inphyvb.html"
    # )
    if len(chapters) < 2:
        print("Not enough chapters to generate hooks")
        return

    chapter_pairs = [(i, chapters[i - 1], chapters[i]) for i in range(1, len(chapters))]

    results = []
    failed = []

    with ThreadPoolExecutor(max_workers=3) as executor:
        future_to_chapter = {
            executor.submit(hook_worker, series_slug, idx, prev_text, curr_text, language): idx
            + 1
            for idx, prev_text, curr_text in chapter_pairs
        }

        for future in as_completed(future_to_chapter):
            chapter_num = future_to_chapter[future]
            try:
                results.append(future.result())
            except Exception as e:
                print(f"Chapter {chapter_num}: hook generation failed — {e}")
                failed.append(chapter_num)

    if failed:
        print(f"\nFailed chapters: {sorted(failed)}")

    results.sort(key=lambda x: x[0])

    df = pd.DataFrame(results, columns=["chapter_number", "hook"])
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / f"{series_slug}_grok.xlsx"
    df.to_excel(output_file, index=False)

    print(f"Results stored in Excel sheet: {output_file}")


if __name__ == "__main__":
    main()
