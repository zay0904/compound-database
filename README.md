# 🧪 Chemical Compound Database

A small, focused Python tool for storing and searching chemical compound
data. Built with SQLite for portability, exposed via a Streamlit web app,
and exportable to JSON so a static website can search it too.

![Demo](screenshots/demo.png)

## Features

- **SQLite database** with schema for name, formula, CAS number, molar mass,
  physical properties, hazard class, and description.
- **Seeded** with ~22 well-known compounds out of the box.
- **Streamlit web UI** — search by name, formula, CAS, or keyword; filter by
  state at STP; add new compounds; download results as CSV.
- **JSON export** — `python export_json.py` writes `compounds.json` for use
  in any static site via `fetch()`.
- **CSV / XLSX import** — coming soon.
- **Tests** with pytest.

## Quick start

```bash
pip install -r requirements.txt

# Create the SQLite database and load starter compounds
python -m src.seed

# Run the web app
streamlit run app.py

# Export to JSON for your static site
python export_json.py