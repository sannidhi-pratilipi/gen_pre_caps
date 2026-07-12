from ingestion.api_client import PratilipiClient

class ChapterIngestor:
    def __init__(self):
        self.client = PratilipiClient()

    def iter_series_chapters(self, series_slug: str, language: str = "en"):
        pratilipi_ids = self.client.get_pratilipi_ids_from_series(series_slug)

        for pid in pratilipi_ids:
            chapters = self.client.fetch_chapter_content(pid, language)
            for chapter_text in chapters:
                yield chapter_text
