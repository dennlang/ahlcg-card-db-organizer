import pandas as pd
import ast

# Load the personal collection
cards_df = pd.read_csv("arkhamdb_cards_personal.csv")

# Find cards with bonded relationships
bonded_cards = []

for idx, row in cards_df.iterrows():
    # Check for a 'bonded_cards' or 'bonded_to' column, or look for 'Bonded' in text fields
    bonded = False
    bonded_info = None
    # Check for explicit bonded columns
    if 'bonded_cards' in row and pd.notnull(row['bonded_cards']):
        bonded = True
        bonded_info = row['bonded_cards']
    elif 'bonded_to' in row and pd.notnull(row['bonded_to']):
        bonded = True
        bonded_info = row['bonded_to']
    # Check for 'Bonded' in text fields
    elif 'text' in row and isinstance(row['text'], str) and 'bonded' in row['text'].lower():
        bonded = True
        bonded_info = row['text']
    if bonded:
        bonded_cards.append({
            'code': row.get('code', ''),
            'name': row.get('name', ''),
            'bonded_info': bonded_info
        })

if bonded_cards:
    print("Bonded cards found:")
    for card in bonded_cards:
        print(f"{card['code']}: {card['name']} | Info: {card['bonded_info']}")
else:
    print("No bonded cards found.")
