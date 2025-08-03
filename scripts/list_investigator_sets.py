import pandas as pd

# Load the personal collection card data from CSV
cards_df = pd.read_csv("arkhamdb_cards_personal.csv")

# Filter for investigator cards
investigator_mask = (
    (cards_df['skill_willpower'] > 0) &
    (cards_df['skill_intellect'] > 0) &
    (cards_df['skill_combat'] > 0) &
    (cards_df['skill_agility'] > 0) &
    (cards_df['health'] > 0) &
    (cards_df['sanity'] > 0)
)
investigators = cards_df[investigator_mask].copy()

# Add a column for set name (pack_name or pack_code)
investigators['set_name'] = investigators.apply(
    lambda row: row['pack_name'] if 'pack_name' in row and pd.notnull(row['pack_name']) else row.get('pack_code', 'Unknown'), axis=1
)

# Sort by set name, then by investigator name
investigators_sorted = investigators.sort_values(['set_name', 'name'])


# Create a reference CSV for sets and main_campaigns
main_campaigns = {
    "Core Set",
    "The Dunwich Legacy",
    "The Path to Carcosa",
    "The Forgotten Age",
    "The Circle Undone",
    "The Dream-Eaters",
    "The Innsmouth Conspiracy",
    "Edge of the Earth Investigator Expansion",
    "The Scarlet Keys Investigator Expansion",
    "The Feast of Hemlock Vale Investigator Expansion",
    "The Drowned City Investigator Expansion"
}

# Get all unique set names from investigators
all_sets = sorted(investigators['set_name'].dropna().unique())

# Build DataFrame for reference
sets_df = pd.DataFrame({
    'set_name': all_sets,
    'main_campaign': [s in main_campaigns for s in all_sets]
})

# Save to CSV
sets_df.to_csv('investigator_sets_reference.csv', index=False)
print("Reference CSV 'investigator_sets_reference.csv' created with set_name and main_campaign columns.")
