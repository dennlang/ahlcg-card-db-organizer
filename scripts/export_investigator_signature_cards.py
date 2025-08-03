import pandas as pd

# Load personal collection and investigator set reference
cards_df = pd.read_csv("arkhamdb_cards_personal.csv")
sets_ref = pd.read_csv("investigator_sets_reference.csv")

# Prepare a list to collect the filtered cards
filtered_cards = []

for _, row in sets_ref.iterrows():
    set_name = row['set_name']
    last_pos = row.get('last_investigator_signature_pos', None)
    if pd.isnull(last_pos):
        continue  # Skip sets with no position info
    try:
        last_pos = int(last_pos)
    except (ValueError, TypeError):
        continue
    # Filter cards for this set
    set_cards = cards_df[cards_df['pack_name'] == set_name] if 'pack_name' in cards_df.columns else cards_df[cards_df['pack_code'] == set_name]
    # Sort by position if available, else by code
    if 'position' in set_cards.columns:
        set_cards_sorted = set_cards.sort_values('position', ascending=True)
        filtered = set_cards_sorted[set_cards_sorted['position'] <= last_pos]
    else:
        set_cards_sorted = set_cards.sort_values('code', ascending=True)
        filtered = set_cards_sorted.head(last_pos)
    filtered_cards.append(filtered)

# Concatenate all filtered cards into a single DataFrame
all_filtered = pd.concat(filtered_cards, ignore_index=True)

# Save to CSV
all_filtered.to_csv('investigator_and_signature_cards.csv', index=False)
print("Saved investigator_and_signature_cards.csv with all cards up to the last investigator+signature position for each set.")
