from __future__ import annotations

import os
from pathlib import Path


def generate_image(prompt: str, out_path: Path) -> None:
    """Generate an image with Gemini and save it to out_path.

    Requires:
      - pip install google-genai
      - GOOGLE_API_KEY
    """
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError("GOOGLE_API_KEY is not set.")

    from google import genai  # type: ignore
    from google.genai import types  # type: ignore

    client = genai.Client(api_key=api_key)

    # Model used in your original script
    model = "gemini-2.0-flash-exp-image-generation"

    resp = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_modalities=["TEXT", "IMAGE"]
        ),
    )

    # Find first image in response
    img_bytes = None
    for cand in getattr(resp, "candidates", []) or []:
        for part in getattr(cand, "content", {}).parts if hasattr(getattr(cand, "content", None), "parts") else []:
            if getattr(part, "inline_data", None) and getattr(part.inline_data, "data", None):
                img_bytes = part.inline_data.data
                break
        if img_bytes:
            break

    if not img_bytes:
        raise RuntimeError("No image returned from Gemini.")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(img_bytes)
