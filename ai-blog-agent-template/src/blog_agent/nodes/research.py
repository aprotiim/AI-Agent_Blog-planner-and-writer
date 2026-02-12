from __future__ import annotations

from datetime import date, timedelta
from typing import Dict, List

from ..config import SETTINGS
from ..schemas import EvidenceItem, State
from ..tools.tavily_search import tavily_search


def _parse_date(s: str) -> date | None:
    try:
        return date.fromisoformat(s[:10])
    except Exception:
        return None


def _dedupe_by_url(items: List[EvidenceItem]) -> List[EvidenceItem]:
    seen = set()
    out: List[EvidenceItem] = []
    for it in items:
        if it.url in seen:
            continue
        seen.add(it.url)
        out.append(it)
    return out


def research_node(state: State) -> Dict:
    if not state.get("needs_research"):
        return {"evidence": []}

    if not SETTINGS.has_tavily:
        # Research requested but tool not configured
        return {"evidence": []}

    queries = state.get("queries") or [state["topic"]]
    raw: List[dict] = []
    for q in queries:
        raw.extend(tavily_search(q, max_results=6))

    evidence: List[EvidenceItem] = []
    for r in raw:
        evidence.append(
            EvidenceItem(
                title=r.get("title") or r.get("name") or "Untitled",
                url=r.get("url") or "",
                snippet=r.get("content") or r.get("snippet"),
                published_at=r.get("published_date") or r.get("published_at"),
                source=r.get("source"),
            )
        )

    evidence = [e for e in evidence if e.url]
    evidence = _dedupe_by_url(evidence)

    # Open-book recency filter
    mode = state.get("mode", "hybrid")
    if mode == "open_book":
        as_of = _parse_date(state.get("as_of") or str(date.today())) or date.today()
        cutoff = as_of - timedelta(days=int(state.get("recency_days", SETTINGS.open_book_max_age_days)))
        filtered: List[EvidenceItem] = []
        for e in evidence:
            if e.published_at:
                d = _parse_date(e.published_at)
                if d and d >= cutoff:
                    filtered.append(e)
            else:
                # keep undated items, but they may be lower quality
                filtered.append(e)
        evidence = filtered

    return {"evidence": evidence}
