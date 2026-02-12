from __future__ import annotations

from langchain_openai import ChatOpenAI
from .config import SETTINGS

# Centralized LLM client
llm = ChatOpenAI(model=SETTINGS.openai_model)
