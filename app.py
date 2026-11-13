"""
Streamlit UI for the Chemical Compound Database.

Run locally:
    streamlit run app.py

Deploy: push to GitHub, then https://share.streamlit.io → New app.
"""
from __future__ import annotations

import pandas as pd
import streamlit as st

from src.queries import search, count, by_state, add_compound
from src.seed import seed


st.set_page_config(page_title="Chemical Compound Database",
                   page_icon="🧪", layout="wide")

st.title("🧪 Chemical Compound Database")
st.caption("Search, browse, and add chemical compounds. Backed by SQLite.")

# Ensure there's data on first run (Streamlit Cloud starts fresh)
if count() == 0:
    n = seed()
    st.info(f"Seeded the database with {n} starter compounds.")

# ---------------- Sidebar filters ----------------
st.sidebar.header("Search")
query = st.sidebar.text_input("Name, formula, CAS, or keyword", "")
state_filter = st.sidebar.selectbox(
    "State at STP", ["Any", "solid", "liquid", "gas"]
)

# ---------------- Query ----------------
if query.strip():
    results = search(query)
elif state_filter != "Any":
    results = by_state(state_filter)
else:
    results = search("", limit=200)

# Apply state filter on top of text search
if state_filter != "Any" and query.strip():
    results = [r for r in results if r.get("state_stp") == state_filter]

st.write(f"**{len(results)}** compound(s) found.")

# ---------------- Results table ----------------
if results:
    df = pd.DataFrame(results)
    # Prettier column order
    preferred = ["name", "formula", "cas_number", "molar_mass",
                 "state_stp", "density", "melting_point", "boiling_point",
                 "hazard_class", "description"]
    cols = [c for c in preferred if c in df.columns]
    df_view = df[cols]

    st.dataframe(
        df_view,
        use_container_width=True,
        hide_index=True,
        column_config={
            "name": "Name",
            "formula": "Formula",
            "cas_number": "CAS #",
            "molar_mass": st.column_config.NumberColumn("M (g/mol)", format="%.3f"),
            "state_stp": "State",
            "density": st.column_config.NumberColumn("Density (g/cm³)", format="%.3f"),
            "melting_point": st.column_config.NumberColumn("MP (°C)", format="%.1f"),
            "boiling_point": st.column_config.NumberColumn("BP (°C)", format="%.1f"),
            "hazard_class": "Hazard",
            "description": "Description",
        },
    )

    # Detail view for a single compound
    with st.expander("🔍 View details for a compound"):
        names = [r["name"] for r in results]
        pick = st.selectbox("Choose compound", names)
        selected = next(r for r in results if r["name"] == pick)
        st.json(selected)

    # CSV download
    csv = df_view.to_csv(index=False).encode("utf-8")
    st.download_button("⬇ Download results as CSV", csv,
                       "compounds.csv", "text/csv")
else:
    st.warning("No compounds matched your search.")

# ---------------- Add new compound ----------------
with st.expander("➕ Add a new compound"):
    with st.form("add_form"):
        c1, c2 = st.columns(2)
        name = c1.text_input("Name*")
        formula = c2.text_input("Formula*")
        cas = c1.text_input("CAS number")
        mass = c2.number_input("Molar mass (g/mol)", min_value=0.0, value=0.0)
        state = c1.selectbox("State at STP", ["", "solid", "liquid", "gas"])
        hazard = c2.text_input("Hazard class")
        description = st.text_area("Description")

        if st.form_submit_button("Add compound"):
            if not name or not formula:
                st.error("Name and formula are required.")
            else:
                try:
                    new_id = add_compound(
                        name=name, formula=formula,
                        cas_number=cas or None,
                        molar_mass=mass or None,
                        state_stp=state or None,
                        hazard_class=hazard or None,
                        description=description or None,
                    )
                    st.success(f"Added '{name}' (id {new_id}). Refresh to see it.")
                except Exception as e:
                    st.error(f"Could not add: {e}")

st.caption("Built by Mwila Molobeka — chemistry meets code.")