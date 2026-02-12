from __future__ import annotations

import os
from typing import List


def tavily_search(query: str, max_results: int = 5) -> List[dict]:
    """Thin wrapper around TavilySearchResults.

    Returns list[dict] with keys like title/url/content/published_date depending on provider.
    """
    if not os.getenv("TAVILY_API_KEY"):
        return []

    from langchain_community.tools.tavily_search import TavilySearchResults  # type: ignore

    tool = TavilySearchResults(max_results=max_results)
    res = tool.invoke({"query": query})
    if isinstance(res, list):
        return res
    return []
