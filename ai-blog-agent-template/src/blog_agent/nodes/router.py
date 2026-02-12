from __future__ import annotations

from datetime import date
from typing import Dict

from langchain_core.messages import SystemMessage, HumanMessage

from ..schemas import RouterDecision, State
from ..llm import llm


ROUTER_SYSTEM = """You are a routing agent for a blog-writing system.
Given a topic and an as-of date, decide whether web research is needed.

Return JSON matching this schema:
{{
  "needs_research": bool,
  "mode": "closed_book" | "hybrid" | "open_book",
  "reason": str,
  "queries": [str],
  "max_results_per_query": int
}}

Guidance:
- closed_book: stable evergreen topics; no need for up-to-date info
- hybrid: mostly evergreen but wants recent examples/stats; limited research ok
- open_book: news/rapidly changing topics or requests for latest; must research
"""


def route_node(state: State) -> Dict:
    topic = state["topic"]
    as_of = state.get("as_of") or str(date.today())

    msg = [
        SystemMessage(content=ROUTER_SYSTEM),
        HumanMessage(content=f"Topic: {topic}\nAs-of date: {as_of}\nReturn only valid JSON.")
    ]
    resp = llm.invoke(msg)
    decision = RouterDecision.model_validate_json(resp.content)

    return {
        "needs_research": decision.needs_research,
        "mode": decision.mode,
        "queries": decision.queries,
    }
def route_next(state: State) -> str:
    return "research" if state["needs_research"] else "orchestrator"