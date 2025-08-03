import pandas as pd
import ast

# Load the organized collection
collection = pd.read_csv("organized_collection.csv", dtype={'code': str, 'links_to_card_by_id': str})

# Remove apostrophe for processing, but keep for output
collection['code_raw'] = collection['code'].str.lstrip("'")
if 'links_to_card_by_id' in collection.columns:
    collection['links_to_card_by_id_raw'] = collection['links_to_card_by_id'].str.lstrip("'")
else:
    collection['links_to_card_by_id_raw'] = None

# Find cards with empty links_to_card_by_id
unlinked = collection[collection['links_to_card_by_id'].isnull() | (collection['links_to_card_by_id'].astype(str).str.strip() == '')].copy()

# Find all bonded sets
bonded_sets = []
visited = set()
for idx, row in unlinked.iterrows():
    # Check for bonded_cards or bonded_to
    bonded_codes = []
    if 'bonded_cards' in row and pd.notnull(row['bonded_cards']):
        try:
            # Try to parse as list of dicts
            bonded_list = ast.literal_eval(row['bonded_cards'])
            if isinstance(bonded_list, list):
                for entry in bonded_list:
                    if isinstance(entry, dict) and 'code' in entry:
                        bonded_codes.append(str(entry['code']).zfill(len(row['code_raw'])))
        except Exception:
            pass
    if bonded_codes:
        set_codes = [row['code_raw']] + bonded_codes
        # Only process if not already visited
        if not any(code in visited for code in set_codes):
            bonded_sets.append(set_codes)
            visited.update(set_codes)

# Prepare preview of what the update would look like
preview = collection.copy()
for set_codes in bonded_sets:
    first_code = set_codes[0]
    for code in set_codes:
        idxs = preview[preview['code_raw'] == code].index
        if len(idxs) > 0:
            # Add apostrophe and pad to match output
            preview.at[idxs[0], 'links_to_card_by_id'] = f"'{first_code.zfill(len(first_code))}"

# Print preview of changes
print("Preview of bonded card linking (code, name, links_to_card_by_id):")
for set_codes in bonded_sets:
    for code in set_codes:
        row = preview[preview['code_raw'] == code].iloc[0]
        print(f"{row['code']}, {row['name']}, {row['links_to_card_by_id']}")
