from __future__ import annotations

import csv
import json
import time
from pathlib import Path

from blog_agent.graph import app

PROMPTS = Path(__file__).parent / "prompts.jsonl"
OUT = Path(__file__).parent / "results.csv"


def load_prompts():
    if not PROMPTS.exists():
        return ["Explain transformers to LLM training pipeline."]
    prompts = []
    for line in PROMPTS.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        prompts.append(json.loads(line)["prompt"])
    return prompts


def main():
    prompts = load_prompts()
    rows = []
    for p in prompts:
        init = {
            "topic": p,
            "mode": "hybrid",
            "needs_research": False,
            "queries": [],
            "evidence": [],
            "plan": None,
            "as_of": "2026-02-11",
            "recency_days": 120,
            "sections": [],
            "merged_md": "",
            "md_with_placeholders": "",
            "image_specs": [],
            "final": "",
        }
        t0 = time.time()
        out = app.invoke(init)
        dt = time.time() - t0
        final = out.get("final", "")
        rows.append({
            "prompt": p,
            "latency_s": round(dt, 3),
            "chars": len(final),
            "citations_guess": final.count("http"),
        })

    with OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(rows)

    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
