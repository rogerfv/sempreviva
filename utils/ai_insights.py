from __future__ import annotations

import json
import os
from typing import Any, Dict, Optional

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()


def _configure() -> Optional[str]:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None
    genai.configure(api_key=api_key)
    return api_key


def generate_insights(stats: Dict[str, Any]) -> Optional[str]:
    if not stats:
        return None

    api_key = _configure()
    if not api_key:
        return None

    prompt = (
        "Eres un analista financiero para una floristería. Resume los indicadores clave en 2-3 oraciones claras. "
        "Destaca tendencias positivas o riesgos, y menciona las categorías que más contribuyen."
    )

    content = {
        "totals": stats.get("totals"),
        "monthly_trend": stats.get("monthly_trend"),
        "top_income": stats.get("top_income"),
        "top_expenses": stats.get("top_expenses"),
    }

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content([prompt, json.dumps(content, default=str)])
        return response.text.strip() if response and response.text else None
    except Exception:
        return None

