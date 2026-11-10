from __future__ import annotations

from typing import Any

from tools._shared import TIMEOUT, domain, err


def duckduckgo_search(query: str = "", topic: str = "general", timeframe: str | None = None, max_results: int = 5) -> dict[str, Any]:
    """Search DuckDuckGo without an API key, as a fallback for lookup."""
    try:
        if not isinstance(query, str) or not query.strip():
            raise ValueError("query must be a non-empty string")
        if topic not in ("general", "news"):
            raise ValueError("topic must be general or news")
        time_limits = {None: None, "day": "d", "week": "w", "month": "m"}
        if timeframe not in time_limits:
            raise ValueError("timeframe must be day, week, month or null")
        if isinstance(max_results, bool) or not isinstance(max_results, int) or not 1 <= max_results <= 10:
            raise ValueError("max_results must be an integer from 1 to 10")

        # Lazy import keeps other tools usable before optional dependencies are installed.
        from ddgs import DDGS

        client = DDGS(timeout=TIMEOUT)
        search = client.news if topic == "news" else client.text
        results = search(query.strip(), backend="duckduckgo", timelimit=time_limits[timeframe], max_results=max_results)
        items = []
        for raw in results:
            url = raw.get("url") or raw.get("href") or ""
            if not isinstance(url, str) or not url.startswith(("https://", "http://")):
                continue
            items.append({
                "title": raw.get("title", ""), "url": url,
                "source": domain(url), "summary": raw.get("body", ""),
                "date": raw.get("date"),
            })
            if len(items) == max_results:
                break
        return {"tool": "duckduckgo_search", "query": query.strip(), "topic": topic,
                "timeframe": timeframe, "items": items}
    except Exception as exc:
        return err("duckduckgo_search", exc)
