# Sempreviva – Supplier Risk Dashboard

## Overview
This repository contains a packaged Streamlit dashboard used to analyze Sempreviva's income and expense data. The app ingests monthly Excel files, stores uploads in a local SQLite database, and renders KPI summaries, breakdowns, trends, and period comparisons. An optional Google Gemini integration can generate narrative insights when an API key is supplied in the UI.

## Features
- Upload monthly income and expense Excel (`.xlsx`) files and store them in SQLite.
- Financial KPIs for income, expenses, profit, and margin.
- Breakdowns by income category/channel and expense type (fixed/variable).
- Interactive charts, tables, and trend views.
- Period comparison (month/quarter/year) with deltas.
- Optional AI-generated insights via Google Gemini (key entered in the sidebar).

## Repository Structure
```
.
├─ README.md
├─ Sempreviva_Dashboard.zip         # Packaged app delivery
└─ (inside Sempreviva_Dashboard.zip)
   ├─ app.py                        # Streamlit application
   ├─ requirements.txt              # Python dependencies
   ├─ financial_data.db             # SQLite database used by the app
   ├─ dashboard.bat                 # Windows launcher (visible console)
   ├─ dashboard.vbs                 # Windows launcher (hidden console)
   └─ README.txt                    # Quick run instructions
```

## Tech Stack
- Streamlit
- Pandas, NumPy
- Plotly, Matplotlib
- SQLite (via Python stdlib `sqlite3`)
- OpenPyXL (Excel reader)
- Google Generative AI (Gemini)

## Getting Started
### Prerequisites
- Python 3.x (version not pinned in this export)
- Windows is assumed for the provided launchers (`dashboard.bat` / `dashboard.vbs`)

### Installation
1. Extract `Sempreviva_Dashboard.zip` into a working folder.
2. Create and activate a virtual environment (recommended):
```bash
python -m venv .venv
.\.venv\Scripts\activate
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Configuration
- There is no `.env` or config file in this export.
- If you want AI insights, enter your Google Gemini API key in the app sidebar when prompted.

### Running the App
From the extracted folder:
```bash
python -m streamlit run app.py --server.port 8501 --browser.gatherUsageStats false
```
Or on Windows, double-click:
- `dashboard.vbs` (runs hidden)
- `dashboard.bat` (runs with a console window)

The app will be available at `http://localhost:8501`.

## Data / Inputs
The app expects monthly Excel files (`.xlsx`) for income and expenses.

Income files
- Must include a `Tags` column.
- Amount column is auto-detected (tries common headers like `Total`, `Importe`, `Amount`, etc.).
- Optional columns used when present: `Estado`, `Descripción`.

Expense files
- Must include a `Cuenta` column.
- Amount column is auto-detected (same logic as income files).
- Optional columns used when present: `Estado`.

File naming
- If filenames follow the pattern `Ingresos dd_mm_yyyy-dd_mm_yyyy` or `Compras dd_mm_yyyy-dd_mm_yyyy`, the month label is derived from the name.
- Otherwise, the filename is used as the period label.

Storage
- Uploaded files are stored in `financial_data.db` (SQLite) inside the extracted folder.

## Scripts & Utilities
- `dashboard.bat`: Activates `.venv`, opens a browser, and runs Streamlit on port 8501.
- `dashboard.vbs`: Launches `dashboard.bat` with the console hidden.

## Testing & Quality
Not included in this export.

## Deployment
No deployment artifacts are included. Run locally with Streamlit, or package for your target environment as needed.

## Troubleshooting
- App does not open: ensure the ZIP is fully extracted and run `dashboard.bat` once to see errors.
- Missing columns: income files require `Tags`; expense files require `Cuenta`.
- Port conflict: stop other services on 8501 or change the port in the run command.
- AI insights disabled: enter a valid Gemini API key in the sidebar.

## Security / Secrets
Do not commit API keys or sensitive data. The Gemini key is entered at runtime in the UI and should be handled as a secret.

## License / Client Delivery Note
No license file is included in this export. This repository appears to be a client delivery package.
