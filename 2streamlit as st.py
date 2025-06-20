import streamlit as st
from scipy.stats import binom

st.title("📈 NBA Prop Betting: Edge Checker")

# Liste aktiver NBA-Spieler (gekürzt für Lesbarkeit – du kannst beliebig erweitern)
nba_players = sorted([
    "Alex Caruso", "Stephen Curry", "LeBron James", "Luka Doncic", "Jayson Tatum", 
    "Kevin Durant", "Devin Booker", "Kyrie Irving", "Anthony Davis", "Nikola Jokic",
    "Giannis Antetokounmpo", "Joel Embiid", "Damian Lillard", "James Harden",
    "Jaylen Brown", "Jimmy Butler", "Zach LaVine", "Donovan Mitchell",
    "Shai Gilgeous-Alexander", "Trae Young", "Jalen Brunson", "Desmond Bane",
    "Anthony Edwards", "Jaren Jackson Jr.", "Tyrese Haliburton", "De'Aaron Fox",
    "RJ Barrett", "Mikal Bridges", "Paolo Banchero", "Scottie Barnes",
    "Franz Wagner", "Chet Holmgren", "Victor Wembanyama"
    # Du kannst hier alle anderen Spieler hinzufügen
])

# Eingaben
player = st.selectbox("Spieler auswählen", nba_players)
prop_type = st.selectbox("Wettart", ["2+ Dreier", "3+ Dreier", "1+ Steal", "10+ Punkte"])
book_odds = st.number_input("Buchmacherquote (Dezimal)", value=2.80)
attempts = st.slider("Wurfversuche (z. B. 3PA)", 1, 15, 5)
accuracy = st.slider("Trefferquote (%)", 10, 100, 39)

# Wahrscheinlichkeitsrechnung
p = accuracy / 100
target_made = int(prop_type[0]) if prop_type[0].isdigit() else 2
prob = 1 - sum([binom.pmf(k, attempts, p) for k in range(target_made)])
fair_odds = 1 / prob if prob > 0 else None
ev = (prob * (book_odds - 1)) - (1 - prob)

# Ausgabe
st.markdown(f"### 📊 Ergebnisse für {player}")
st.write(f"**Wahrscheinlichkeit für '{prop_type}':** {round(prob * 100, 2)} %")
st.write(f"**Faire Quote:** {round(fair_odds, 2) if fair_odds else 'unbekannt'}")
st.write(f"**Expected Value (EV):** {round(ev, 3)}")

if ev > 0:
    st.success("✅ +EV – Diese Wette hat einen Edge!")
elif ev == 0:
    st.info("⚖️ Fair bewertet")
else:
    st.error("❌ Kein Value – Finger weg!")
