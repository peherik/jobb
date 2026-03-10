import streamlit as st
import pandas as pd
from datetime import date

# --- KONFIGURATION ---
st.set_page_config(page_title="Schema-kollen", page_icon="📅", layout="wide")
st.title("Arbetsschema - 4 veckors rullande")

# Startdatum för schemaperioden (Vecka 1, Måndag)
START_DATE = date(2026, 2, 2) 

# Definition av alla scheman (28 dagar per person)
# x = Jobbar, None = Ledig
schedules = {
    "Gittan": [
        "x", None, None, "x", None, None, None, # V1
        None, None, None, None, "x", "x", None, # V2
        None, "x", None, None, "x", None, None, # V3
        "x", "x", None, None, None, None, "x"   # V4
    ],
    "Rebecca": [
        "x", "x", "x", None, None, None, "x",  # V1
        "x", None, None, "x", "x", None, None, # V2
        "x", None, None, None, "x", "x", "x",  # V3
        "x", None, None, None, None, None, None # V4
    ],
    "Cecilia": [
        None, "x", "x", None, None, None, "x", # V1
        "x", None, None, None, None, "x", "x", # V2
        None, None, "x", "x", None, None, None, # V3
        None, None, None, "x", "x", "x", None  # V4
    ],
    "Marie": [
        None, None, None, None, "x", "x", None, # V1
        None, "x", "x", None, None, None, "x", # V2
        "x", None, None, None, None, "x", "x", # V3
        None, "x", "x", None, None, None, None  # V4
    ],
    "Molly": [
        None, None, None, "x", "x", "x", None, # V1
        None, "x", "x", "x", None, None, None, # V2
        None, "x", "x", "x", None, None, None, # V3
        "x", "x", None, None, "x", "x", "x"   # V4
    ]
}

# --- LOGIK ---
def get_status(person, check_date):
    delta = (check_date - START_DATE).days
    day_in_cycle = delta % 28
    return schedules[person][day_in_cycle]

# --- ANVÄNDARGRÄNSSNITT ---

# 1. Kolla specifikt datum
st.subheader("🔎 Kolla pass")
col1, col2 = st.columns(2)

with col1:
    valda_personer = st.multiselect("Välj personal:", list(schedules.keys()), default=list(schedules.keys()))
with col2:
    valda_datum = st.date_input("Välj datum:", date.today())

if st.button("Visa status"):
    dag_namn = ["Måndag", "Tisdag", "Onsdag", "Torsdag", "Fredag", "Lördag", "Söndag"][valda_datum.weekday()]
    delta = (valda_datum - START_DATE).days
    vecka_i_schema = ((delta % 28) // 7) + 1
    
    st.write(f"**Resultat för {dag_namn} {valda_datum} (Schema-vecka {vecka_i_schema}):**")
    
    cols = st.columns(len(valda_personer))
    for i, person in enumerate(valda_personer):
        jobbar = get_status(person, valda_datum) == "x"
        with cols[i]:
            if jobbar:
                st.success(f"**{person}**\n\nJobbar ✅")
            else:
                st.info(f"**{person}**\n\nLedig 😴")

st.divider()

# 2. Schema-översikt (Dataframe)
st.subheader("📊 Fullständig schema-översikt")

# Skapa tabell-data
days_labels = ["M", "Ti", "O", "To", "F", "L", "S"] * 4
table_data = []
for person, days in schedules.items():
    # Gör om "x" och None till lite snyggare emojis för tabellen
    row = [("✅" if d == "x" else "") for d in days]
    table_data.append(row)

# Skapa kolumnnamn med Vecka 1, Vecka 2 osv.
headers = []
for v in range(1, 5):
    for d in ["M", "Ti", "O", "To", "F", "L", "S"]:
        headers.append(f"V{v} {d}")

df = pd.DataFrame(table_data, columns=headers, index=schedules.keys())

# Visa tabellen
st.dataframe(df, use_container_width=True)

st.caption(f"Schemat rullar på 28 dagar med start måndag {START_DATE}.")