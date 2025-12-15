# Sempreviva Financial Dashboard Implementation Plan

## Overview
A web application to replace manual Excel/Notebook processing. Users can upload income/expense files, which are processed to generate interactive dashboards showing earnings, trends, and expense breakdowns.

## Current State Analysis
- **Logic:** Currently locked in Jupyter notebooks (`ingressos_code.ipynb`, `compres_code.ipynb`).
- **Data:** Input via specific Excel formats.
- **Rules:** Hardcoded Python lists + `Documento_Reglas_GPT.docx`.
- **UI:** None (Manual execution).

## Desired End State
- **Interface:** Web-based dashboard.
- **Input:** Drag-and-drop file upload.
- **Processing:** Server-side execution of existing categorization logic.
- **Visualization:** Interactive charts (replacing static Excel output).

## Architecture Decisions
- **Tech Stack:** Streamlit (Python)
  - **Why:** Direct reuse of existing pandas logic, fastest delivery, excellent for data apps.
- **Deployment:** Local execution (User runs `streamlit run app.py`)
- **Authentication:** None (Local access only)
- **Data Persistence:** SQLite Database (`sempreviva.db`)
  - **Why:** Zero-configuration, local file-based, supports SQL queries for analytics, perfect for "auto-save" requirement.
  - **Mechanism:** Uploaded files are processed -> cleaned data inserted into SQLite -> Dashboard queries SQLite.
- **AI Integration:** Google Gemini API (via `google-generativeai`)
  - **Purpose:** Automated executive summaries and trend analysis.
  - **Privacy:** Only aggregated stats sent to API.

## Project Structure
```
sempreviva/
├── app.py                  # Main Streamlit entry point
├── requirements.txt        # Dependencies (streamlit, pandas, google-generativeai)
├── .env.example            # Template for env vars (GEMINI_API_KEY)
├── database.py             # SQLite connection and queries
├── processing/
│   ├── __init__.py
│   ├── income.py           # Ported logic from ingressos_code.ipynb
│   └── expenses.py         # Ported logic from compres_code.ipynb
├── ui/
│   ├── __init__.py
│   ├── dashboard.py        # Main dashboard layout
│   ├── income_page.py      # Income view
│   ├── expense_page.py     # Expense view
│   └── upload_page.py      # File upload & processing
└── utils/
    ├── __init__.py
    ├── ai_insights.py      # Gemini API integration
    └── charts.py           # Plotly/Altair chart definitions
```

## Data Processing Logic

### Income Processing (Source: `ingressos_code.ipynb`)
- **Input:** Excel files with `Tags`, `Descripción`, and an Amount column.
- **Categorization:**
  - **Product Category:** Derived from `Tags` via substring matching (e.g., "nuvies" -> "Novias").
  - **Sales Channel:** Derived from `Tags` via substring matching (e.g., "instagram" -> "Instagram").
- **Metrics:** Total Income, Income by Category (%), Income by Channel (%).

### Expense Processing (Source: `compres_code.ipynb`)
- **Input:** Excel files with `Cuenta` and an Amount column.
- **Categorization:**
  - **Expense Type:** Derived from `Cuenta` via substring matching (e.g., "alquiler" -> "Alquiler del local").
  - **Grouping:**
    - **Fixed/Operating:** Rent, Salaries, Utilities, Marketing, etc.
    - **Variable:** Flowers, Materials, Packaging, Courier, etc.
- **Metrics:** Total Expenses, Fixed vs Variable Split, Expense breakdown by Type.

## Dashboard Structure (Streamlit)
1. **Sidebar:** Navigation (Dashboard, Income, Expenses, Upload), Global Date Filter.
2. **Dashboard (Home):**
   - **AI Insights Widget:** Dynamic text summary ("Revenue is up 10% driven by Novias...").
   - **KPIs:** Total Income, Total Expenses, Net Profit, Profit Margin.
   - **Trend Chart:** Monthly Income vs Expenses (Line chart).
   - **Distribution:** Expenses Breakdown (Donut), Income by Channel (Bar).
3. **Income Page:** Detailed breakdown by Category/Channel, Data Table.
4. **Expenses Page:** Fixed vs Variable split, Detailed Data Table.
5. **Upload Page:** Drag-and-drop zone.
   - **Post-Upload Action:** Triggers immediate AI analysis of the new batch vs historical average.

## AI Implementation Details
- **Provider:** Google Gemini Flash (Fast, free tier available).
- **Configuration:** User provides `GEMINI_API_KEY` in `.env` or settings.
- **Prompt Strategy:**
  - Context: "You are a financial analyst for a floral business."
  - Input: JSON of current month totals, previous month totals, and top 3 categories.
  - Output: 2-3 sentence executive summary highlighting major changes or concerns.

## Data Processing Logic
- **Tech Stack:** Streamlit (Python)
- **Deployment:** Local execution (User runs `streamlit run app.py`)
- **Authentication:** None (Local access only)
- **Data Persistence:** SQLite Database (`sempreviva.db`)
  - **Why:** Zero-configuration, local file-based, supports SQL queries for analytics, perfect for "auto-save" requirement.
  - **Mechanism:** Uploaded files are processed -> cleaned data inserted into SQLite -> Dashboard queries SQLite.
- **AI Integration (New):** Google Gemini API (Free tier)
  - **Library:** `google-generativeai`
  - **Purpose:** Generate text summaries of financial health, spot trends, and explain anomalies.
  - **Privacy:** Only aggregated statistical data (totals, category sums) is sent to the LLM, not raw transaction rows.

## Database Schema (Proposed)
**Table: `transactions`**
- `id` (PK)
- `date` (Date)
- `amount` (Float)
- `type` (Enum: 'INCOME', 'EXPENSE')
- `category` (String - e.g., 'Novias', 'Alquiler')
- `subcategory` (String - e.g., 'Instagram', 'Fixed')
- `description` (String)
- `source_file` (String - filename)
- `created_at` (Timestamp)

**Table: `processed_files`**
- `filename` (PK)
- `upload_date` (Timestamp)
- `row_count` (Integer)
