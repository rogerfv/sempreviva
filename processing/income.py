from __future__ import annotations

from datetime import datetime
from typing import Dict, List, Tuple

import pandas as pd

PRODUCT_TAGS: Dict[str, List[str]] = {
    "Novias": ["novia", "nuvies", "bride"],
    "Eventos": ["evento", "event"],
    "Cumpleaños": ["cumple", "birthday"],
    "Funerales": ["funeral", "condolencia"],
    "Corporativo": ["empresa", "corporate", "b2b"],
    "Regalos": ["regalo", "gift"],
}

CHANNEL_TAGS: Dict[str, List[str]] = {
    "Instagram": ["instagram", "ig"],
    "Tienda": ["tienda", "store", "local"],
    "Web": ["web", "online", "shop"],
    "WhatsApp": ["whatsapp", "wasap", "ws"],
    "Referidos": ["referido", "referal", "recomendacion", "recomendación"],
}

AMOUNT_COLUMNS = ["amount", "importe", "total", "valor", "precio", "monto"]


def _find_column(df: pd.DataFrame, candidates: List[str]) -> str:
    cols = {col.lower(): col for col in df.columns}
    for candidate in candidates:
        if candidate in cols:
            return cols[candidate]
    raise ValueError(f"Required column not found. Expected one of: {candidates}")


def _normalize(text) -> str:
    return str(text).lower() if pd.notna(text) else ""


def _map_from_tags(text: str, mapping: Dict[str, List[str]], default: str) -> str:
    lower_text = _normalize(text)
    for label, keywords in mapping.items():
        for keyword in keywords:
            if keyword in lower_text:
                return label
    return default


def categorize_income_row(tags: str) -> Tuple[str, str]:
    category = _map_from_tags(tags, PRODUCT_TAGS, default="Otros")
    channel = _map_from_tags(tags, CHANNEL_TAGS, default="Otros")
    return category, channel


def detect_amount_column(df: pd.DataFrame) -> str:
    try:
        return _find_column(df, AMOUNT_COLUMNS)
    except ValueError:
        numeric_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
        if len(numeric_cols) == 1:
            return numeric_cols[0]
        raise


def process_income(file, filename: str) -> Tuple[pd.DataFrame, List[Dict]]:
    df = pd.read_excel(file)

    amount_col = detect_amount_column(df)
    tags_col = _find_column(df, ["tags", "etiquetas", "tag"])
    desc_col = _find_column(df, ["descripcion", "descripción", "description", "concepto"])
    date_col_candidates = {c.lower(): c for c in df.columns if "fecha" in c.lower() or "date" == c.lower()}
    date_col = date_col_candidates.get("fecha") or date_col_candidates.get("date")

    df["amount"] = pd.to_numeric(df[amount_col], errors="coerce").fillna(0)
    df["description"] = df[desc_col].fillna("")
    df["tags"] = df[tags_col].fillna("")
    if date_col:
        df["date"] = pd.to_datetime(df[date_col], errors="coerce").dt.date
    else:
        df["date"] = pd.Timestamp.today().date()

    df[["category", "channel"]] = df.apply(
        lambda row: pd.Series(categorize_income_row(row["tags"])), axis=1
    )

    records: List[Dict] = []
    for _, row in df.iterrows():
        records.append(
            {
                "date": row["date"].isoformat() if hasattr(row["date"], "isoformat") else str(row["date"]),
                "amount": float(row["amount"]),
                "type": "INCOME",
                "category": row.get("category"),
                "subcategory": row.get("channel"),
                "description": str(row.get("description", "")),
                "source_file": filename,
                "created_at": datetime.utcnow().isoformat(),
            }
        )

    return df, records

