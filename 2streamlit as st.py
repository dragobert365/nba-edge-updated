import streamlit as st
from scipy.stats import binom
from nba_api.stats.static import players
from nba_api.stats.endpoints import commonplayerinfo

st.set_page_config(layout="wide")
st.title("📈 NBA Prop Betting with Player Headshots")

# Deine komplette Spielerliste
nba_players = [
    "Jaylen Brown", "Sam Hauser", "Jrue Holiday", "Al Horford", "Luke Kornet",
    "Kristaps Porzingis", "Payton Pritchard", "Jayson Tatum", "Derrick White",
    "Nic Claxton", "Noah Clowney", "Killian Hayes", "Cameron Johnson",
    "Keon Johnson", "Tyrese Martin", "De'Anthony Melton", "D'Angelo Russell",
    "Day'Ron Sharpe", "Can Thomas", "Ziaire Williams", "Precious Achiuwa",
    "OG Anunoby", "Mikal Bridges", "Jalen Brunson", "Josh Hart", "Miles McBride",
    "Cameron Payne", "Mitchell Robinson", "Karl-Anthony Towns", "PJ Tucker",
    "Jared Butler", "Andre Drummond", "Joel Embiid", "Paul George",
    "Eric Gordon", "Quentin Grimes", "Kyle Lowry", "Tyrese Maxey",
    "Jared McCain", "Kelly Oubre Jr", "Guerschon Yabusele", "Gradey Dick",
    "Jonathan Mogbo", "Brandon Ingram", "Scottie Barnes", "Immanuel Quickley",
    "RJ Barrett", "Jakob Poeltl", "Ochai Agbaji", "Coby White", "Lonzo Ball",
    "Josh Giddey", "Jalen Smith", "Nikola Vucevic", "Zach Collins",
    "Kevin Huerter", "Matas Buzelis", "Tre Jones", "Patrick Williams",
    "Max Strus", "Ty Jerome", "Evan Mobley", "Darius Garland",
    "De'Andre Hunter", "Tristan Thompson", "Jarett Allen", "Dean Wade",
    "Isaac Okoro", "Donovan Mitchell", "Jalen Duren", "Cade Cunningham",
    "Malik Beasley", "Tim Hardaway Jr", "Ausar Thompson", "Tobias Harris",
    "Dennis Schröder", "Jaden Ivey", "Tyrese Haliburton", "Bennedict Mathurin",
    "Obi Toppin", "Andrew Nembhard", "T.J. McConnell", "Aaron Nesmith",
    "Myles Turner", "Pascal Siakam", "Damian Lillard", "Kevin Porter Jr",
    "Gary Trent Jr", "Bobby Portis", "Brook Lopez", "Taurean Prince",
    "Kyle Kuzma", "AJ Green", "Giannis Antetokounmpo", "Andre Jackson Jr",
    "Jalen Johnson", "Caris LeVert", "Dyson Daniels", "Zaccharie Risacher",
    "Trae Young", "Terance Mann", "Clint Capela", "Onyeka Okongwu",
    "Larry Nance Jr", "Miles Bridges", "LaMelo Ball", "Grant Williams",
    "Mark Williams", "Josh Green", "Jusuf Nurkic", "Josh Okogie",
    "Moussa Diabate", "Tre Mann", "Brandon Miller", "Seth Curry", "Taj Gibson",
    "Terry Rozier", "Nikola Jovic", "Kel'el Ware", "Jaime Jaquez Jr",
    "Bam Adebayo", "Tyler Herro", "Alec Burks", "Kyle Anderson",
    "Andrew Wiggins", "Kevin Love", "Davion Mitchell", "Duncan Robinson",
    "Anthony Black", "Jonathan Issac", "Desmond Bane", "Jalen Suggs",
    "Paolo Banchero", "Franz Wagner", "Moritz Wagner", "Tristan Da Silva",
    "Wendell Carter Jr", "Goga Bitadze", "Bilal Coulibaly", "AJ Johnson",
    "Justin Champagnie", "Jordan Poole", "Sadiq Bey", "Malcolm Brogdon",
    "Kyshawn George", "Alex Sarr", "JT Thor", "Cory Kispert",
    "Khris Middleton", "Marcus Smart", "Christian Braun",
    "Michael Porter Jr", "Julian Strawther", "Russell Westbrook",
    "Deandre Jordan", "Peyton Watson", "Dario Saric", "Nikola Jokic",
    "Jamal Murray", "Aaron Gordon", "Donte DiVincenzo",
    "Jaden McDaniels", "Rob Dillingham", "Anthony Edwards",
    "Joe Ingles", "Nickeil Alexander-Walker", "Mike Conley",
    "Naz Reid", "Rudy Gobert", "Julius Randle", "Leonard Miller",
    "Shai Gilgeous-Alexander", "Lu Dort", "Jaylin Williams",
    "Chet Holmgren", "Jaylen Williams", "Alex Caruso", "Isaiah Joe",
    "Aaron Wiggins", "Cason Wallace", "Isaiah Hartenstein",
    "Nikola Topic", "Scott Henderson", "Anfernee Simons",
    "Deandre Ayton", "Matisse Thybulle", "Deni Avdija",
    "Jerami Grant", "Shaedon Sharpe", "Kris Murray", "Jabari Walker",
    "Robert Williams III", "Jordan Clarkson", "Collin Sexton",
    "Keyonte George", "Isaiah Collier", "John Collins", "Kyle Filipowski",
    "Lauri Markkanen", "Walker Kessler", "Gary Payton II",
    "Jonathan Kuminga", "Brandin Podziemski", "Moses Moody",
    "Kevon Looney", "Buddy Hield", "Jimmy Butler", "Draymond Green",
    "Stephen Curry", "Trayce Jackson-Davis", "James Harden",
    "Kawhi Leonard", "Amir Coffey", "Kris Dunn", "Bogdan Bogdanovic",
    "Drew Eubanks", "Kobe Brown", "Norman Powell", "Ben Simmons",
    "Nicolas Batum", "Ivica Zubac", "Patty Mills", "Jared Vanderbilt",
    "Dalton Knecht", "Gabe Vincent", "Bronny James", "Jaxson Hayes",
    "Maxi Kleber", "Austin Reaves", "Dorian Finney-Smith", "LeBron James",
    "Alex Len", "Rui Hachimura", "Luka Doncic", "Royce O'Neale",
    "Ryan Dunn", "Devin Booker", "Nick Richards", "Bradley Beal",
    "Grayson Allen", "Bol Bol", "Vasilje Micic", "Tyus Jones",
    "Mason Plumlee", "Monte Morris", "Kevin Durant", "Malik Monk",
    "Zach LaVine", "DeMar DeRozan", "Domantas Sabonis",
    "Keegan Murray", "Jonas Valanciunas", "Markelle Fultz",
    "Max Christie", "Dante Exum", "Jaden Hardy", "Dereck Lively II",
    "Anthony Davis", "Kyrie Irving", "Caleb Martin", "Daniel Gafford",
    "PJ Washington", "Klay Thompson", "Spencer Dinwiddie", "Amen Thompson",
    "Jalen Green", "Fred VanVleet", "Cam Whitmore", "Dillon Brooks",
    "Jabari Smith Jr", "Steven Adams", "Reed Sheppard", "Tari Eason",
    "Alperen Şengün", "Jaylin Williams", "Scotty Pippen Jr",
    "Kentavious Caldwell-Pope", "Santi Aldama", "Luke Kennard",
    "Ja Morant", "Jaren Jackson Jr", "Zach Edey", "Bruce Brown",
    "Zion Williamson", "Herbert Jones", "CJ McCollum", "Dejounte Murray",
    "Brandon Boston", "Kelly Olynyk", "Jose Alvarado", "Yves Missi",
    "Trey Murphy III", "Keldon Johnson", "Victor Wembanyama",
    "Chris Paul", "De'Aaron Fox", "Stephon Castle", "Jeremy Sochan",
    "Bismack Biyombo", "Devin Vassell", "Julian Champagnie",
    "Harrison Barnes"
]

# Spieler-Auswahl
player = st.selectbox("Spieler auswählen", sorted(nba_players))

# Spielerbild laden via NBA-ID
player_lookup = players.find_players_by_full_name(player)
if player_lookup:
    pid = player_lookup[0]['id']
    info = commonplayerinfo.CommonPlayerInfo(player_id=pid).get_normalized_dict()['CommonPlayerInfo'][0]
    img_url = info.get('PHOTO_URL', None)
    if img_url:
        st.image(img_url, width=120, caption=player)

# Wett-Eingaben
prop = st.selectbox("Wettart", ["2+ Dreier", "3+ Dreier", "1+ Steal", "10+ Punkte"])
book_odds = st.number_input("Buchmacherquote (Dezimal)", value=2.80)
attempts = st.slider("Versuche (z. B. 3PA)", 1, 15, 5)
accuracy = st.slider("Trefferquote (%)", 10, 100, 39)

# Wahrscheinlichkeit & EV
p = accuracy / 100
target = int(prop.split('+')[0])
prob = 1 - sum(binom.pmf(k, attempts, p) for k in range(target))
fair_odds = 1 / prob if prob > 0 else None
ev = (prob * (book_odds - 1)) - (1 - prob)

# Ergebnis
st.markdown(f"### 📊 {player} – Prop: {prop}")
st.write(f"Wahrscheinl.: {prob*100:.2f}% | Faire Quote: {fair_odds:.2f} | EV: {ev:.3f}")
if ev > 0: st.success("✅ +EV – Edge vorhanden!")
elif ev == 0: st.info("⚖️ Fair bewertet")
else: st.error("❌ Kein Value")

