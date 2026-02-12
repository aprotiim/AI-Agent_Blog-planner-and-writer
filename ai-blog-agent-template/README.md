# AI Agent Blog Planner & Writer (LangGraph + Streamlit)

An agentic blog generator that **routes** (closed-book vs hybrid vs open-book), optionally **does web research**, creates a structured **plan**, writes sections via **parallel worker agents**, then **merges + optionally generates diagrams/images** and outputs a complete blog in Markdown.

Built with **LangGraph** (backend graph) and **Streamlit** (frontend UI).

## Demo
- Add a 60–120s video (Loom/YouTube) of: topic → plan → evidence → final blog (+ images)
- Add screenshots/GIFs under `examples/screenshots/`

## Features
- Route-first decision: `closed_book` vs `hybrid` vs `open_book`
- Optional web research via Tavily (evidence extraction + recency filtering for `open_book`)
- Structured planning with Pydantic schemas (`Plan`, `Task`, `EvidenceItem`)
- Parallel section writing using LangGraph fan-out workers
- Optional image/diagram planning + generation (Gemini) + placeholder replacement in Markdown
- Streamlit UI: Plan / Evidence / Preview / Images / Logs + download markdown/zip

## Repository layout
- `app/streamlit_app.py` — Streamlit UI
- `src/blog_agent/` — core agent package (schemas, graph builder, nodes, tools)
- `outputs/` — generated artifacts (blogs/plans/evidence/images)
- `examples/` — sample outputs and screenshots for recruiters
- `tests/` — unit tests
- `eval/` — simple batch evaluation script

## Requirements
- Python 3.10+
- API keys:
  - `OPENAI_API_KEY` (required for text generation)
  - `TAVILY_API_KEY` (optional: web research evidence)
  - `GOOGLE_API_KEY` (optional: image generation via Gemini)

## Quickstart

### 1) Create venv + install
```bash
python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows
.venv\Scripts\activate

pip install -U pip
pip install -r requirements.txt
```

### 2) Configure env
Copy `.env.example` to `.env` and fill in keys.

### 3) Run the app
```bash
streamlit run app/streamlit_app.py
```

## Outputs
- Blogs: `outputs/blogs/*.md`
- Plans: `outputs/plans/*.json`
- Evidence: `outputs/evidence/*.json`
- Images: `outputs/images/*` (if enabled)

## Notes for recruiters
If you don’t want to run the project, check:
- `examples/example_blog.md`
- `examples/example_plan.json`
- `examples/example_evidence.json`
- screenshots under `examples/screenshots/`

## License
Add a `LICENSE` file (MIT recommended for portfolios).
