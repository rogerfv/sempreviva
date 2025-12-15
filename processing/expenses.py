from __future__ import annotations

from datetime import datetime
from typing import Dict, List, Tuple

import pandas as pd

EXPENSE_TAGS: Dict[str, List[str]] = {
    "Alquiler del local": ["alquiler", "renta", "lloguer"],
    "Sueldos y honorarios": ["nomina", "nómina", "sueldo", "salario", "honorario"],
    "Servicios": ["luz", "agua", "internet", "gas", "energia", "energía"],
    "Marketing": ["ads", "facebook", "instagram ads", "publicidad", "marketing"],
    "Transporte y envíos": ["envio", "envío", "envios", "envíos", "transporte", "courier", "glovo", "uber"],
    "Materiales": ["material", "suministro", "herramienta"],
    "Flores y verdes": ["flor", "rosa", "tallo", "verde", "ramo", "floral"],
    "Empaques y packaging": ["caja", "bolsa", "papel", "packaging", "envoltorio"],
    "Impuestos y tasas": ["impuesto", "iva", "tasas", "tributo"],
    "Otros": [],
}

FIXED_CATEGORIES = {
    "Alquiler del local",
    "Sueldos y honorarios",
    "Servicios",
    "Marketing",
    "Impuestos y tasas",
}

VARIABLE_CATEGORIES = {
    "Transporte y envíos",
    "Materiales",
    "Flores y verdes",
    "Empaques y packaging",
    "Otros",
}

AMOUNT_COLUMNS = ["amount", "importe", "total", "valor", "monto"]


def _find_column(df: pd.DataFrame, candidates: List[str]) -> str:
    cols = {col.lower(): col for col in df.columns}
    for candidate in candidates:
        if candidate in cols:
            return cols[candidate]
    raise ValueError(f"Required column not found. Expected one of: {candidates}")


def _normalize(text) -> str:
    return str(text).lower() if pd.notna(text) else ""


def _map_category(account: str) -> Tuple[str, str]:
    normalized = _normalize(account)
    for label, keywords in EXPENSE_TAGS.items():
        for keyword in keywords:
            if keyword in normalized:
                return label, _group_for_category(label)
    return "Otros", _group_for_category("Otros")


def _group_for_category(category: str) -> str:
    if category in FIXED_CATEGORIES:
        return "Fijo"
    if category in VARIABLE_CATEGORIES:
        return "Variable"
    return "Variable"


def detect_amount_column(df: pd.DataFrame) -> str:
    try:
        return _find_column(df, AMOUNT_COLUMNS)
    except ValueError:
        numeric_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
        if len(numeric_cols) == 1:
            return numeric_cols[0]
        raise


def process_expenses(file, filename: str) -> Tuple[pd.DataFrame, List[Dict]]:
    df = pd.read_excel(file)

    amount_col = detect_amount_column(df)
    account_col = _find_column(df, ["cuenta", "account", "categoria", "categoría"])
    desc_col_candidates = {c.lower(): c for c in df.columns if "descripcion" in c.lower() or "descripción" in c.lower()}
    desc_col = desc_col_candidates.get("descripcion") or desc_col_candidates.get("descripción") or account_col
    date_col_candidates = {c.lower(): c for c in df.columns if "fecha" in c.lower() or "date" == c.lower()}
    date_col = date_col_candidates.get("fecha") or date_col_candidates.get("date")

    df["amount"] = pd.to_numeric(df[amount_col], errors="coerce").fillna(0)
    df["description"] = df[desc_col].fillna("")
    df["account"] = df[account_col].fillna("")
    if date_col:
        df["date"] = pd.to_datetime(df[date_col], errors="coerce").dt.date
    else:
        df["date"] = pd.Timestamp.today().date()

    df[["category", "group"]] = df.apply(lambda row: pd.Series(_map_category(row["account"])), axis=1)

    records: List[Dict] = []
    for _, row in df.iterrows():
        records.append(
            {
                "date": row["date"].isoformat() if hasattr(row["date"], "isoformat") else str(row["date"]),
                "amount": float(row["amount"]),
                "type": "EXPENSE",
                "category": row.get("category"),
                "subcategory": row.get("group"),
                "description": str(row.get("description", "")),
                "source_file": filename,
                "created_at": datetime.utcnow().isoformat(),
            }
        )

    return df, records

