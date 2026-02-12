from __future__ import annotations

from typing import Dict

from langchain_core.messages import SystemMessage, HumanMessage

from ..schemas import Plan, State
from ..llm import llm


PLANNER_SYSTEM = """You are a senior technical editor.
Create a blog plan as JSON matching this schema:

Plan = {
  "blog_title": str,
  "audience": str,
  "tone": str,
  "blog_kind": "explainer" | "tutorial" | "news_roundup" | "comparison" | "system_design",
  "constraints": [str],
  "tasks": [
    {
      "id": int,
      "title": str,
      "goal": str,
      "bullets": [str]  # 3-6,
      "target_words": int,  # 120-550
      "tags": [str],
      "requires_research": bool,
      "requires_citations": bool,
      "include_code": bool
    }
  ]
}

Rules:
- Produce 5-9 tasks.
- Each task must be specific and lead to a section starting with '## <title>'.
- If evidence exists, set requires_citations=true for tasks with factual claims.
"""


def orchestrator_node(state: State) -> dict:
    planner = llm.with_structured_output(Plan)
    mode = state.get("mode", "closed_book")
    evidence = state.get("evidence", [])

    forced_kind = "news_roundup" if mode == "open_book" else None

    plan = planner.invoke(
        [
            SystemMessage(content=PLANNER_SYSTEM),
            HumanMessage(
                content=(
                    f"Topic: {state['topic']}\n"
                    f"Mode: {mode}\n"
                    f"As-of: {state['as_of']} (recency_days={state['recency_days']})\n"
                    f"{'Force blog_kind=news_roundup' if forced_kind else ''}\n\n"
                    f"Evidence:\n{[e.model_dump() for e in evidence][:16]}"
                )
            ),
        ]
    )
    if forced_kind:
        plan.blog_kind = "news_roundup"

    return {"plan": plan}
