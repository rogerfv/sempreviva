from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

import pandas as pd

DB_PATH = Path("sempreviva.db")


@contextmanager
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def init_db() -> None:
    DB_PATH.touch(exist_ok=True)
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                amount REAL NOT NULL,
                type TEXT NOT NULL CHECK(type IN ('INCOME', 'EXPENSE')),
                category TEXT,
                subcategory TEXT,
                description TEXT,
                source_file TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS processed_files (
                filename TEXT PRIMARY KEY,
                upload_date TEXT DEFAULT CURRENT_TIMESTAMP,
                row_count INTEGER NOT NULL
            )
            """
        )
        conn.commit()


def record_processed_file(filename: str, row_count: int) -> None:
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO processed_files (filename, upload_date, row_count)
            VALUES (?, ?, ?)
            ON CONFLICT(filename) DO UPDATE SET
                upload_date=excluded.upload_date,
                row_count=excluded.row_count
            """,
            (filename, datetime.utcnow().isoformat(), row_count),
        )
        conn.commit()


def insert_transactions(rows: Iterable[Dict]) -> int:
    rows = list(rows)
    if not rows:
        return 0

    with get_connection() as conn:
        conn.executemany(
            """
            INSERT INTO transactions (
                date, amount, type, category, subcategory, description, source_file, created_at
            )
            VALUES (:date, :amount, :type, :category, :subcategory, :description, :source_file, :created_at)
            """,
            rows,
        )
        conn.commit()
    return len(rows)


def _date_filters(start_date: Optional[str], end_date: Optional[str]) -> Tuple[str, List[str]]:
    clauses: List[str] = []
    params: List[str] = []
    if start_date:
        clauses.append("date >= ?")
        params.append(start_date)
    if end_date:
        clauses.append("date <= ?")
        params.append(end_date)
    where = " WHERE " + " AND ".join(clauses) if clauses else ""
    return where, params


def fetch_transactions_df(
    start_date: Optional[str] = None, end_date: Optional[str] = None, txn_type: Optional[str] = None
) -> pd.DataFrame:
    where, params = _date_filters(start_date, end_date)
    if txn_type:
        where += " AND" if where else " WHERE"
        where += " type = ?"
        params.append(txn_type)

    query = f"SELECT * FROM transactions{where} ORDER BY date DESC, id DESC"
    with get_connection() as conn:
        df = pd.read_sql_query(query, conn, params=params, parse_dates=["date", "created_at"])
    return df


def get_totals(start_date: Optional[str] = None, end_date: Optional[str] = None) -> Dict[str, float]:
    where, params = _date_filters(start_date, end_date)
    query = f"""
        SELECT
            SUM(CASE WHEN type='INCOME' THEN amount ELSE 0 END) AS income,
            SUM(CASE WHEN type='EXPENSE' THEN amount ELSE 0 END) AS expenses
        FROM transactions{where}
    """
    with get_connection() as conn:
        row = conn.execute(query, params).fetchone()
    income = row["income"] or 0.0
    expenses = row["expenses"] or 0.0
    net = income - expenses
    margin = (net / income * 100) if income else 0.0
    return {"income": income, "expenses": expenses, "net": net, "margin": margin}


def get_monthly_totals(start_date: Optional[str] = None, end_date: Optional[str] = None) -> pd.DataFrame:
    where, params = _date_filters(start_date, end_date)
    query = f"""
        SELECT substr(date, 1, 7) AS month,
            SUM(CASE WHEN type='INCOME' THEN amount ELSE 0 END) AS income,
            SUM(CASE WHEN type='EXPENSE' THEN amount ELSE 0 END) AS expenses
        FROM transactions{where}
        GROUP BY month
        ORDER BY month
    """
    with get_connection() as conn:
        df = pd.read_sql_query(query, conn, params=params)
    return df


def get_breakdown(
    txn_type: str, group_by: str = "category", start_date: Optional[str] = None, end_date: Optional[str] = None
) -> pd.DataFrame:
    if group_by not in {"category", "subcategory"}:
        raise ValueError("group_by must be 'category' or 'subcategory'")

    where, params = _date_filters(start_date, end_date)
    where += " AND" if where else " WHERE"
    where += " type = ?"
    params.append(txn_type)

    query = f"""
        SELECT {group_by} AS label, SUM(amount) AS total
        FROM transactions{where}
        GROUP BY {group_by}
        ORDER BY total DESC
    """
    with get_connection() as conn:
        df = pd.read_sql_query(query, conn, params=params)
    return df


def get_date_bounds() -> Tuple[Optional[str], Optional[str]]:
    query = "SELECT MIN(date) as min_date, MAX(date) as max_date FROM transactions"
    with get_connection() as conn:
        row = conn.execute(query).fetchone()
    min_date = row["min_date"]
    max_date = row["max_date"]
    return min_date, max_date


def recent_files(limit: int = 10) -> List[sqlite3.Row]:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM processed_files ORDER BY upload_date DESC LIMIT ?", (limit,)
        ).fetchall()
    return rows


def clear_all() -> None:
    with get_connection() as conn:
        conn.execute("DELETE FROM transactions")
        conn.execute("DELETE FROM processed_files")
        conn.commit()

