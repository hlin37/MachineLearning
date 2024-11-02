import tkinter as tk
from tkinter import ttk

def create_full_bracket(notebook, round_letters, chosen_key):
    match_data = round_letters.get(chosen_key, {})
    rect_width = 150
    rect_height = 30
    spacing_y = 20  # Space between matches vertically
    group_spacing_y = 60  # Additional space between groups of matches
    round_spacing = 200  # Horizontal spacing between rounds

    # Sample data for demonstration purposes
    match_results = {
        'A': ('Maryland', 10, 'DC Recruits', 8),
        'B': ('Virginia', 15, 'George', 12),
        'C': ('Clownies', 9, 'Richmond', 7),
        'D': ('James', 14, 'Pitts', 11),
        'E': ('Maryland', 13, 'Virginia', 12),
        'F': ('Clownies', 16, 'James', 14),
        'G': ('Maryland', 18, 'Clownies', 17),
        'H': ('DC Recruits', 20, 'George', 19),
        'I': ('Richmond', 25, 'Pitt', 23),
        'J': ('DC', 25, 'Richmond', 23),
        'K': ('James Madison', 14, 'Virginia', 12),
        'L': ('George', 28, 'Pitt', 26),
        'M': ('George', 28, 'Pitt', 26),
        'N': ('George', 28, 'Pitt', 26),
        'O': ('George', 28, 'Pitt', 26),
        'P': ('George', 28, 'Pitt', 26),
        'Q': ('George', 28, 'Pitt', 26),
        'R': ('George', 28, 'Pitt', 26),
        'S': ('George', 28, 'Pitt', 26),
        'T': ('George', 28, 'Pitt', 26),
        'U': ('George', 28, 'Pitt', 26),
        # Additional matches can be added as needed
    }

    for place, rounds in sorted(match_data.items()):
        # Create a frame for each tab
        place_frame = ttk.Frame(notebook)
        if place == -1:
            place = "Crossover"
        notebook.add(place_frame, text=f"Place {place} Bracket")
        
        # Create a canvas inside each frame for drawing
        canvas = tk.Canvas(place_frame, width=1500, height=800)
        canvas.pack(fill="both", expand=True)

        start_x = 50  # Initial X position for drawing rounds
        previous_round_centers = []

        for round_num, groups in enumerate(rounds, start=1):
            current_round_centers = []

            for group_index, group in enumerate(groups):
                if group in match_results:
                    winner_name, winner_score, loser_name, loser_score = match_results[group]

                    # Calculate Y position for centering
                    if not previous_round_centers:
                        # First round, calculate positions based on index
                        y_pos = 50 + (rect_height * 2 + spacing_y) * group_index
                    else:
                        if 'EFGH' in groups:
                            y_pos = 50 + (rect_height * 2 + spacing_y) * group_index
                        else:
                            # Center the current match between the previous two matches it depends on
                            if group_index * 2 < len(previous_round_centers):
                                prev_centers = previous_round_centers[group_index * 2:group_index * 2 + 2]

                                if len(prev_centers) == 2:
                                    # Center the match between two corresponding matches from the previous round
                                    y_pos = (prev_centers[0][1] + prev_centers[1][1]) // 2
                                else:
                                    y_pos = prev_centers[0][1]
                            else:
                                y_pos = previous_round_centers[-1][1] + (rect_height + spacing_y)

                    # Draw the winner and loser rectangles
                    canvas.create_rectangle(start_x, y_pos, start_x + rect_width, y_pos + rect_height, fill="blue")
                    canvas.create_text(start_x + 5, y_pos + rect_height // 2, text=f"{winner_name} {winner_score}", anchor="w", fill="white")
                    canvas.create_rectangle(start_x, y_pos + rect_height, start_x + rect_width, y_pos + 2 * rect_height, fill="red")
                    canvas.create_text(start_x + 5, y_pos + 1.5 * rect_height, text=f"{loser_name} {loser_score}", anchor="w", fill="white")

                    # Store center positions for the next round centering
                    center_x = start_x + rect_width
                    center_y = y_pos + rect_height  # Center Y-position between winner and loser
                    current_round_centers.append((center_x, center_y))

            # Update previous round centers for next iteration
            previous_round_centers = current_round_centers
            start_x += round_spacing  # Move to the next round horizontally

# Create the main Tkinter window and notebook
root = tk.Tk()
root.title("Full Tournament Bracket")

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

# Example round_letters dictionary for testing
round_letters = {
    (1, 8) :  {1: ["ABCD", "EF", "G"], 3: ["K"], 5: ["HI", "J"], 7: ["L"]},
    (2, 8) : {1: ["AB", "C"], 2: ["DE", "FG", "H", "I"], 5: ["J"], 7: ["K"],},
    (4, 8) : {1: ["A"], 2: ["B", "C"], 4: ["DE", "F", "G"], 7: ["H"]},
    (6, 8) : {1: ["AB", "CD", "E"], 2: ["F", "G"], 4: ["HI", "J", "K"], 6: ["L", "M"]},
    (1, 10) : {1: ['ABCD', "EF", "G"], 3: ["K"], 5: ["HI", "J"], 7: ["L"], 9: ["M"]},
    (2, 10) : {1: ["AB", "C"], 2: ["DE", "FG", "H", "I"], 5: ["J"], 7: ["K"], 9: ["L"]},
    (4, 10) : {1: ["A"], 2: ["B", "C"], 4: ["DE", "F", "G"], 7: ["H"], 9: ["I"]},
    (6, 10) : {1: ["AB", "C"], 2: ["D", "E"], 5: ["F"], 6: ["GH", "I", "J"], 9: ["K"]},
    (1, 12) : {1: ['ABCD', "EF", "G"], 3: ["K"], 5: ["HI", "J"], 7: ["L"], 9: ["MN", "O"], 10: ["P", "Q"]},
    (2, 12) : {1: ["A"], 2: ["BC", "D", "E"], 5: ["F"], 7: ["GH", "IJ", "K"], 9: ["L"], 11: ["M"]},
    (4, 12) : {1: ["A"], 2: ["B", "C"], 4: ["DE", "F", "G"], 7: ["H"], 9: ["IJ", "K"], 10:["L", "M"]},
    (6, 12) : {1: ['AB', "C"], 2: ["D", "E"], 4: ["GH", "I", "F"], 6: ["JK", "LM", "N"], 9: ["O"], 11: ["P"]},
    (1, 16) : {1: ["ABCD", "EFGH", "IJ", "K"], -1: ["PQ"], 3: ["L"], 5: ["MN", "O"], 7: ["RSVW", "TX", "UY", "Z"], 11:["{"], 13:["|}", "~"], 15: ["["]},
    (1, 20) : {1: ["ABCD", "EFGH", "IJ", "K"], -1: ["PQ"], 3: ["L"], 5: ["MN", "O"], 7: ["RSVW", "TX", "UY", "Z"], 11:["{"], 13:["|}", "~"], 15: ["["], 17:["]^", "_"], 19: ["`"]}
}

# Hard-coded chosen key for testing
chosen_key = (1, 16)

# Create the full bracket visualization inside the notebook
create_full_bracket(notebook, round_letters, chosen_key)

root.mainloop()
