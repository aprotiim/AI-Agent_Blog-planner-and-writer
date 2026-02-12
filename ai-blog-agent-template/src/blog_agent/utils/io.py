from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

from ..config import BLOGS_DIR, EVIDENCE_DIR, IMAGES_DIR, PLANS_DIR


_slug_re = re.compile(r"[^a-zA-Z0-9]+")


def slugify(text: str) -> str:
    slug = _slug_re.sub("-", text).strip("-").lower()
    return slug[:80] if slug else "blog"


def save_json(obj: Any, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False))


def save_markdown(md: str, title: str) -> Path:
    filename = f"{slugify(title)}.md"
    out = BLOGS_DIR / filename
    out.write_text(md, encoding="utf-8")
    return out


def list_saved_blogs() -> List[Path]:
    return sorted(BLOGS_DIR.glob("*.md"))


def read_markdown(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def outputs_paths() -> Dict[str, Path]:
    return {
        "blogs": BLOGS_DIR,
        "plans": PLANS_DIR,
        "evidence": EVIDENCE_DIR,
        "images": IMAGES_DIR,
    }
