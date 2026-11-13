"""
Load a starter set of well-known compounds into the database.

Values are approximate reference values for demonstration. For a
production chemistry tool, verify against PubChem or CRC Handbook.
"""
from __future__ import annotations

from .db import connect

COMPOUNDS = [
    # name, formula, cas, mass, density, mp, bp, state, hazard, description
    ("Water", "H2O", "7732-18-5", 18.015, 1.000, 0.0, 100.0, "liquid", None,
     "Universal solvent; essential for life."),
    ("Ethanol", "C2H6O", "64-17-5", 46.068, 0.789, -114.1, 78.37, "liquid",
     "Flammable", "Common laboratory solvent and disinfectant."),
    ("Methanol", "CH4O", "67-56-1", 32.042, 0.792, -97.6, 64.7, "liquid",
     "Toxic, Flammable", "Industrial solvent; highly toxic if ingested."),
    ("Acetic acid", "C2H4O2", "64-19-7", 60.052, 1.049, 16.6, 118.1, "liquid",
     "Corrosive", "Main component of vinegar; weak acid."),
    ("Sodium chloride", "NaCl", "7647-14-5", 58.44, 2.165, 801.0, 1413.0,
     "solid", None, "Table salt; ionic compound."),
    ("Glucose", "C6H12O6", "50-99-7", 180.156, 1.54, 146.0, None, "solid",
     None, "Simple sugar; primary energy source in cells."),
    ("Sucrose", "C12H22O11", "57-50-1", 342.30, 1.587, 186.0, None, "solid",
     None, "Table sugar; disaccharide of glucose and fructose."),
    ("Eucalyptus oil (1,8-cineole)", "C10H18O", "470-82-6", 154.25, 0.922,
     1.5, 176.0, "liquid", "Flammable",
     "Major component of eucalyptus essential oil — the subject of my thesis."),
    ("Citric acid", "C6H8O7", "77-92-9", 192.12, 1.665, 153.0, 175.0, "solid",
     None, "Weak organic acid found in citrus fruits."),
    ("Sodium bicarbonate", "NaHCO3", "144-55-8", 84.007, 2.20, 50.0, None,
     "solid", None, "Baking soda; mild base."),
    ("Sulfuric acid", "H2SO4", "7664-93-9", 98.079, 1.830, 10.31, 337.0,
     "liquid", "Corrosive, Toxic", "Strong mineral acid; widely used industrially."),
    ("Hydrochloric acid", "HCl", "7647-01-0", 36.46, 1.18, -114.2, -85.05,
     "gas", "Corrosive", "Strong acid; aqueous solution is 'muriatic acid'."),
    ("Sodium hydroxide", "NaOH", "1310-73-2", 39.997, 2.13, 318.0, 1388.0,
     "solid", "Corrosive", "Strong base; also known as lye or caustic soda."),
    ("Ammonia", "NH3", "7664-41-7", 17.031, 0.73, -77.73, -33.34, "gas",
     "Toxic, Corrosive", "Pungent gas; important industrial chemical."),
    ("Carbon dioxide", "CO2", "124-38-9", 44.01, 0.001977, -56.6, None, "gas",
     None, "Greenhouse gas; product of combustion and respiration."),
    ("Oxygen", "O2", "7782-44-7", 31.998, 0.001429, -218.79, -182.96, "gas",
     "Oxidizer", "Essential for aerobic respiration."),
    ("Nitrogen", "N2", "7727-37-9", 28.014, 0.001251, -210.0, -195.79, "gas",
     None, "Most abundant gas in Earth's atmosphere."),
    ("Methane", "CH4", "74-82-8", 16.043, 0.000657, -182.5, -161.5, "gas",
     "Flammable", "Main component of natural gas."),
    ("Benzene", "C6H6", "71-43-2", 78.11, 0.876, 5.53, 80.1, "liquid",
     "Carcinogenic, Flammable", "Aromatic hydrocarbon; known carcinogen."),
    ("Aspirin", "C9H8O4", "50-78-2", 180.16, 1.40, 136.0, 140.0, "solid",
     "Irritant", "Acetylsalicylic acid; common analgesic."),
    ("Copper(II) sulfate", "CuSO4", "7758-98-7", 159.609, 3.60, 110.0, None,
     "solid", "Irritant", "Blue crystalline solid; pentahydrate is common."),
    ("Potassium permanganate", "KMnO4", "7722-64-7", 158.034, 2.703, 240.0,
     None, "solid", "Oxidizer, Irritant", "Strong oxidizing agent; purple solution."),
]


def seed(force: bool = False) -> int:
    """
    Insert the starter compounds. If `force`, clear the table first.
    Returns the number of rows now in the table.
    """
    conn = connect()
    with conn:
        if force:
            conn.execute("DELETE FROM compounds")
        for row in COMPOUNDS:
            name, formula, cas, mass, dens, mp, bp, state, hazard, desc = row
            conn.execute(
                """
                INSERT OR IGNORE INTO compounds
                (name, formula, cas_number, molar_mass, density,
                 melting_point, boiling_point, state_stp, hazard_class, description)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (name, formula, cas, mass, dens, mp, bp, state, hazard, desc),
            )
    n = conn.execute("SELECT COUNT(*) FROM compounds").fetchone()[0]
    conn.close()
    return n


if __name__ == "__main__":
    count = seed(force=True)
    print(f"Seeded database — {count} compounds available.")