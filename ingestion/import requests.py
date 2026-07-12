import requests
import config
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from typing import List, Dict, Any

BASE_URL = config.PRATILIPI_BASE_URL
GRAPHQL_URL = getattr(config, "PRATILIPI_GRAPHQL_URL", f"{BASE_URL}/graphql")

GRAPHQL_HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Origin": BASE_URL,
    "Referer": f"{BASE_URL}/",
    "User-Agent": "Mozilla/5.0"
}


class PratilipiClient:
    def __init__(self, max_retries: int = 3, backoff: float = 0.5):
        # session with retries for transient failures
        self.session = requests.Session()
        retry = Retry(total=max_retries, backoff_factor=backoff,
                      status_forcelist=(429, 500, 502, 503, 504),
                      allowed_methods=("GET", "POST"))
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

    # GraphQL
    def get_chapters_from_series_slug(self, series_slug: str) -> list[str]:
        """
        Returns ordered list of chapter pratilipiIds
        """
        query = """
        query getSeriesPartsPaginatedBySlug($where: GetSeriesInput!, $page: LimitCursorPageInput) {
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
            "page": {"limit": 100, "cursor": "0"}
        }

        resp = self.session.post(
            GRAPHQL_URL,
            headers=GRAPHQL_HEADERS,
            json={"query": query, "variables": variables},
            timeout=10,
        )
        resp.raise_for_status()

        data = resp.json()
        parts = data["data"]["getSeries"]["series"]["publishedParts"]["parts"]

        return [p["pratilipi"]["pratilipiId"] for p in parts]

    # GraphQL bulk fetch 
    def get_whole_pratilipi_graphql(self, pratilipi_id: str, timeout: int = 10) -> List[Dict[str, Any]]:
        """Fetch all chapters (number/title/content) using a single GraphQL request.

        Returns list of {"chapterNo": int, "title": str, "content": str}
        On network errors or timeouts, returns empty list so caller can fallback to REST.
        """
        query = """
        query GetWholeStoryContent($pratilipiId: ID!) {
          getPratilipiChapters(where: { pratilipiId: $pratilipiId }) {
            chapters {
              chapterNo
              title
              content(isFullContent: true)
            }
          }
        }
        """
        variables = {"pratilipiId": pratilipi_id}

        try:
            resp = self.session.post(
                GRAPHQL_URL,
                headers=GRAPHQL_HEADERS,
                json={"query": query, "variables": variables},
                timeout=timeout,
            )
            resp.raise_for_status()
        except requests.exceptions.RequestException as exc:
            print(f"GraphQL request failed: {exc}")
            return []

        data = resp.json()
        try:
            chapters = data["data"]["getPratilipiChapters"]["chapters"]
        except Exception:
            return []

        out = []
        for ch in chapters:
            out.append({
                "chapterNo": ch.get("chapterNo"),
                "title": ch.get("title"),
                "content": ch.get("content")
            })
        return out

    def _html_to_text(self, html: str) -> str:
        """Convert HTML to normalized plain text."""
        soup = BeautifulSoup(html or "", "html.parser")
        return "\n".join(
            line.strip()
            for line in soup.get_text("\n").splitlines()
            if line.strip()
        )

    # REST iterative fallback 
    def get_chapter_index(self, pratilipi_id: str) -> List[Dict[str, Any]]:
        url = f"{BASE_URL}/content/v1.0/contents/{pratilipi_id}/index"
        resp = self.session.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        # normalize shapes to list
        if isinstance(data, list):
            candidates = data
        elif isinstance(data, dict):
            candidates = data.get("chapters") or data.get("data") or data.get("items") or data.get("results")
            if candidates is None:
                for v in data.values():
                    if isinstance(v, list):
                        candidates = v
                        break
        else:
            candidates = []

        out = []
        for item in (candidates or []):
            if isinstance(item, dict):
                for key in ("chapterNo", "chapter_number", "chapterNumber", "number", "no"):
                    if key in item:
                        try:
                            out.append({"chapterNo": int(item[key])})
                            break
                        except Exception:
                            continue
        return out

    def fetch_chapter_content_by_number(self, pratilipi_id: str, chapter_no: int, convert_to_text: bool = True) -> str:
        """Fetch chapter content by pratilipiId + chapterNo (REST)."""
        url = f"{BASE_URL}/pratilipi/content"
        params = {"pratilipiId": pratilipi_id, "chapterNo": chapter_no, "_apiVer": 3}

        resp = self.session.get(url, params=params, timeout=10)
        if resp.status_code == 404:
            return ""
        resp.raise_for_status()

        try:
            data = resp.json()
            html = (data.get("data") or {}).get("html") or data.get("html") or data.get("content")
            if html:
                return self._html_to_text(html) if convert_to_text else html
            return self._html_to_text(resp.text) if convert_to_text else resp.text
        except ValueError:
            return self._html_to_text(resp.text) if convert_to_text else resp.text

    def get_whole_pratilipi_rest(self, pratilipi_id: str, max_workers: int = 6) -> List[Dict[str, Any]]:
        """Iteratively fetch all chapter numbers (index) and then fetch content concurrently."""
        index = self.get_chapter_index(pratilipi_id)
        if not index:
            return []

        chapter_numbers = [item["chapterNo"] for item in index]

        out: List[Dict[str, Any]] = []
        with ThreadPoolExecutor(max_workers=max_workers) as ex:
            futures = {ex.submit(self.fetch_chapter_content_by_number, pratilipi_id, no): no for no in chapter_numbers}
            for fut in as_completed(futures):
                no = futures[fut]
                try:
                    content = fut.result()
                except Exception as exc:
                    print(f"Failed to fetch chapter {no}: {exc}")
                    continue
                if not content:
                    print(f"Chapter {no} empty or not found; skipping")
                    continue
                out.append({"chapterNo": no, "content": content})
        # preserve ordering
        return sorted(out, key=lambda d: d["chapterNo"])

    # REST - per-pratilipi-id (when you have the chapter's pratilipiId)
    def fetch_chapter_content(self, chapter_pratilipi_id: str, convert_to_text: bool = True) -> str:
        """Fetches FULL chapter HTML using private REST API (by chapter pratilipi id).

        If convert_to_text is True, converts returned HTML to plain text.
        """
        url = f"{BASE_URL}/pratilipi/content"
        params = {
            "pratilipiId": chapter_pratilipi_id,
            "_apiVer": 3
        }

        resp = self.session.get(url, params=params, timeout=10)
        resp.raise_for_status()

        try:
            data = resp.json()
            html = data.get("data", {}).get("html") or data.get("content") or data.get("html")
            if html and convert_to_text:
                return self._html_to_text(html)
            return html or ""
        except ValueError:
            body = resp.text
            return self._html_to_text(body) if convert_to_text else body


