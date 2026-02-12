from __future__ import annotations

from pathlib import Path
import re

_IMG_MD = re.compile(r"!\[(.*?)\]\((.*?)\)")


def rewrite_image_paths(md: str, images_dir: Path) -> str:
    """Make image links resolvable for Streamlit by converting relative paths."""
    def repl(m: re.Match) -> str:
        alt, path = m.group(1), m.group(2)
        p = Path(path)
        if p.is_absolute():
            return m.group(0)
        # assume stored under outputs/images
        new_path = str((images_dir / p.name).resolve())
        return f"![{alt}]({new_path})"
    return _IMG_MD.sub(repl, md)
