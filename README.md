# AI-Agent_Blog-planner-and-writer
AI agent that plans before execution, decides when internet research is required, breaks tasks into parallel subtasks, uses multiple worker agents, adds citations and images automatically, and generates a complete blog end-to-end.
# AI Agent Blog Planner & Writer (LangGraph + Streamlit)

An agentic blog generator that **routes** (closed-book vs hybrid vs open-book), optionally **does web research**, creates a structured **plan**, writes sections via **parallel worker agents**, then **merges + optionally generates diagrams/images** and outputs a complete blog in Markdown.

Built with **LangGraph** (backend) and **Streamlit** (frontend UI).

---

## Demo (add these)
- 🎥 60–120s video (Loom/YouTube): topic → plan → evidence → final blog + images
- 🖼️ GIF/screenshot of the Streamlit app tabs (Plan / Evidence / Preview / Images / Logs)

---

## How it works

### Backend graph (LangGraph)
Pipeline:

1. **Router** decides if research is needed and sets mode:
   - `closed_book` (no research)
   - `hybrid` (research for up-to-date examples)
   - `open_book` (news/volatile topics; stricter recency filtering) :contentReference[oaicite:2]{index=2}

2. **Research (optional)** uses Tavily Search if `TAVILY_API_KEY` is set, extracts a deduplicated `EvidenceItem` list, and filters by recency for `open_book`. :contentReference[oaicite:3]{index=3}

3. **Orchestrator** creates a `Plan` with 5–9 tasks (each task has bullets, target words, flags like citations/code). :contentReference[oaicite:4]{index=4}

4. **Workers (fan-out)**: one worker per task writes a Markdown section starting with `## <Section Title>`. Workers cite ONLY provided evidence URLs when required. :contentReference[oaicite:5]{index=5}

5. **Reducer + Images (subgraph)**:
   - merges sections into one blog
   - decides whether images/diagrams are needed (max 3) using placeholders `[[IMAGE_1]]...`
   - generates images via **Gemini image model** (if `GOOGLE_API_KEY` is set), saves to `images/`, and replaces placeholders with Markdown image links + captions. :contentReference[oaicite:6]{index=6}

The final Markdown is also saved to a local file named from the blog title (slugified). :contentReference[oaicite:7]{index=7}

### Frontend (Streamlit)
`bwa_frontend.py` loads the compiled LangGraph app (`from bwa_backend import app`) and provides:
- Sidebar topic input + “Generate Blog”
- Tabs:
  - **Plan** (tasks table)
  - **Evidence** (URLs + dates)
  - **Markdown Preview** (renders local images)
  - **Images** (shows `images/` files + zip download)
  - **Logs** (graph stream/invoke logs) :contentReference[oaicite:8]{index=8} :contentReference[oaicite:9]{index=9}

It also supports loading **past saved blogs** (`*.md` in the current directory) directly in the UI. :contentReference[oaicite:10]{index=10}

---

## Features

- ✅ Route-first decision: closed-book vs hybrid vs open-book :contentReference[oaicite:11]{index=11}
- ✅ Optional web research via Tavily + evidence extraction + recency filter for news mode :contentReference[oaicite:12]{index=12}
- ✅ Structured planning with Pydantic schemas (`Plan`, `Task`, `EvidenceItem`) :contentReference[oaicite:13]{index=13}
- ✅ Parallel section writing with LangGraph fan-out workers :contentReference[oaicite:14]{index=14}
- ✅ Optional image/diagram planning + generation + insertion into Markdown :contentReference[oaicite:15]{index=15}
- ✅ Streamlit UI with downloads (Markdown and bundle zip with images) :contentReference[oaicite:16]{index=16}

---

## Requirements

- Python 3.10+ recommended
- API keys (optional but unlock features):
  - `OPENAI_API_KEY` (required for text generation via `ChatOpenAI`) :contentReference[oaicite:17]{index=17}
  - `TAVILY_API_KEY` (optional: web research evidence) :contentReference[oaicite:18]{index=18}
  - `GOOGLE_API_KEY` (optional: image generation via Gemini) :contentReference[oaicite:19]{index=19}

---

## Quickstart

### 1) Create venv + install deps
```bash
python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows
.venv\Scripts\activate

pip install -U pip
pip install -r requirements.txt
