import streamlit as st
import pandas as pd
from matcher.matching import match_donors
from pathlib import Path

st.set_page_config(page_title="Blood Bank Matcher", layout="wide")
st.title("🩸 Blood Bank Matcher")

# Load defaults
default_donors = pd.read_csv("data/donors.csv")
default_recipients = pd.read_csv("data/recipients.csv")
default_inventory = pd.read_csv("data/inventory.csv")

st.sidebar.header("Upload CSVs (optional)")
ud = st.sidebar.file_uploader("Donors CSV", type=["csv"])
ur = st.sidebar.file_uploader("Recipients CSV", type=["csv"])
ui = st.sidebar.file_uploader("Inventory CSV", type=["csv"])

donors = pd.read_csv(ud) if ud else default_donors.copy()
recipients = pd.read_csv(ur) if ur else default_recipients.copy()
inventory = pd.read_csv(ui) if ui else default_inventory.copy()

st.subheader("Recipients")
st.dataframe(recipients)

recipient_ids = recipients["id"].tolist()
sel = st.selectbox("Select recipient ID", recipient_ids)
topn = st.slider("How many donor recommendations?", 1, 10, 5)

if st.button("Find Matches"):
    results = match_donors(donors, recipients, inventory, sel, topn)
    if not results:
        st.warning("No eligible donors found under current rules.")
    else:
        rows = []
        for r in results:
            drow = donors.loc[donors['id'] == r.donor_id].iloc[0]
            rows.append({
                "donor_id": r.donor_id,
                "name": drow['name'],
                "blood": f"{drow['blood_type']}{drow['rh']}",
                "distance_km": round(r.distance_km, 1),
                "score": round(r.score, 3),
                "explanation": r.explanation
            })
        st.subheader("Recommended Donors")
        st.dataframe(pd.DataFrame(rows))
