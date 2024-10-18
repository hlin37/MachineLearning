import numpy as np
import pandas as pd
import re

# List of actions to track
actions = ["Pull", "Swing", "Pass", "Dropped pass", "Block", "Score", "Dump", "Dish",
           "Huck throwaway", "Huck", "Stall", "Dropped huck"]

# Dictionary to map actions to indices
action_to_index = {action: i for i, action in enumerate(actions)}
index_to_action = {i: action for i, action in enumerate(actions)}

# Initialize the transition matrix (counts)
transition_matrix = np.zeros((len(actions), len(actions)))

# Function to extract action from a line
def extract_action(line):
    for act in actions:
        if act in line:
            return act
    return None

# Reading the file and calculating action transitions
previous_action = None
with open("gameEvent.txt", "r") as file:
    for line in file:
        current_action = extract_action(line)
        if current_action and previous_action:
            current_idx = action_to_index[previous_action]
            next_idx = action_to_index[current_action]
            transition_matrix[current_idx][next_idx] += 1
        previous_action = current_action

# Normalize the transition matrix row-wise to create a probability matrix
# Avoid division by zero in rows with all zeros by using np.where
row_sums = np.sum(transition_matrix, axis=1, keepdims=True)
probability_matrix = np.divide(transition_matrix, row_sums, where=row_sums != 0)

# Create a DataFrame from the probability matrix
probability_df = pd.DataFrame(probability_matrix, index=actions, columns=actions)
probability_df.to_excel("actionMatrix.xlsx")

# Display the DataFrame with probabilities
print("Transition Probability Matrix as DataFrame:")
print(probability_df)
