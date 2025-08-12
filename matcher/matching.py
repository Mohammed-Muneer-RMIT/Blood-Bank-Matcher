import pandas as pd
import numpy as np
import math
from datetime import datetime, timedelta
from dataclasses import dataclass

WHOLE_BLOOD_DEFERRAL_DAYS = 56

ABO_COMPAT = {
    "O": ["O", "A", "B", "AB"],
    "A": ["A", "AB"],
    "B": ["B", "AB"],
    "AB": ["AB"],
}

def rh_compatible(donor_rh: str, recip_rh: str) -> bool:
    # Rh- can donate to Rh- and Rh+ ; Rh+ -> Rh+ only
    if donor_rh == "-":
        return True
    return recip_rh == "+"

def abo_compatible(donor_abo: str, recip_abo: str) -> bool:
    return recip_abo in ABO_COMPAT.get(donor_abo, [])

def days_since(date_str: str) -> int:
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return (datetime.utcnow() - dt).days
    except Exception:
        return 10**9

def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0
    phi1 = math.radians(lat1); phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dl/2)**2
    c = 2*math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R*c

@dataclass
class MatchResult:
    donor_id: int
    score: float
    distance_km: float
    explanation: str

def score_donor(d, recip, inv_units):
    # Base score from proximity (closer is better)
    distance = haversine_km(d["lat"], d["lon"], recip["lat"], recip["lon"])
    proximity = max(0.0, 1.0 - (distance / 200.0))  # 0..1 ~ within 200km

    # ABO/Rh exactness bonus
    exact_abo = 1.0 if d["blood_type"] == recip["blood_type"] else 0.0
    exact_rh  = 1.0 if d["rh"] == recip["rh"] else 0.0

    # Inventory urgency (lower stock => higher weight)
    shortage = max(0, recip["units_needed"] - inv_units)
    shortage_factor = min(1.0, shortage / max(1, recip["units_needed"]))

    # Final weighted score
    score = (
        0.55 * proximity +
        0.20 * exact_abo +
        0.10 * exact_rh +
        0.15 * shortage_factor
    )
    return float(score), float(distance), exact_abo, exact_rh, shortage

def eligible(d, recip):
    if not abo_compatible(d["blood_type"], recip["blood_type"]):
        return False, "ABO incompatible"
    if not rh_compatible(d["rh"], recip["rh"]):
        return False, "Rh incompatible"
    if str(d.get("available","")).lower() in ("0","false","no"):
        return False, "Donor unavailable"
    if days_since(str(d.get("last_donation_date","1900-01-01"))) < WHOLE_BLOOD_DEFERRAL_DAYS:
        return False, "Within deferral window"
    return True, ""

def match_donors(donors_df, recipients_df, inventory_df, recipient_id, top_n=5):
    recip = recipients_df.loc[recipients_df["id"] == recipient_id]
    if recip.empty:
        raise ValueError("Recipient not found")
    recip = recip.iloc[0]

    inv = inventory_df[
        (inventory_df["blood_type"] == recip["blood_type"]) &
        (inventory_df["rh"] == recip["rh"])
    ]
    inv_units = int(inv.iloc[0]["units_available"]) if not inv.empty else 0

    rows = []
    for _, d in donors_df.iterrows():
        ok, reason = eligible(d, recip)
        if not ok:
            continue
        s, dist, exact_abo, exact_rh, shortage = score_donor(d, recip, inv_units)
        expl = []
        expl.append(f"ABO {d['blood_type']}→{recip['blood_type']} ✓")
        expl.append(f"Rh {d['rh']}→{recip['rh']} {'✓' if exact_rh or d['rh']=='-' else '✓ (Rh- universal)'}")
        expl.append(f"Distance {dist:.1f} km")
        expl.append(f\"Inventory for {recip['blood_type']}{recip['rh']}: {inv_units} units (shortage {shortage})\")
        if exact_abo: expl.append("Exact ABO match +")
        if exact_rh: expl.append("Exact Rh match +")
        rows.append(MatchResult(int(d['id']), s, dist, "; ".join(expl)))

    rows.sort(key=lambda x: (-x.score, x.distance_km))
    return rows[:top_n]
    
if __name__ == '__main__':
    import argparse, pandas as pd, json, os
    parser = argparse.ArgumentParser()
    parser.add_argument('--recipient', type=int, required=True)
    parser.add_argument('--top', type=int, default=5)
    parser.add_argument('--donors', default='data/donors.csv')
    parser.add_argument('--recipients', default='data/recipients.csv')
    parser.add_argument('--inventory', default='data/inventory.csv')
    args = parser.parse_args()

    donors = pd.read_csv(args.donors)
    recips = pd.read_csv(args.recipients)
    inv = pd.read_csv(args.inventory)
    matches = match_donors(donors, recips, inv, args.recipient, args.top)
    for m in matches:
        print(m)
