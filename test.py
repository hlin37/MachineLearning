import numpy as np
import pandas as pd

class FrisbeeActionPredictor:
    def __init__(self):
        self.actions = ["Pull", "Swing", "Pass", "Dump", "Dish", "Huck", "Stall", "Block",
                        "Dropped Pass", "Dropped Huck", "Throwaway", "Huck Throwaway", "Score"]
        self.action_to_index = {action: i for i, action in enumerate(self.actions)}
        
        # Load the transition matrix
        self.transition_df = pd.read_excel('manualCreatedActionMatrix.xlsx')
        self.transition_matrix = self.transition_df.to_numpy()

    # Continuous scaling functions for each action based on distance
    def huck_modifier(self, distance):
        return max(0.1, distance / 100)

    def score_modifier(self, distance):
        return min(2.0, (100 - distance) / 50)

    def pass_modifier(self, distance):
        return max(0.8, 1 - (100 - distance) / 300)

    def dump_dish_modifier(self, distance):
        return min(2.0, (100 - distance) / 50)

    def swing_modifier(self, distance):
        return max(0.8, 1 - (100 - distance) / 200)

    def stall_modifier(self, distance):
        return 1.0

    def drop_modifier(self, distance):
        return min(1.5, 1 + (100 - distance) / 200)

    def block_modifier(self, distance):
        return min(2.0, (100 - distance) / 50)

    def throwaway_modifier(self, distance):
        return min(1.5, 1 + (100 - distance) / 200)

    # Adjust probabilities based on continuous distance functions
    def adjust_probabilities(self, distance_to_goal):
        adjustment_matrix = np.ones_like(self.transition_matrix)

        # Get the continuous modifiers for each action based on distance
        huck_mod = self.huck_modifier(distance_to_goal)
        score_mod = self.score_modifier(distance_to_goal)
        pass_mod = self.pass_modifier(distance_to_goal)
        dump_dish_mod = self.dump_dish_modifier(distance_to_goal)
        swing_mod = self.swing_modifier(distance_to_goal)
        drop_mod = self.drop_modifier(distance_to_goal)
        block_mod = self.block_modifier(distance_to_goal)
        throwaway_mod = self.throwaway_modifier(distance_to_goal)

        # Apply modifications to relevant actions
        huck_idx = self.action_to_index["Huck"]
        score_idx = self.action_to_index["Score"]
        pass_idx = self.action_to_index["Pass"]
        dump_idx = self.action_to_index["Dump"]
        dish_idx = self.action_to_index["Dish"]
        swing_idx = self.action_to_index["Swing"]
        drop_idx = self.action_to_index["Dropped Pass"]
        dropped_huck_idx = self.action_to_index["Dropped Huck"]
        block_idx = self.action_to_index["Block"]
        throwaway_idx = self.action_to_index["Throwaway"]
        huck_throwaway_idx = self.action_to_index["Huck Throwaway"]

        for i in range(len(self.actions)):
            adjustment_matrix[i][huck_idx] *= huck_mod
            adjustment_matrix[i][score_idx] *= score_mod
            adjustment_matrix[i][pass_idx] *= pass_mod
            adjustment_matrix[i][dump_idx] *= dump_dish_mod
            adjustment_matrix[i][dish_idx] *= dump_dish_mod
            adjustment_matrix[i][swing_idx] *= swing_mod
            adjustment_matrix[i][drop_idx] *= drop_mod
            adjustment_matrix[i][dropped_huck_idx] *= drop_mod
            adjustment_matrix[i][block_idx] *= block_mod
            adjustment_matrix[i][throwaway_idx] *= throwaway_mod
            adjustment_matrix[i][huck_throwaway_idx] *= throwaway_mod

        # Adjust the original transition matrix with the continuous modifiers
        adjusted_matrix = self.transition_matrix * adjustment_matrix

        # Re-normalize each row to ensure probabilities sum to 1
        row_sums = np.sum(adjusted_matrix, axis=1, keepdims=True)
        adjusted_matrix = np.divide(adjusted_matrix, row_sums, where=row_sums != 0)

        return adjusted_matrix

    # Predict the next action using the Markov Chain
    def predict_next_action(self, current_action, distance_to_goal):
        # Adjust probabilities based on distance
        adjusted_matrix = self.adjust_probabilities(distance_to_goal)

        # Get probabilities for the current action
        current_idx = self.action_to_index[current_action]
        markov_probabilities = adjusted_matrix[current_idx]

        # Sample the next action
        next_action_idx = np.random.choice(len(self.actions), p=markov_probabilities)
        return self.actions[next_action_idx]

# Example usage:
predictor = FrisbeeActionPredictor()
next_action = None
while (next_action != "Score"):
    next_action = predictor.predict_next_action("Pass", 50)
    print(next_action)
