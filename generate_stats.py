import pandas as pd
import random

# Generate random names
names = []
with open("names.txt", "r") as f:
    for line in f:
        names.append(line.strip())

f.close()

# Define stats attributes
attributes = ['throw', 'accuracy', 'speed', 'defense', 'agility', 'catch']

# Create a DataFrame with random stats (values ranging from 70-100)
data = {attr: [random.randint(70, 100) for _ in names] for attr in attributes}
data['name'] = names

# Convert to DataFrame
df = pd.DataFrame(data)

# Reorder to have 'name' first
df = df[['name'] + attributes]

# Save to Excel file
df.to_excel("player_stats.xlsx", index=False)

print("Excel file saved as 'player_stats.xlsx'")