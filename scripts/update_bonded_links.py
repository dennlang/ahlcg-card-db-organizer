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
            bonded_list = ast.literal_eval(row['bonded_cards'])
            if isinstance(bonded_list, list):
                for entry in bonded_list:
                    if isinstance(entry, dict) and 'code' in entry:
                        bonded_codes.append(str(entry['code']).zfill(len(row['code_raw'])))
        except Exception:
            pass
    if bonded_codes:
        set_codes = [row['code_raw']] + bonded_codes
        if not any(code in visited for code in set_codes):
            bonded_sets.append(set_codes)
            visited.update(set_codes)

# Update the links_to_card_by_id column for bonded sets
for set_codes in bonded_sets:
    first_code = set_codes[0]
    for code in set_codes:
        idxs = collection[collection['code_raw'] == code].index
        if len(idxs) > 0:
            collection.at[idxs[0], 'links_to_card_by_id'] = f"'{first_code.zfill(len(first_code))}"


# Add 'binder' column
def get_binder(row, code_to_faction):
    linked_code = str(row['links_to_card_by_id']).lstrip("'") if pd.notnull(row['links_to_card_by_id']) and str(row['links_to_card_by_id']).strip() != '' else None
    if linked_code and linked_code in code_to_faction:
        return code_to_faction[linked_code]
    return row['faction_name']

code_to_faction = dict(zip(collection['code_raw'], collection['faction_name']))
collection['binder'] = collection.apply(lambda row: get_binder(row, code_to_faction), axis=1)

# Add 'binder_category' column
def get_binder_category(row, code_to_type, code_to_links):
    # Investigator if type is investigator or links_to_card_by_id points to an investigator
    if row['type_code'] == 'investigator':
        return 'investigator'
    linked_code = str(row['links_to_card_by_id']).lstrip("'") if pd.notnull(row['links_to_card_by_id']) and str(row['links_to_card_by_id']).strip() != '' else None
    if linked_code and code_to_type.get(linked_code) == 'investigator':
        return 'investigator'
    return 'player_card'

# Build a mapping from code (raw, no apostrophe) to type_code
code_to_type = dict(zip(collection['code_raw'], collection['type_code']))
code_to_links = dict(zip(collection['code_raw'], collection['links_to_card_by_id']))
collection['binder_category'] = collection.apply(lambda row: get_binder_category(row, code_to_type, code_to_links), axis=1)

# Drop helper columns
collection = collection.drop(columns=['code_raw', 'links_to_card_by_id_raw'])

# Save the updated DataFrame back to the same CSV
collection.to_csv('organized_collection.csv', index=False)
print("Updated organized_collection.csv with bonded links and binder column.")
