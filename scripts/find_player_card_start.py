print("This script is currently disabled to prevent overwriting existing values in investigator_sets_reference.csv.")
exit(0)

# --- Script logic below is commented out to preserve code ---
# import pandas as pd
#
# # Load the personal collection and set reference
# cards_df = pd.read_csv("arkhamdb_cards_personal.csv")
# sets_ref = pd.read_csv("investigator_sets_reference.csv")
#
# # Only use sets in the reference list
# sets_to_check = sets_ref['set_name'].tolist()
#
# # Prepare to collect user responses
# last_investigator_sig_positions = []
#
# for set_idx, set_name in enumerate(sets_to_check):
#     print(f"\nSet: {set_name}")
#     # Filter cards for this set
#     set_cards = cards_df[cards_df['pack_name'] == set_name] if 'pack_name' in cards_df.columns else cards_df[cards_df['pack_code'] == set_name]
#     # Sort by position (ascending) if the column exists, otherwise by code
#     if 'position' in set_cards.columns:
#         set_cards_sorted = set_cards.sort_values('position', ascending=True)
#     else:
#         set_cards_sorted = set_cards.sort_values('code', ascending=True)
#
#     # Show the first 30 cards (or all if fewer)
#     preview = set_cards_sorted.head(30)
#     for idx, row in preview.iterrows():
#         print(f"{idx+1}. {row.get('name', 'Unknown')} (type: {row.get('type_code', 'Unknown')}, code: {row.get('code', 'Unknown')}, position: {row.get('position', 'N/A')})")
#
#     default_response = None
#     if len(preview) < 30 and len(preview) > 0:
#         # Use the actual position value of the last card in the preview, if available
#         last_card = preview.iloc[-1]
#         last_position = last_card.get('position', None)
#         if pd.notnull(last_position):
#             default_response = str(int(last_position))
#         else:
#             default_response = str(len(preview))
#
#     prompt = "\nPlease enter the position (1-based) of the LAST investigator + signature card in this set, or press Enter to skip:"
#     if default_response:
#         prompt += f" [default: {default_response}]"
#     print(prompt)
#     print("Type 'cancel' to stop and save progress.")
#     pos = input()
#     if pos.strip().lower() == 'cancel':
#         print("Cancelling and saving progress so far...")
#         break
#     if not pos.strip() and default_response:
#         pos = default_response
#     # Save the response (as int if possible, else None)
#     try:
#         pos_val = int(pos)
#     except (ValueError, TypeError):
#         pos_val = None
#     last_investigator_sig_positions.append(pos_val)
#
# # Fill the rest with None if cancelled early
# while len(last_investigator_sig_positions) < len(sets_to_check):
#     last_investigator_sig_positions.append(None)
#
# # Add the responses as a new column in investigator_sets_reference.csv
# sets_ref['last_investigator_signature_pos'] = last_investigator_sig_positions
# sets_ref.to_csv('investigator_sets_reference.csv', index=False)
# print("Updated investigator_sets_reference.csv with last_investigator_signature_pos column.")
