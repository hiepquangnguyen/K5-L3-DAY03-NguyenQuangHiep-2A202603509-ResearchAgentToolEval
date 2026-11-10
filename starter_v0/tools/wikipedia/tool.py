from __future__ import annotations

import urllib.parse
from typing import Any
import requests

from tools._shared import TIMEOUT, err


def search_wikipedia(query: str = "") -> dict[str, Any]:
    """Tra cứu tóm tắt bách khoa toàn thư từ Wikipedia REST API."""
    query = (query or "").strip()
    if not query:
        return {
            "tool": "search_wikipedia",
            "query": query,
            "title": "",
            "summary": "Vui lòng cung cấp từ khóa cần tra cứu trên Wikipedia.",
            "url": "",
        }

    try:
        encoded_title = urllib.parse.quote(query.replace(" ", "_"))
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{encoded_title}"
        headers = {
            "User-Agent": "AI20k-Research-Agent/1.0 (educational lab)"
        }
        
        response = requests.get(url, headers=headers, timeout=TIMEOUT)
        if response.status_code == 404:
            return {
                "tool": "search_wikipedia",
                "query": query,
                "title": "",
                "summary": f"Không tìm thấy bài viết Wikipedia nào khớp với từ khóa '{query}'.",
                "url": "",
            }
        
        response.raise_for_status()
        data = response.json()
        
        return {
            "tool": "search_wikipedia",
            "query": query,
            "title": data.get("title", ""),
            "summary": data.get("extract", ""),
            "url": data.get("content_urls", {}).get("desktop", {}).get("page", ""),
        }
    except Exception as exc:
        return err("search_wikipedia", exc)