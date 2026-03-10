import streamlit as st
from datetime import date, timedelta

# Inställningar för appen
st.set_page_config(page_title="Schema-kollen", page_icon="📅")
st.title("Vem jobbar idag?")

# Grundinställningar
START_DATE = date(2026, 2, 2)

# Scheman (0-27 dagar)
schedules = {
    "Rebecca": [
        "x", "x", "x", None, None, None, "x",  # Vecka 1
        "x", None, None, "x", "x", None, None, # Vecka 2
        "x", None, None, None, "x", "x", "x",  # Vecka 3
        "x", None, None, None, None, None, None # Vecka 4
    ],
    "Gittan": [
        "x", None, None, "x", None, None, None, # V1
        None, None, None, None, "x", "x", None, # V2
        None, "x", None, None, "x", None, None, # V3
        "x", "x", None, None, None, None, "x"  # V4
    ]
}

# Användargränssnitt
valda_personer = st.multiselect("Välj kollegor att kolla:", list(schedules.keys()), default=["Rebecca"])
valda_datum = st.date_input("Välj datum att kontrollera:", date.today())

if st.button("Kolla schema"):
    delta = (valda_datum - START_DATE).days
    dag_i_cykel = delta % 28
    
    # Räkna ut vilken vecka och dag det motsvarar i schemat
    vecka = (dag_i_cykel // 7) + 1
    dag_namn = ["Måndag", "Tisdag", "Onsdag", "Torsdag", "Fredag", "Lördag", "Söndag"][valda_datum.weekday()]
    
    st.info(f"Datum: {valda_datum} ({dag_namn}, Vecka {vecka} i schemat)")
    
    for person in valda_personer:
        jobbar = schedules[person][dag_i_cykel] == "x"
        if jobbar:
            st.success(f"✅ **{person}** jobbar!")
        else:
            st.error(f"😴 **{person}** är ledig.")

# Visar en liten tabell för överblick
with st.expander("Visa hela 4-veckorsperioden"):
    st.write("Här kan du se hur schemat ser ut i sin helhet.")
    # (Här kan man lägga till en dataframe-tabell om man vill)