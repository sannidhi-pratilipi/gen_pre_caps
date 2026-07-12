import requests
import html
import re
from typing import List

from config import (
    PRATILIPI_GRAPHQL_URL,
    USER_AGENT,
    PRATILIPI_TOKEN,
)

def strip_html(text: str) -> str:
    """Remove HTML tags from content."""
    return re.sub(r"<[^>]+>", "", text or "")

class PratilipiClient:
    """
    Client responsible for interacting with Pratilipi GraphQL APIs.
    """

    def _graphql_headers(self, language: str = "en") -> dict:
        headers = {
            "client-type": "ANDROID_APP",
            "apollographql-client-name": "ANDROID",
            "apollographql-client-version": "8.13.0",
            "Access-Token": PRATILIPI_TOKEN,
            "Content-Type": "application/json",
        }

        if USER_AGENT:
            headers["User-Agent"] = USER_AGENT

        if language:
            headers["language"] = language

        return headers

    def get_pratilipi_ids_from_series(self, series_slug: str) -> List[str]:
        """
        Fetch all pratilipiIds belonging to a series.
        """
        query = """
        query getSeriesPartsPaginatedBySlug(
          $where: GetSeriesInput!,
          $page: LimitCursorPageInput
        ) {
          getSeries(where: $where) {
            series {
              publishedParts(page: $page) {
                parts {
                  pratilipi {
                    pratilipiId
                  }
                }
              }
            }
          }
        }
        """

        variables = {
            "where": {"seriesSlug": series_slug},
            "page": {"limit": 100, "cursor": "0"},
        }

        resp = requests.post(
            PRATILIPI_GRAPHQL_URL,
            headers=self._graphql_headers(),
            json={"query": query, "variables": variables},
            timeout=30,
        )
        resp.raise_for_status()

        data = resp.json()

        parts = (
            data.get("data", {})
            .get("getSeries", {})
            .get("series", {})
            .get("publishedParts", {})
            .get("parts", [])
        )

        return [
            p["pratilipi"]["pratilipiId"]
            for p in parts
            if p.get("pratilipi")
        ]

    def fetch_chapter_content(
        self,
        pratilipi_id: str,
        language: str = "en"
    ) -> List[str]:
        """
        Fetch and clean all readable chapters for a given pratilipiId.
        """
        query = """
        query ($where: GetPratilipiChaptersQueryInput!) {
          getPratilipiChapters(where: $where) {
            chapters {
              title
              content
            }
          }
        }
        """

        variables = {
            "where": {
                "pratilipiId": str(pratilipi_id)
            }
        }

        resp = requests.post(
            PRATILIPI_GRAPHQL_URL,
            headers=self._graphql_headers(language),
            json={"query": query, "variables": variables},
            timeout=30,
        )
        resp.raise_for_status()

        data = resp.json()

        raw_chapters = (
            data.get("data", {})
            .get("getPratilipiChapters", {})
            .get("chapters", [])
        )

        cleaned_chapters: List[str] = []

        for ch in raw_chapters:
            content = ch.get("content")

            if not content:
                title = ch.get("title") or "Untitled"
                print(f"Skipping locked chapter: {title}")
                continue

            cleaned = strip_html(html.unescape(content)).strip()

            if cleaned:
                cleaned_chapters.append(cleaned)

        if not cleaned_chapters:
            print(f"⚠ No usable chapters for pratilipiId={pratilipi_id}")

        return cleaned_chapters

def fetch_chapters_from_html_file(
    path: str,
) -> List[str]:
        """
        Read and split chapters from a local HTML/text file.

        Assumes chapters are separated by lines like:
        1.
        25.
        200.
        """

        try:
            with open(path, "r", encoding="utf-8") as f:
                raw_text = f.read()
        except FileNotFoundError:
            print(f"⚠ File not found: {path}")
            return []

        raw_text = strip_html(html.unescape(raw_text))

        raw_text = raw_text.replace("\r\n", "\n")

        chapter_blocks = re.split(r"\n\s*Chapter\s+\d+\s*\n", raw_text, flags=re.IGNORECASE)

        cleaned_chapters: List[str] = []

        for block in chapter_blocks:
            cleaned = block.strip()
            if cleaned:
                cleaned_chapters.append(cleaned)

        if not cleaned_chapters:
            print(f"⚠ No usable chapters found in file: {path}")

        return cleaned_chapters
