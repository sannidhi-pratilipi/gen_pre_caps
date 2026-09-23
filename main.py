from itertools import islice
from pathlib import Path

# import pandas as pd  # only needed for the Excel dump (currently disabled)

from ingestion.ingest_chapter import ChapterIngestor
from pipeline.arc_planning import LOOKAHEAD, plan_precaps
from pipeline.runner import process_chapter

# Precaps are generated for chapters 1..PRECAP_LIMIT only. Chapters past that
# are still fetched and planned over, because a precap at chapter
# PRECAP_LIMIT may target a scene up to LOOKAHEAD chapters ahead.
PRECAP_LIMIT = 10
CHAPTER_LIMIT = 15

# Pass 2 is sequential because each precap is shown the ones written before it:
# every earlier precap aimed at the same target scene, plus the one immediately
# before this chapter.


def main():
    series_slug = "wxljcrzqxhlj"
    language = "hi"
    ingestor = ChapterIngestor()

    chapters = list(islice(ingestor.iter_series_chapters(series_slug, language=language), CHAPTER_LIMIT))
    if len(chapters) < 2:
        print("Not enough chapters to generate precaps")
        return

    output_dir = Path("output-latest-rq") / series_slug
    output_dir.mkdir(parents=True, exist_ok=True)

    # ── Pass 1: one planning call over the full chapter text.
    mappings, rejected, blueprint_xml = plan_precaps(
        chapters, language=language, lookahead=LOOKAHEAD, precap_limit=PRECAP_LIMIT
    )

    # Persist the planner's raw response straight away, so the blueprint
    # survives even if Pass 2 blows up.
    blueprint_file = output_dir / f"{series_slug}_blueprint.xml"
    blueprint_file.write_text(blueprint_xml, encoding="utf-8")
    print(f"Pass 1 blueprint XML stored: {blueprint_file}")

    # The blueprint itself is not printed — it is already on disk as the raw
    # planner XML above. Only the count and anything that went wrong is logged.
    print(f"\nBlueprint: {len(mappings)}/{PRECAP_LIMIT} chapters mapped")
    if rejected:
        print("\nDropped by constraint check (no precap generated for these):")
        for chapter_number, reason in rejected:
            print(f"  chapter {chapter_number}: {reason}")

    if not mappings:
        print("\nNo valid mappings — nothing to generate.")
        return

    # ── Pass 2: strictly sequential, in chapter order. Each precap sees every
    # earlier one aimed at the same scene, plus the one immediately before it —
    # so it can be written to repeat neither their content nor their shape.
    # That dependency is why this cannot be parallelised.
    print(f"Generating {len(mappings)} precaps sequentially")

    results = []
    failed = []
    run_precaps: list[str] = []
    previous_precap = None
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
                book_id=f"{series_slug}_chapter_{mapping.chapter_number}",
                chapter_read_text=chapters[mapping.chapter_number - 1],
                target_chapter_text=chapters[mapping.target_chapter - 1],
                mapping=mapping,
                language=language,
                previous_reveal=previous_mapping.reveal if same_run else None,
                same_scene_precaps=list(run_precaps),
                previous_precap=previous_precap,
            )
        except Exception as e:
            # one failure must not stop the chain — the next chapter simply
            # compares against the last precaps that did succeed
            print(f"Chapter {mapping.chapter_number}: precap generation failed — {e}")
            failed.append(mapping.chapter_number)
            previous_mapping = None
            continue

        results.append(
            (mapping.chapter_number, mapping.target_chapter, mapping.scene_description, hook)
        )
        run_precaps.append(hook)
        previous_precap = hook
        previous_mapping = mapping

    if failed:
        print(f"\nFailed chapters: {sorted(failed)}")

    results.sort(key=lambda row: row[0])

    # ── Excel dump disabled for now; markdown is the working output format.
    # df = pd.DataFrame(results, columns=["chapter_number", "target_chapter", "target_scene", "hook"])
    # output_dir = Path("output")
    # output_dir.mkdir(exist_ok=True)
    # output_file = output_dir / f"{series_slug}_hindi.xlsx"
    # df.to_excel(output_file, index=False)
    # print(f"Results stored in Excel sheet: {output_file}")

    output_file = output_dir / f"{series_slug}.md"

    lines = [f"# {series_slug} ({language})", ""]
    for chapter_number, target_chapter, _scene, hook in results:
        lines.append(f"## Chapter {chapter_number}")
        lines.append("")
        lines.append(f"- **Target chapter:** {target_chapter}")
        lines.append("")
        lines.append(hook)
        lines.append("")

    output_file.write_text("\n".join(lines), encoding="utf-8")

    print(f"Results stored in markdown: {output_file}")


if __name__ == "__main__":
    main()
