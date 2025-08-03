import pandas as pd

# Load the filtered investigator and signature cards
cards_df = pd.read_csv("investigator_and_signature_cards.csv")

# Prepare a column for links
cards_df['links_to_card_by_id'] = None

# Group by set
if 'pack_name' in cards_df.columns:
    set_group = cards_df.groupby('pack_name')
else:
    set_group = cards_df.groupby('pack_code')


for set_name, group in set_group:
    group_sorted = group.sort_values('position' if 'position' in group.columns else 'code', ascending=True)
    if group_sorted.empty:
        continue
    last_investigator_idx = None
    last_investigator_code = None
    skip_set = False
    for idx, row in group_sorted.iterrows():
        if str(row.get('type_name', '')).lower() == 'investigator':
            # If previous card was also an investigator, skip this set
            if last_investigator_idx is not None and idx == last_investigator_idx + 1:
                skip_set = True
                break
            last_investigator_idx = idx
            last_investigator_code = row['code']
            # Set the investigator's own code in links_to_card_by_id
            cards_df.at[row.name, 'links_to_card_by_id'] = row['code']
        else:
            if last_investigator_code is not None:
                cards_df.at[row.name, 'links_to_card_by_id'] = last_investigator_code
    if skip_set:
        continue

# Save the updated DataFrame back to the same CSV
cards_df.to_csv('investigator_and_signature_cards.csv', index=False)
print("Updated investigator_and_signature_cards.csv with links_to_card_by_id column.")
