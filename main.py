from collections import deque
from itertools import islice
from pathlib import Path

# import pandas as pd  # only needed for the Excel dump (currently disabled)

from ingestion.ingest_chapter import ChapterIngestor
from pipeline.arc_planning import (
    LOOKAHEAD,
    BlueprintParseError,
    blueprint_from_xml,
    plan_precaps,
)
from pipeline.runner import process_chapter

# Precaps are generated for chapters 1..PRECAP_LIMIT only. Chapters past that
# are still fetched and planned over, because a precap at chapter
# PRECAP_LIMIT may target a scene up to LOOKAHEAD chapters ahead.
PRECAP_LIMIT = 4
CHAPTER_LIMIT = 15

# Pass 2 is sequential because each precap is shown the ones written before it:
# every earlier precap aimed at the same target scene, plus the last few the
# listener heard whatever scene they were about.

# How many recent precaps each new one is written against. A phrase reused three
# chapters later is as audible as one reused in the next chapter, so the window
# is several precaps wide rather than one.
RECENT_PRECAP_WINDOW = 3


def write_markdown(output_file, series_slug, language, results):
    """Rewrite the whole .md from the results so far.

    Called after every finished precap rather than once at the end: a
    sequential run is 20 chapters long, each costing a generate plus a critique
    plus up to 3 rewrites, so a crash or an interrupt at chapter 18 would
    otherwise throw away everything. Rewriting the file each time keeps the
    chapters in order for the cost of a few kilobytes."""
    lines = [f"# {series_slug} ({language})", ""]
    for chapter_number, target_chapter, _scene, hook in sorted(results, key=lambda r: r[0]):
        lines.append(f"## Chapter {chapter_number}")
        lines.append("")
        lines.append(f"- **Target chapter:** {target_chapter}")
        lines.append("")
        lines.append(hook)
        lines.append("")
    output_file.write_text("\n".join(lines), encoding="utf-8")


def main():
    # series_slug = "wxljcrzqxhlj"
    series_slug="vnustigw45xt"
    language = "hi"
    ingestor = ChapterIngestor()

    chapters = list(islice(ingestor.iter_series_chapters(series_slug, language=language), CHAPTER_LIMIT))
    if len(chapters) < 2:
        print("Not enough chapters to generate precaps")
        return

    output_dir = Path("output-latest-rq") / series_slug
    output_dir.mkdir(parents=True, exist_ok=True)

    # ── Pass 1: one planning call over the full chapter text — unless a
    # blueprint for this series is already on disk. The planning call reads
    # every chapter in one prompt, so it is the single most expensive step in
    # the run; when a previous run already produced a usable blueprint there is
    # nothing to gain from asking for it again. Delete the .xml to force a
    # fresh plan.
    blueprint_file = output_dir / f"{series_slug}_blueprint.xml"
    mappings = rejected = blueprint_xml = None

    existing_xml = (
        blueprint_file.read_text(encoding="utf-8") if blueprint_file.exists() else ""
    )
    if existing_xml.strip():
        try:
            mappings, rejected = blueprint_from_xml(
                existing_xml,
                chapter_count=len(chapters),
                lookahead=LOOKAHEAD,
                precap_limit=PRECAP_LIMIT,
            )
            if mappings:
                blueprint_xml = existing_xml
                print(f"Pass 1 skipped — reusing blueprint XML: {blueprint_file}")
            else:
                # parsed, but nothing survived the constraint check — e.g. the
                # file was planned for a different lookahead or chapter count
                print("Stored blueprint has no usable mappings — planning again")
        except BlueprintParseError as e:
            # a truncated or hand-broken file is not a reason to stop; fall
            # through and plan again rather than run with no mappings
            print(f"Stored blueprint unusable ({e}) — planning again")

    if blueprint_xml is None:
        try:
            mappings, rejected, blueprint_xml = plan_precaps(
                chapters, language=language, lookahead=LOOKAHEAD, precap_limit=PRECAP_LIMIT
            )
        except BlueprintParseError as e:
            # the planning call is expensive; keep what came back so it can be read
            failed_file = output_dir / f"{series_slug}_blueprint_failed.xml"
            failed_file.write_text(e.response, encoding="utf-8")
            print(f"Pass 1 failed — {e}\nRaw planner response written to: {failed_file}")
            return

        # Persist the planner's raw response straight away, so the blueprint
        # survives even if Pass 2 blows up.
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
            # one failure must not stop the chain — the next chapter simply
            # compares against the last precaps that did succeed
            print(f"Chapter {mapping.chapter_number}: precap generation failed — {e}")
            failed.append(mapping.chapter_number)
            previous_mapping = None
            continue

        results.append(
            (mapping.chapter_number, mapping.target_chapter, mapping.scene_description, hook)
        )
        write_markdown(output_file, series_slug, language, results)
        print(f"  chapter {mapping.chapter_number} written ({len(results)}/{len(mappings)})")
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
