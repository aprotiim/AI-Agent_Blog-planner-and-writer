from __future__ import annotations

from typing import Dict, List, Tuple

from langchain_core.messages import SystemMessage, HumanMessage

from ..schemas import ImageSpec, Plan, State
from ..config import IMAGES_DIR
from ..tools.image_gen import generate_image
from ..utils.io import save_markdown
from ..llm import llm


MERGE_SYSTEM = """You are an expert technical editor.
Merge the provided sections into a cohesive blog post.
- Add an H1 title as the first line.
- Keep section headings as H2.
- Ensure smooth transitions and consistent voice.
Return Markdown only.
"""

IMAGE_DECIDER_SYSTEM = """You are an assistant that decides if diagrams/images would improve clarity.
Given a blog in Markdown, propose up to 3 images.

Return JSON list[ImageSpec] with:
- placeholder: [[IMAGE_1]], [[IMAGE_2]], ...
- filename: short, safe, ends with .png
- alt: str
- caption: str
- prompt: detailed prompt for generating the image/diagram
If no images are needed, return [].
"""


def merge_node(state: State) -> Dict:
    plan: Plan = state["plan"]  # type: ignore
    sections: List[Tuple[int, str]] = sorted(state.get("sections") or [], key=lambda x: x[0])
    merged = "\n\n".join([s for _, s in sections])

    msg = [
        SystemMessage(content=MERGE_SYSTEM),
        HumanMessage(content=f"Blog title: {plan.blog_title}\n\nSections:\n{merged}")
    ]
    resp = llm.invoke(msg)
    return {"merged_md": resp.content}


def decide_images_node(state: State) -> Dict:
    msg = [
        SystemMessage(content=IMAGE_DECIDER_SYSTEM),
        HumanMessage(content=state.get("merged_md", ""))
    ]
    resp = llm.invoke(msg)
    try:
        specs = [ImageSpec.model_validate(x).model_dump() for x in __import__("json").loads(resp.content)]
    except Exception:
        specs = []
    return {"image_specs": specs}


def generate_and_place_images_node(state: State) -> Dict:
    md = state.get("merged_md", "")
    specs = state.get("image_specs") or []

    # insert placeholders near relevant sections (simple: append near end of doc)
    md_with = md
    for spec in specs:
        placeholder = spec.get("placeholder", "")
        caption = spec.get("caption", "")
        alt = spec.get("alt", "")
        filename = spec.get("filename", "image.png")
        md_with += f"\n\n{placeholder}\n\n*{caption}*\n"

        # generate image (best-effort)
        try:
            generate_image(spec.get("prompt", ""), IMAGES_DIR / filename)
            md_with = md_with.replace(placeholder, f"![{alt}](images/{filename})")
        except Exception:
            md_with = md_with.replace(placeholder, f"**[Image generation skipped/failed]**")

    # Save blog
    plan = state.get("plan")
    title = plan.blog_title if plan else "blog"
    out_path = save_markdown(md_with, title)

    return {"final": md_with}
