# # import numpy as np
# # import pandas as pd

# # class FrisbeeActionPredictor:
# #     def __init__(self):
# #         self.actions = ["Pull", "Swing", "Pass", "Dump", "Dish", "Huck", "Stall", "Block",
# #                         "Dropped Pass", "Dropped Huck", "Throwaway", "Huck Throwaway", "Score"]
# #         self.action_to_index = {action: i for i, action in enumerate(self.actions)}
        
# #         # Load the transition matrix
# #         self.transition_df = pd.read_excel('manualCreatedActionMatrix.xlsx')
# #         self.transition_matrix = self.transition_df.to_numpy()

# #     # Continuous scaling functions for each action based on distance
# #     def huck_modifier(self, distance):
# #         return max(0.1, distance / 100)

# #     def score_modifier(self, distance):
# #         return min(2.0, (100 - distance) / 50)

# #     def pass_modifier(self, distance):
# #         return max(0.8, 1 - (100 - distance) / 300)

# #     def dump_dish_modifier(self, distance):
# #         return min(2.0, (100 - distance) / 50)

# #     def swing_modifier(self, distance):
# #         return max(0.8, 1 - (100 - distance) / 200)

# #     def stall_modifier(self, distance):
# #         return 1.0

# #     def drop_modifier(self, distance):
# #         return min(1.5, 1 + (100 - distance) / 200)

# #     def block_modifier(self, distance):
# #         return min(2.0, (100 - distance) / 50)

# #     def throwaway_modifier(self, distance):
# #         return min(1.5, 1 + (100 - distance) / 200)

# #     # Adjust probabilities based on continuous distance functions
# #     def adjust_probabilities(self, distance_to_goal):
# #         adjustment_matrix = np.ones_like(self.transition_matrix)

# #         # Get the continuous modifiers for each action based on distance
# #         huck_mod = self.huck_modifier(distance_to_goal)
# #         score_mod = self.score_modifier(distance_to_goal)
# #         pass_mod = self.pass_modifier(distance_to_goal)
# #         dump_dish_mod = self.dump_dish_modifier(distance_to_goal)
# #         swing_mod = self.swing_modifier(distance_to_goal)
# #         drop_mod = self.drop_modifier(distance_to_goal)
# #         block_mod = self.block_modifier(distance_to_goal)
# #         throwaway_mod = self.throwaway_modifier(distance_to_goal)

# #         # Apply modifications to relevant actions
# #         huck_idx = self.action_to_index["Huck"]
# #         score_idx = self.action_to_index["Score"]
# #         pass_idx = self.action_to_index["Pass"]
# #         dump_idx = self.action_to_index["Dump"]
# #         dish_idx = self.action_to_index["Dish"]
# #         swing_idx = self.action_to_index["Swing"]
# #         drop_idx = self.action_to_index["Dropped Pass"]
# #         dropped_huck_idx = self.action_to_index["Dropped Huck"]
# #         block_idx = self.action_to_index["Block"]
# #         throwaway_idx = self.action_to_index["Throwaway"]
# #         huck_throwaway_idx = self.action_to_index["Huck Throwaway"]

# #         for i in range(len(self.actions)):
# #             adjustment_matrix[i][huck_idx] *= huck_mod
# #             adjustment_matrix[i][score_idx] *= score_mod
# #             adjustment_matrix[i][pass_idx] *= pass_mod
# #             adjustment_matrix[i][dump_idx] *= dump_dish_mod
# #             adjustment_matrix[i][dish_idx] *= dump_dish_mod
# #             adjustment_matrix[i][swing_idx] *= swing_mod
# #             adjustment_matrix[i][drop_idx] *= drop_mod
# #             adjustment_matrix[i][dropped_huck_idx] *= drop_mod
# #             adjustment_matrix[i][block_idx] *= block_mod
# #             adjustment_matrix[i][throwaway_idx] *= throwaway_mod
# #             adjustment_matrix[i][huck_throwaway_idx] *= throwaway_mod

# #         # Adjust the original transition matrix with the continuous modifiers
# #         adjusted_matrix = self.transition_matrix * adjustment_matrix

# #         # Re-normalize each row to ensure probabilities sum to 1
# #         row_sums = np.sum(adjusted_matrix, axis=1, keepdims=True)
# #         adjusted_matrix = np.divide(adjusted_matrix, row_sums, where=row_sums != 0)

# #         return adjusted_matrix

# #     # Predict the next action using the Markov Chain
# #     def predict_next_action(self, current_action, distance_to_goal):
# #         # Adjust probabilities based on distance
# #         adjusted_matrix = self.adjust_probabilities(distance_to_goal)

# #         # Get probabilities for the current action
# #         current_idx = self.action_to_index[current_action]
# #         markov_probabilities = adjusted_matrix[current_idx]

# #         # Sample the next action
# #         next_action_idx = np.random.choice(len(self.actions), p=markov_probabilities)
# #         return self.actions[next_action_idx]

# # # Example usage:
# # predictor = FrisbeeActionPredictor()
# # next_action = None
# # while (next_action != "Score"):
# #     next_action = predictor.predict_next_action("Pass", 50)
# #     print(next_action)

# import tkinter as tk

# class BracketDisplay(tk.Tk):
#     def __init__(self, teams):
#         super().__init__()
#         self.title("Tournament Bracket")

#         # Number of teams and rounds
#         self.teams = teams
#         self.num_teams = len(teams)
#         self.num_rounds = self.calculate_rounds(self.num_teams)

#         # Display the bracket
#         self.display_bracket()

#     def calculate_rounds(self, num_teams):
#         rounds = 0
#         while num_teams > 1:
#             num_teams //= 2
#             rounds += 1
#         return rounds

#     def display_bracket(self):
#         round_teams = self.teams

#         for round_num in range(self.num_rounds):
#             # Frame for each round
#             round_frame = tk.Frame(self, padx=20, pady=10)
#             round_frame.grid(row=0, column=round_num * 2)

#             # Display each match in the round
#             next_round_teams = []
#             for i in range(0, len(round_teams), 2):
#                 # Team 1
#                 team1_label = tk.Label(round_frame, text=round_teams[i], font=("Arial", 10), width=15, relief="ridge")
#                 team1_label.pack()

#                 # Spacer between team1 and team2
#                 spacer = tk.Label(round_frame, text="vs", font=("Arial", 10))
#                 spacer.pack()

#                 # Team 2
#                 if i + 1 < len(round_teams):
#                     team2_label = tk.Label(round_frame, text=round_teams[i + 1], font=("Arial", 10), width=15, relief="ridge")
#                     team2_label.pack()
#                     next_round_teams.append(f"Winner of {round_teams[i]} vs {round_teams[i + 1]}")
#                 else:
#                     # Handle odd number of teams (bye)
#                     next_round_teams.append(round_teams[i])

#             round_teams = next_round_teams

#             # Draw lines between rounds (optional)
#             if round_num < self.num_rounds - 1:
#                 line_frame = tk.Frame(self, padx=5)
#                 line_frame.grid(row=0, column=(round_num * 2) + 1)
#                 for _ in range(len(next_round_teams)):
#                     line = tk.Label(line_frame, text="|", font=("Arial", 5))
#                     line.pack(pady=20)

#         # Final match
#         final_frame = tk.Frame(self, padx=20, pady=10)
#         final_frame.grid(row=0, column=self.num_rounds * 2)
#         final_label = tk.Label(final_frame, text="Champion", font=("Arial", 12, "bold"), width=15, relief="solid")
#         final_label.pack()

# # List of team names
# teams = ["Team 1", "Team 2", "Team 3", "Team 4", "Team 5", "Team 6", "Team 7", "Team 8"]

# # Create and run the bracket display
# app = BracketDisplay(teams)
# app.mainloop()

import tkinter as tk

def create_bracket(canvas, match_data, first_place_chars):
    # Constants for drawing
    start_x = 50
    start_y = 50
    rect_width = 150
    rect_height = 30
    spacing_y = 20  # Space between rectangles vertically
    round_spacing = 200  # Horizontal spacing between rounds

    # Organize matches by round based on ASCII values
    rounds = {}  # Store matches by round
    for ascii_key, (team1, team2) in match_data.items():
        round_num = ascii_key // 2  # Group matches by round number
        if round_num not in rounds:
            rounds[round_num] = []
        rounds[round_num].append((ascii_key, (team1, team2)))

    match_centers = {}  # Store center points of matches for drawing lines

    # Draw each round
    for round_num, matches in rounds.items():
        # Calculate vertical offset for this round
        vertical_offset = start_y + (rect_height + spacing_y) * (len(matches) * 2) * (round_num + 1)

        for i, (ascii_key, (team1, team2)) in enumerate(matches):
            # Determine if this match is part of the first place bracket
            if chr(ascii_key) in first_place_chars:
                bracket_label = "First Place Bracket"
            else:
                bracket_label = "Other Bracket"

            # Determine the vertical position for this match
            y_pos = vertical_offset - (i + 1) * (rect_height + spacing_y)

            # Determine the winner and loser
            winner = team1 if team1[1] > team2[1] else team2
            loser = team1 if team1[1] <= team2[1] else team2

            # Draw rectangles for the teams
            canvas.create_rectangle(start_x, y_pos, start_x + rect_width, y_pos + rect_height,
                                    fill="blue" if team1 == winner else "red")
            canvas.create_text(start_x + 5, y_pos + rect_height // 2,
                               text=f"{team1[0]} {team1[1]}", anchor="w", fill="white")
            
            canvas.create_rectangle(start_x, y_pos + rect_height,
                                    start_x + rect_width, y_pos + rect_height * 2,
                                    fill="blue" if team2 == winner else "red")
            canvas.create_text(start_x + 5, y_pos + rect_height + rect_height // 2,
                               text=f"{team2[0]} {team2[1]}", anchor="w", fill="white")

            # Store the center point of this match for line drawing
            center_x = start_x + rect_width
            center_y = y_pos + rect_height
            match_centers[ascii_key] = (center_x, center_y)

            # Draw connecting L-shaped lines to the next round
            if round_num < max(rounds.keys()):  # Check if there's a next round
                next_round = round_num + 1
                next_match_index = i // 2  # Each match in the next round corresponds to two matches in this round

                # Ensure the next match index is valid
                if next_match_index < len(rounds[next_round]):
                    next_match_key = rounds[next_round][next_match_index][0]

                    # Only attempt to access match_centers if next_match_key is valid
                    if next_match_key in match_centers:
                        next_center_x, next_center_y = match_centers[next_match_key]

                        # Draw the L-shaped line
                        canvas.create_line(center_x, center_y, center_x + round_spacing, center_y, fill="black")  # Horizontal line
                        canvas.create_line(center_x + round_spacing, center_y, center_x + round_spacing, next_center_y, fill="black")  # Vertical line

    # Draw bracket labels
    for round_num in rounds.keys():
        bracket_label = "First Place Bracket" if round_num == 0 else "Other Bracket"
        label_y = start_y + (rect_height + spacing_y) * (len(rounds[round_num]) * 2) * (round_num + 1) - (rect_height + 20)
        canvas.create_text(start_x + rect_width + 20, label_y, text=bracket_label, font=("Arial", 14, "bold"))

# Create the main Tkinter window and canvas
root = tk.Tk()
root.title("Tournament Bracket")

canvas = tk.Canvas(root, width=1000, height=800)
canvas.pack()

# Example match data: character keys and teams with scores
match_data = {
    65: (("Team A", 10), ("Team B", 8)),  # 'A'
    66: (("Team C", 12), ("Team D", 5)),  # 'B'
    67: (("Team E", 9), ("Team F", 6)),   # 'C'
    68: (("Team G", 11), ("Team H", 7)),  # 'D'
    69: (("Team I", 15), ("Team J", 14)), # 'E'
    70: (("Team K", 13), ("Team L", 9)),  # 'F'
    71: (("Winner A/B", 11), ("Winner C/D", 12)), # Semifinal 1
    72: (("Winner E/F", 10), ("Winner G/H", 9)), # Semifinal 2
    73: (("Final Winner", 15), ("Final Runner-up", 13)), # Final
}

# Characters representing the first place bracket
first_place_chars = "ABCD"  # Matches A, B, C, D, E belong to the first place bracket

# Create the brackets based on the match data and specified bracket chars
create_bracket(canvas, match_data, first_place_chars)

root.mainloop()

