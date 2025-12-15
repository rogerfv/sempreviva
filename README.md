# Sempreviva Financial Dashboard

A Streamlit application that processes uploaded Excel files for incomes and expenses, stores them in SQLite, and renders interactive dashboards with AI-generated insights.

## Project Structure
- `app.py` – Streamlit entry point with navigation, date filters, and page routing.
- `database.py` – SQLite schema, inserts, and analytic queries.
- `processing/` – Parsers and categorization logic for income and expense files.
- `ui/` – Page components for dashboard, income, expenses, and uploads.
- `utils/` – Chart helpers and Gemini AI integration.
- `.env.example` – Environment variable template.

## Setup
1. Create and activate a virtual environment (optional but recommended).
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy the environment template and add your Gemini API key:
   ```bash
   cp .env.example .env
   # Edit .env and set GEMINI_API_KEY
   ```

## Running the App
Start Streamlit from the repository root:
```bash
streamlit run app.py
```

The app provides:
- A sidebar navigator with a global date filter.
- Dashboard KPIs, trends, and distribution charts.
- Income and expense detail pages with breakdowns and tables.
- A drag-and-drop upload page that processes Excel files and persists results.
- Optional AI summaries powered by Google Gemini when `GEMINI_API_KEY` is configured.

