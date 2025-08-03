import pandas as pd

# Load both CSVs, forcing 'code' columns to string to preserve leading zeros
cards_df = pd.read_csv("arkhamdb_cards_personal.csv", dtype={'code': str})
sig_df = pd.read_csv("investigator_and_signature_cards.csv", dtype={'code': str, 'links_to_card_by_id': str})

# Merge on 'code' (card id)
merged = cards_df.merge(sig_df[['code', 'links_to_card_by_id']], on='code', how='left')

# Ensure both 'code' and 'links_to_card_by_id' are zero-padded strings of the same width, prefixed with an apostrophe for Excel
if 'code' in merged.columns:
    max_code_len = merged['code'].astype(str).str.len().max()
    merged['code'] = merged['code'].apply(lambda x: f"'{str(x).zfill(max_code_len)}")
if 'links_to_card_by_id' in merged.columns:
    def pad_and_prefix(x):
        if pd.isnull(x):
            return x
        s = str(x).zfill(max_code_len)
        return f"'{s}"
    merged['links_to_card_by_id'] = merged['links_to_card_by_id'].apply(pad_and_prefix)

# Save to new CSV
merged.to_csv("organized_collection.csv", index=False)
print("Saved organized_collection.csv with all personal cards and investigator/signature links.")
