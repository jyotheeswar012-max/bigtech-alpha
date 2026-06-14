# 🤝 Contributing to Market Nexus

Thank you for your interest in improving Market Nexus! This document explains how to report bugs, propose features, and submit code changes.

---

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How to Report a Bug](#how-to-report-a-bug)
- [How to Request a Feature](#how-to-request-a-feature)
- [Submitting a Pull Request](#submitting-a-pull-request)
- [Code Style Guidelines](#code-style-guidelines)
- [Project Structure Reference](#project-structure-reference)

---

## Code of Conduct

Be respectful and constructive. All contributors are expected to maintain a welcoming environment regardless of experience level, background, or perspective.

---

## Getting Started

1. **Fork** the repository on GitHub.
2. **Clone** your fork locally:
   ```bash
   git clone https://github.com/<your-username>/market-nexus.git
   cd market-nexus
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the app** to confirm everything works:
   ```bash
   streamlit run nexus.py
   ```
5. **Create a branch** for your change:
   ```bash
   git checkout -b fix/your-bug-description
   # or
   git checkout -b feature/your-feature-name
   ```

---

## How to Report a Bug

1. Search [existing issues](https://github.com/jyotheeswar012-max/market-nexus/issues) first — your bug may already be reported.
2. If not, open a new issue with:
   - **Title:** Short description, e.g. `Stock Performance page crashes when single company selected`
   - **Steps to reproduce:** Numbered list of exact steps
   - **Expected behaviour:** What should happen
   - **Actual behaviour:** What actually happens
   - **Environment:** Python version, OS, Streamlit version (`streamlit version`)
   - **Screenshot or traceback** if applicable

---

## How to Request a Feature

1. Open an issue with the label `enhancement`.
2. Describe:
   - **The problem** you're trying to solve (not just the solution)
   - **Your proposed approach**, if you have one
   - **Which page or module** it would affect

Feature requests are reviewed and prioritised by the maintainer.

---

## Submitting a Pull Request

### Before you start

- For non-trivial changes, open an issue first to discuss the approach.
- One pull request per logical change — avoid bundling unrelated edits.

### PR checklist

- [ ] My branch is up to date with `main`
- [ ] The app runs without errors (`streamlit run nexus.py`)
- [ ] I have tested both **live mode** (with `live_data.py`) and **CSV fallback** (without it)
- [ ] New chart or UI changes are tested at both wide and narrow viewport widths
- [ ] I have not introduced new Python warnings or Streamlit deprecation warnings
- [ ] PR title clearly describes the change (e.g. `fix: handle empty price_df on Stock Performance page`)

### PR title convention

Use a short prefix:

| Prefix | When to use |
|---|---|
| `feat:` | New feature or page |
| `fix:` | Bug fix |
| `docs:` | Documentation only |
| `style:` | CSS / UI polish, no logic change |
| `refactor:` | Code restructure, no behaviour change |
| `data:` | CSV data update |

---

## Code Style Guidelines

### Python

- Follow **PEP 8** — 4-space indentation, max line length ~110 chars.
- Use descriptive variable names. Avoid single-letter names outside of short list comprehensions.
- All Plotly figures must go through the `sf(fig, height)` helper to apply the shared dark theme — do not call `fig.update_layout(**PL)` directly in page code.
- Guard every data operation that might fail on an empty DataFrame:
  ```python
  if not df.empty and 'ColumnName' in df.columns:
      ...
  ```

### Adding a new page

1. Add the page name to `PAGE_NAMES` in `nexus.py` and increment the unpacking tuple.
2. Add a new `elif page_idx == PAGE_XX:` block at the bottom of `nexus.py`.
3. Use `page_header_range()` (year-range slider) or `page_header_single()` (single year picker) as the first call.
4. Filter `ann_df`, `q_df`, and `price_df` immediately after the header using `sel_companies` and the chosen year variable.
5. Wrap all content in `st.tabs([...])` with at least one tab.

### Adding a new chart

1. Create a `go.Figure()`, add traces, then call `sf(fig, height)` before `st.plotly_chart()`.
2. Set `config={'displayModeBar': False}` on every `st.plotly_chart()` call.
3. Use company colours from `COLORS.get(company, '#818cf8')` for consistency.

### CSS / Styling

- All custom styles live in the single `st.markdown("""<style>...</style>""")` block at the top of `nexus.py`.
- Use the CSS variables defined in `:root` (e.g. `var(--primary)`, `var(--border)`) — do not hardcode hex values in new CSS rules.
- If adding a reusable UI component, define its CSS class in the `:root` block and document it with a brief comment.

---

## Project Structure Reference

```
market-nexus/
├── nexus.py               # Main app — all pages, sidebar, data loading
├── live_data.py           # yfinance fetcher — do not break the merge_with_csv contract
├── constants.py           # COLORS, PAGE_NAMES, CSS tokens — single source of truth
├── annual_metrics.csv     # Annual financial data (CSV fallback)
├── quarterly_revenue.csv  # Quarterly revenue data (CSV fallback)
├── stock_prices.csv       # Daily price history (CSV fallback)
├── requirements.txt       # pip dependencies
├── CONTRIBUTING.md        # This file
└── LICENSE                # MIT License
```

### The `merge_with_csv` contract

`live_data.merge_with_csv(live_df, csv_df, keys)` must continue to:
- Prefer live API rows over CSV rows for matching keys
- Fill missing columns from CSV via `ffill/bfill` within key groups
- Return a DataFrame with the **union** of both DataFrames' columns

Do not change this behaviour — `nexus.py` relies on it for the ghost-column patch logic.

---

Thank you for contributing! 🚀
