# Research

## Summary
The current repository appears to be a collection of data files (Excel), a rules document (Word), and Jupyter notebooks, rather than a structured web application. The "app" logic likely currently resides in the notebooks `compres_code.ipynb` and `ingressos_code.ipynb`.

## Repository: sempreviva

### Existing Files
- `Documento_Reglas_GPT.docx`: Business rules documentation.
- `FINANZAS DE TU NEGOCIO- 2025.xlsx`: Financial overview.
- `Mapeo_Productos_y_Canales.xlsx`: Data mapping.
- `Maria Vert Carbó - Compras...`: Expense data.
- `Maria Vert Carbó - Ingresos...`: Income data.
- `compres_code.ipynb`: Analysis script for purchases/expenses.
- `ingressos_code.ipynb`: Analysis script for income.

### Component: Data Analysis (Notebooks)
**Location:** `/workspace/cmj75sq9n0165imps68157kc4/sempreviva/*.ipynb`

**Logic: Income (`ingressos_code.ipynb`)**
- **Input:** Excel files matching `Maria Vert Carbó - Ingresos DD_MM_YYYY-DD_MM_YYYY.xlsx`.
- **Key Columns Required:** `Tags`, Amount column (`Total`, `Importe`, etc.), `Descripción` (optional for sub-classification).
- **Categorization:**
  - **Product:** Derived from `Tags` using hardcoded keywords (e.g., "nuvies" -> "Novias"). Default: "Productos web...".
  - **Channel:** Derived from `Tags` (e.g., "instagram" -> "Instagram"). Default: "Sin identificar".
- **Outputs:** `ingresos_report_global.xlsx` with sheets for each month + "TOTAL" + "Tendencias".
- **Visuals:** Bar charts for Category/Channel; Line charts for Trends.

**Logic: Expenses (`compres_code.ipynb`)**
- **Input:** Excel files matching `Maria Vert Carbó - Compras DD_MM_YYYY-DD_MM_YYYY.xlsx`.
- **Key Columns Required:** `Cuenta` (for categorization), Amount column.
- **Categorization:**
  - **Type:** Derived from `Cuenta` using regex-like substrings (e.g., "alquiler" -> "Alquiler del local").
  - **Groups:** Split into "Fixed/Operating" vs "Variable" expenses.
- **Outputs:** `gastos_report_global.xlsx`.

**Data Flow**
- Current: User manually places Excel files in folder -> Runs Notebook -> Gets Output Excel.
- Desired: Web App -> Upload Interface -> Dashboard.

**Discrepancies**
- The repository contains `Mapeo_Productos_y_Canales.xlsx` but the notebooks use **hardcoded python lists** for rules. The app might need to externalize these rules to a database or config file.

**Connections**
- `compres_code.ipynb` handles the "expenses" mode the user requested.
- `ingressos_code.ipynb` handles the "earnings" part.
