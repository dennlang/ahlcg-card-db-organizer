import pandas as pd

# Load the filtered investigator and signature cards
cards_df = pd.read_csv("investigator_and_signature_cards.csv")

# Prepare a list to collect updated cards
updated_cards = []

# Group by set
if 'pack_name' in cards_df.columns:
    set_group = cards_df.groupby('pack_name')
else:
    set_group = cards_df.groupby('pack_code')

for set_name, group in set_group:
    group_sorted = group.sort_values('position' if 'position' in group.columns else 'code', ascending=True).reset_index(drop=True)
    if group_sorted.empty:
        continue
    # The first card must be an investigator
    if not group_sorted.iloc[0].get('type_name', '').lower() == 'investigator':
        continue
    investigator_code = group_sorted.iloc[0]['code']
    skip_set = False
    # Check for pattern: if any card after the first is an investigator, skip this set
    for idx in range(1, len(group_sorted)):
        if str(group_sorted.iloc[idx].get('type_name', '')).lower() == 'investigator':
            skip_set = True
            break
    if skip_set:
        continue
    # Assign links_to_card_by_id
    group_sorted['links_to_card_by_id'] = investigator_code
    updated_cards.append(group_sorted)

# Concatenate all updated cards into a single DataFrame
if updated_cards:
    all_updated = pd.concat(updated_cards, ignore_index=True)
    all_updated.to_csv('signature_cards_linked.csv', index=False)
    print("Saved signature_cards_linked.csv with signature cards linked to their investigator.")
else:
    print("No sets matched the pattern. No output generated.")
