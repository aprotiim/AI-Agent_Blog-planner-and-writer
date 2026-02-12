from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
BLOGS_DIR = OUTPUTS_DIR / "blogs"
PLANS_DIR = OUTPUTS_DIR / "plans"
EVIDENCE_DIR = OUTPUTS_DIR / "evidence"
IMAGES_DIR = OUTPUTS_DIR / "images"

for d in (BLOGS_DIR, PLANS_DIR, EVIDENCE_DIR, IMAGES_DIR):
    d.mkdir(parents=True, exist_ok=True)


@dataclass(frozen=True)
class Settings:
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
    open_book_max_age_days: int = int(os.getenv("OPEN_BOOK_MAX_AGE_DAYS", "120"))

    @property
    def has_tavily(self) -> bool:
        return bool(os.getenv("TAVILY_API_KEY"))

    @property
    def has_gemini(self) -> bool:
        return bool(os.getenv("GOOGLE_API_KEY"))


SETTINGS = Settings()
