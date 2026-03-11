import streamlit as st
import pandas as pd
from datetime import date

# --- KONFIGURATION ---
st.set_page_config(page_title="Schema-kollen", page_icon="📅")
st.title("Arbetsschema")

# Startdatum för schemaperioden (Vecka 1, Måndag)
START_DATE = date(2026, 2, 2) 

# Scheman för alla medarbetare
schedules = {
    "Gittan": ["x",None,None,"x",None,None,None,None,None,None,None,"x","x",None,None,"x",None,None,"x",None,None,"x","x",None,None,None,None,"x"],
    "Rebecca": ["x","x","x",None,None,None,"x","x",None,None,"x","x",None,None,"x",None,None,None,"x","x","x","x",None,None,None,None,None,None],
    "Cecilia": [None,"x","x",None,None,None,"x","x",None,None,None,None,"x","x",None,None,"x","x",None,None,None,None,None,None,"x","x","x",None],
    "Marie": [None,None,None,None,"x","x",None,None,"x","x",None,None,None,"x","x",None,None,None,None,"x","x",None,"x","x",None,None,None,None],
    "Molly": [None,None,None,"x","x","x",None,None,"x","x","x",None,None,None,None,"x","x","x",None,None,None,"x","x",None,None,"x","x","x"]
}

# --- LOGIK ---
def get_status(person, check_date):
    delta = (check_date - START_DATE).days
    day_in_cycle = delta % 28
    return schedules[person][day_in_cycle]

# --- ANVÄNDARGRÄNSSNITT ---

st.subheader("🔎 Kolla pass")
col1, col2 = st.columns(2)

with col1:
    # Här är nu Rebecca vald som standard (default=["Rebecca"])
    valda_personer = st.multiselect("Välj personal:", list(schedules.keys()), default=["Rebecca"])
with col2:
    valda_datum = st.date_input("Välj datum:", date.today())

if st.button("Visa status"):
    dag_namn = ["Måndag", "Tisdag", "Onsdag", "Torsdag", "Fredag", "Lördag", "Söndag"][valda_datum.weekday()]
    delta = (valda_datum - START_DATE).days
    vecka_i_schema = ((delta % 28) // 7) + 1
    
    st.markdown(f"**{dag_namn} {valda_datum}** (Vecka {vecka_i_schema})")
    
    # Visar resultaten i kolumner
    cols = st.columns(len(valda_personer) if len(valda_personer) > 0 else 1)
    for i, person in enumerate(valda_personer):
        jobbar = get_status(person, valda_datum) == "x"
        with cols[i]:
            if jobbar:
                st.success(f"**{person}**\n\nJobbar ✅")
            else:
                st.error(f"**{person}**\n\nLedig 😴")

st.divider()

# --- DATAFRAME I EN EXPANDER (DOLD SOM STANDARD) ---
with st.expander("📊 Visa hela schema-översikten (28 dagar)"):    
    
    # Skapa tabell-data
    headers = []
    for v in range(1, 5):
        for d in ["M", "Ti", "O", "To", "F", "L", "S"]:
            headers.append(f"V{v} {d}")

    table_data = []
    for person, days in schedules.items():
        row = [("✅" if d == "x" else "") for d in days]
        table_data.append(row)

    df = pd.DataFrame(table_data, columns=headers, index=schedules.keys())
    
    # Visa tabellen med lite extra styling
    st.dataframe(df, use_container_width=False)
    
    st.caption(f"Appen räknar ut rullande schema baserat på startmåndag {START_DATE}.")