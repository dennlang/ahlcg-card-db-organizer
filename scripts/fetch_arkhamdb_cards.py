import requests
import pandas as pd

# Fetch all cards from the public API
url = "https://arkhamdb.com/api/public/cards/"
response = requests.get(url)
response.raise_for_status()  # Raise error if request failed

cards = response.json()

# Convert to DataFrame for easy tabular display
df = pd.DataFrame(cards)

# Save the full table to a CSV file for verification
df.to_csv("arkhamdb_cards.csv", index=False)


# Only fetch and save all cards to CSV
print("Saved all cards to arkhamdb_cards.csv")
print(df[["code", "name", "type_code", "faction_code"]].head(20))
