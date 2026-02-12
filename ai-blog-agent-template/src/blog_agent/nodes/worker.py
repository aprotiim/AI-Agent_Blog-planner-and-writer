from __future__ import annotations

from typing import Dict, List, Tuple

from langchain_core.messages import SystemMessage, HumanMessage

from ..schemas import EvidenceItem, State, Task, Plan
from ..llm import llm


WORKER_SYSTEM = """You are a section-writing agent.

Write ONE blog section in Markdown.
- Start with: ## <Section Title>
- Follow with 2-6 short paragraphs and/or bullet lists as appropriate.
- If include_code=true, include a small code snippet.
- If requires_citations=true, cite only from the provided Evidence URLs (inline as (URL) or [n] style).
- Do NOT invent citations. If a needed citation is missing, explicitly say: 'Not found in provided sources.'
"""


def _evidence_block(evidence: List[EvidenceItem]) -> str:
    lines = []
    for i, e in enumerate(evidence[:15], start=1):
        date_s = f" | {e.published_at}" if e.published_at else ""
        lines.append(f"[{i}] {e.title}{date_s} - {e.url}")
    return "\n".join(lines)


def worker_node(payload: dict) -> dict:
    task = Task(**payload["task"])
    plan = Plan(**payload["plan"])
    evidence = [EvidenceItem(**e) for e in payload.get("evidence", [])]

    bullets_text = "\n- " + "\n- ".join(task.bullets)
    evidence_text = "\n".join(
        f"- {e.title} | {e.url} | {e.published_at or 'date:unknown'}"
        for e in evidence[:20]
    )

    section_md = llm.invoke(
        [
            SystemMessage(content=WORKER_SYSTEM),
            HumanMessage(
                content=(
                    f"Blog title: {plan.blog_title}\n"
                    f"Audience: {plan.audience}\n"
                    f"Tone: {plan.tone}\n"
                    f"Blog kind: {plan.blog_kind}\n"
                    f"Constraints: {plan.constraints}\n"
                    f"Topic: {payload['topic']}\n"
                    f"Mode: {payload.get('mode')}\n"
                    f"As-of: {payload.get('as_of')} (recency_days={payload.get('recency_days')})\n\n"
                    f"Section title: {task.title}\n"
                    f"Goal: {task.goal}\n"
                    f"Target words: {task.target_words}\n"
                    f"Tags: {task.tags}\n"
                    f"requires_research: {task.requires_research}\n"
                    f"requires_citations: {task.requires_citations}\n"
                    f"include_code: {task.include_code}\n"
                    f"Bullets:{bullets_text}\n\n"
                    f"Evidence (ONLY cite these URLs):\n{evidence_text}\n"
                )
            ),
        ]
    ).content.strip()

    return {"sections": [(task.id, section_md)]}

