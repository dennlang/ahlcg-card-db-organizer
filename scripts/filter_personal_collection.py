import pandas as pd

# Load the full card data from CSV
cards_df = pd.read_csv("arkhamdb_cards.csv")

# Omit specific sets you don't have
sets_to_omit = {"Revised Core Set"}

# If pack_name is present, filter by it; otherwise, use pack_code
if 'pack_name' in cards_df.columns:
    filtered_df = cards_df[~cards_df['pack_name'].isin(sets_to_omit)]
else:
    filtered_df = cards_df.copy()  # No filtering if pack_name not present

# Save the filtered collection to a new CSV
filtered_df.to_csv("arkhamdb_cards_personal.csv", index=False)
print("Filtered personal collection saved to arkhamdb_cards_personal.csv, omitting sets:", sets_to_omit)
