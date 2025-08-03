import pandas as pd
import ast

# Load all cards from CSV
csv_path = "arkhamdb_cards.csv"
df_csv = pd.read_csv(csv_path)

# Define player card types
player_types = ["asset", "event", "skill", "investigator", "treasure"]

# Filter for player cards
player_cards = df_csv[df_csv["type_code"].isin(player_types)]

# Identify investigator cards: must have all six fields non-null
investigator_columns = [
    "skill_willpower", "skill_intellect", "skill_combat", "skill_agility",
    "health", "sanity"
]
investigator_cards = player_cards.dropna(subset=investigator_columns, how="any")


# Identify all investigator codes
investigator_codes = set(investigator_cards["code"])

# Identify all signature cards for all investigators
signature_codes = set()
for _, row in investigator_cards.iterrows():
    deck_req_str = row.get("deck_requirements", None)
    if pd.notnull(deck_req_str):
        try:
            deck_req = ast.literal_eval(deck_req_str)
            card_dict = deck_req.get("card", {})
            for v in card_dict.values():
                signature_codes.update(v.keys())
        except Exception:
            pass

# Player cards: all player_cards that are not investigators or signature cards
player_card_codes = set(player_cards["code"]) - investigator_codes - signature_codes

# Build the combined DataFrame
combined_codes = list(investigator_codes | signature_codes | player_card_codes)
combined_df = df_csv[df_csv["code"].isin(combined_codes)].copy()

def classify_card(row):
    if row["code"] in investigator_codes:
        return "investigator"
    elif row["code"] in signature_codes:
        return "signature_card"
    else:
        return "player_card"

combined_df["card_type"] = combined_df.apply(classify_card, axis=1)

# Save to new CSV
combined_df.to_csv("arkhamdb_player_cards_classified.csv", index=False)
print("Combined player cards with classification saved to arkhamdb_player_cards_classified.csv")
