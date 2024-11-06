from team import *
from tournament import *
from handle_tournament import *
from display_month import *

import customtkinter as ctk
import calendar
from tkinter import ttk
import tkinter as tk

class TournamentApp:

    def __init__(self, root, team_generator, tournament_generator, tournament_director):

        self.root = root
        root.title("Ultimate Frisbee")

        ## list of all team objects
        self.teams = team_generator.teamList

        ## list of all tournament objects
        self.tournaments = tournament_generator.tournaments

        self.tournament_generator = tournament_generator

        ## handles which team is going/eligible/invited to which tournament
        self.tournament_director = tournament_director

        ## list of all the tournaments that the user has selected
        self.selected_tournaments = []

        ## string of the user's selected team
        self.selected_team_name = None

        self.current_month = 1
        self.current_year = 2024
        self.current_date = datetime.date(self.current_year, 1, 1)

        self.paused = False
        self.in_simulation = False

        self.notebook_tab_list = []

        self.choose_team(root)

    def choose_team(self, root):
        
        ctk.CTkLabel(root, text="Choose Your Team", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)

        selected_team = ctk.StringVar()
        team_values = [team.teamName for team in self.teams]

        teams_dropdown = ctk.CTkComboBox(root, values=team_values, state="readonly", variable=selected_team)
        teams_dropdown.set(self.teams[0].teamName)
        teams_dropdown.grid(row=1, column=0, padx=10, pady=10)

        confirm_team_button = ctk.CTkButton(root, text="Confirm Team", command=lambda: self.confirm_team(selected_team.get()))
        confirm_team_button.grid(row=1, column=1, padx=10, pady=10)
    
    def confirm_team(self, selected_team):
        
        self.selected_team_name = selected_team

        # team object that the user has selected.
        # it removes the selected team so that it doesn't get automatically added to tournaments
        self.selected_team = self.tournament_director.remove_from_team_list(selected_team)

        ## selects which tournaments the other teams will be going to
        self.tournament_director.decide_which_tournament()

        for widget in self.root.winfo_children():
            widget.destroy()

        self.display_calendar()

    def display_calendar(self):
        
        self.notebook_tab = ctk.CTkTabview(self.root)
        self.notebook_tab.grid(row=0, column=0)

        calendar_tab = self.notebook_tab.add("Calendar")
        self.notebook_tab_list.append("Calendar")

        calendar_frame = ctk.CTkFrame(self.notebook_tab.tab("Calendar"))
        calendar_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ne")

        # Month and Year Frame
        nav_frame = ctk.CTkFrame(calendar_frame)
        nav_frame.grid(row=1, column=0, columnspan=10, pady=10)

        previous_month = ctk.CTkButton(nav_frame, text="Previous", command=self.prev_month)
        previous_month.grid(row=0, column=0, padx=5)

        next_month = ctk.CTkButton(nav_frame, text="Next", command=self.next_month)
        next_month.grid(row=0, column=2, padx=5)

        tournaments_information_frame = ctk.CTkFrame(calendar_frame)
        tournaments_information_frame.grid(row=3, column=2, padx=10, pady=10, sticky="ne")

        tournament_information_label = ctk.CTkLabel(tournaments_information_frame, text="", anchor="nw", justify="left", 
                width=30, height=20, padx=10, pady=10, text_color="red", fg_color="white")
        tournament_information_label.grid(row=0, column=0)

        selected_tournaments_frame = None

        if not self.in_simulation:
            header_label = ctk.CTkLabel(calendar_frame, text="Selecting Tournaments", font=("Arial", 16))
            header_label.grid(row=0, column=0, columnspan=10)

            self.current_month_label = ctk.CTkLabel(nav_frame, text=self.get_month_year_label())
            self.current_month_label.grid(row=0, column=1, padx=10)

            selected_tournaments_frame = ctk.CTkFrame(calendar_frame, fg_color="black")
            selected_tournaments_frame.grid(row=3, column=1, padx=10, pady=10, sticky="ne")

            for index in range(len(self.selected_tournaments)):
                tournament = self.selected_tournaments[index]
                selected_tournament_label = ctk.CTkLabel(selected_tournaments_frame, text=tournament.name, anchor="nw", justify="left", 
                                                        width=30, height=20, padx=10, pady=10, text_color="red")
                selected_tournament_label.grid(row=index, column=0)

            confirm_tournaments_button = ctk.CTkButton(nav_frame, text="Confirm Tournaments", command=self.confirm_tournaments)
            confirm_tournaments_button.grid(row=1, column=0, columnspan=3, pady=10)

        else:
            header_label = ctk.CTkLabel(calendar_frame, text="Season 2024", font=("Arial", 16))
            header_label.grid(row=0, column=0, columnspan=10, padx=10, pady=5)

            self.current_date_label = ctk.CTkLabel(nav_frame, text=f"Current Date: {self.current_date}", font=("Arial", 16))
            self.current_date_label.grid(row=0, column=1, padx=10)

            self.start_simulation_button = ctk.CTkButton(nav_frame, text="Start Simulation", command=self.start_simulation)
            self.start_simulation_button.grid(row=1, column=0, columnspan=3, pady=10)

            self.pause_button = ctk.CTkButton(nav_frame, text="Pause", command=self.toggle_pause)
            self.pause_button.grid(row=2, column=0, columnspan=7, pady=5)

        display_month_instance = DisplayMonth(calendar_frame, selected_tournaments_frame, tournament_information_label, self.current_year, self.current_month, self.tournament_generator, self)

    def prev_month(self):
        if self.current_month == 1:
            self.current_month = 12
        else:
            self.current_month -= 1
        self.update_calendar_display()

    def next_month(self):
        if self.current_month == 12:
            self.current_month = 1
        else:
            self.current_month += 1
        self.update_calendar_display()
    
    def get_month_year_label(self):
        return calendar.month_name[self.current_month] + " " + str(self.current_year)
    
    def update_calendar_display(self):
        # Update the month-year label and refresh the calendar grid
        for widget in self.root.winfo_children():
            widget.destroy()
        self.display_calendar()
    
    def confirm_tournaments(self):
        if not self.selected_tournaments:
            print("No Selection")
        else:

            ## Add user-selected team to the tournaments selected.
            for tournament in self.selected_tournaments:
                tournament.add_team(self.selected_team)

            ## For the tournaments that still have a spot, add the first team on the waitlist
            for tournament in self.tournaments:
                # if not tournament.invite_tournament:
                while len(tournament.teams) < tournament.maxTeams - tournament.number_of_qualified_teams:
                    if len(tournament.waitList) != 0:
                        tournament.add_team(tournament.waitList.pop())
                    else:
                        tournament.add_team(tournament.invited_teams.pop())
            
                # Sort tournament teams by Elo in descending order
                tournament.teams = sorted(tournament.teams, key=lambda x: x.elo, reverse=True)

                tournament.create_base_pools_names_ranks()
        
            ## For some reason, self.teams does not contain the user-selected team
            self.teams.append(self.selected_team)

            self.in_simulation = True
            
            self.update_calendar_display()
    
    def create_team_pool_object_for_tournament(self, tournament):

        tournament.teams = sorted(tournament.teams, key=lambda x: x.elo, reverse=True)

        tournament_pools = []

        for pool, seeding in tournament.pool_format.items():
            team_in_pools = []
            for seed in seeding:
                seed_rank = int(seed.replace("Seed #", ""))
                rank_and_name = tournament.teams[seed_rank - 1]
                team_in_pools.append(rank_and_name)
            tournament_pools.append(team_in_pools)
        
        tournament.tournament_pool_objects = tournament_pools

    def display_tournament_info(self, tournament):
        # Check if the tournament has reached its maximum number of teams
        if len(tournament.teams) != tournament.maxTeams:
            return
        
        self.create_team_pool_object_for_tournament(tournament)
        
        if tournament.name not in self.notebook_tab_list:
            self.create_tournament_tab(tournament)
        else:
            self.notebook_tab.set(tournament.name)
        
        # Display pool information or results
        self.display_pool_play(tournament)

        if tournament.completed:
            # Add bracket tab and display the bracket
            self.display_bracket_tab(tournament)
        
        if not tournament.completed:
            self.add_simulate_button(tournament)
        
    
    def create_tournament_tab(self, tournament):

        self.tournament_tab = self.notebook_tab.add(tournament.name)
        self.notebook_tab_list.append(tournament.name)

        self.tournament_results = ctk.CTkTabview(self.tournament_tab)
        self.tournament_results.grid(row=0, column=0, sticky="nsew")

        self.tournament_results.add("Pool Play")

        self.pool_play_frame = ctk.CTkFrame(self.tournament_results.tab("Pool Play"))
        self.pool_play_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ne")

    
    def display_pool_play(self, tournament):

        pools_frame = ttk.Frame(self.pool_play_frame)
        pools_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        pool_names = list(tournament.pool_format.keys())

        for i, pool_name in enumerate(pool_names):
            header_label = tk.Label(pools_frame, text=pool_name, font=("Arial", 16), width=20, height=2)
            header_label.grid(row=0, column=i * 2, columnspan=2, padx=5, pady=5)

        # Populate teams and records based on tournament status
        if not tournament.completed:
            self.populate_pool_teams(tournament, pool_names, pools_frame)
        else:
            self.populate_completed_pool_results(tournament, pool_names, pools_frame)

        # Create the results frame underneath the standings
        results_frame = ttk.Frame(self.pool_play_frame)
        results_frame.grid(row=1, column=0, columnspan=len(pool_names) * 2, sticky="nsew", padx=10, pady=10)

        # Display game results with headers
        self.display_pool_game_results(results_frame, tournament)

    def display_pool_game_results(self, parent_frame, tournament):
        """Displays game results for each pool with a centered header."""
        pool_names = list(tournament.pool_format.keys())

        # Create headers and pool frames for results
        for i, pool_name in enumerate(pool_names):
            # Create a centered header for each pool
            header_label = tk.Label(
                parent_frame,
                text=f"Results for {pool_name}",
                font=("Arial", 18, "bold"),
                anchor="center"
            )
            header_label.grid(row=0, column=i, padx=10, pady=(10, 5), sticky="nsew")

            # Create a frame to display the game results for this pool
            pool_frame = tk.Frame(parent_frame, borderwidth=1, relief="solid")
            pool_frame.grid(row=1, column=i, padx=5, pady=5, sticky="nsew")

            if tournament.completed:
                # Display completed game results
                pool_results = tournament.pool_score_results.get(pool_name, [])
                for game_index, game in enumerate(pool_results):
                    game_label = tk.Label(pool_frame, text=game, font=("Arial", 12), anchor="w")
                    game_label.grid(row=game_index, column=0, sticky="w", padx=5, pady=2)
            else:
                # Display "0-0" results when the tournament is ongoing
                team_combinations = list(combinations(tournament.tournament_pool_objects[i], 2))
                for game_index, match in enumerate(team_combinations):
                    game_text = f"{match[0].teamName} vs {match[1].teamName} : 0-0"
                    game_label = tk.Label(pool_frame, text=game_text, font=("Arial", 12), anchor="w")
                    game_label.grid(row=game_index, column=0, sticky="w", padx=5, pady=2)

    def populate_pool_teams(self, tournament, pool_names, pools_frame):
        """Populates pool teams for an ongoing tournament."""
        for pool_index, pool_name in enumerate(pool_names):
            for row, team in enumerate(tournament.pool_teams[pool_index], start=1):
                team_label = tk.Label(pools_frame, text=team, font=("Arial", 16), width=20, height=2, borderwidth=1, relief="solid")
                team_label.grid(row=row, column=pool_index * 2)

                record_label = tk.Label(pools_frame, text="0-0", font=("Arial", 16), width=5, height=2, borderwidth=1, relief="solid")
                record_label.grid(row=row, column=(pool_index * 2) + 1)
        

    def populate_completed_pool_results(self, tournament, pool_names, pools_frame):
        """Populates pool results for a completed tournament."""
        initial_ranks = {team.rsplit("(", 1)[0].strip(): team.rsplit("(", 1)[1].strip(")") for pool in tournament.pool_teams for team in pool}

        for pool_index, pool_results in enumerate(tournament.pool_results):
            for row, team_info in enumerate(pool_results, start=1):
                team_name = team_info[0].teamName
                win_loss = f"{team_info[1]['wins']}-{team_info[1]['losses']}"
                initial_rank = initial_ranks.get(team_name, "N/A")
                entry_text = f"{team_name} ({initial_rank})"

                team_label = tk.Label(pools_frame, text=entry_text, font=("Arial", 16), width=20, height=2, borderwidth=1, relief="solid")
                team_label.grid(row=row, column=pool_index * 2)

                record_label = tk.Label(pools_frame, text=win_loss, font=("Arial", 16), width=5, height=2, borderwidth=1, relief="solid")
                record_label.grid(row=row, column=(pool_index * 2) + 1)
    
    def display_bracket_tab(self, tournament):
        
        bracket_tab = self.tournament_results.add(tournament.name + " Bracket")

        bracket_results = ctk.CTkTabview(bracket_tab)
        bracket_results.grid(row=0, column=0)

        self.draw_full_bracket(bracket_results, tournament)


    def draw_full_bracket(self, notebook, tournament):
        teams_advancing = tournament.number_of_qualified_teams
        if tournament.maxTeams in [16, 20] or teams_advancing == 0:
            teams_advancing = 1
        
        match_data = tournament.bracket.round_letters.get((teams_advancing, tournament.maxTeams), {})
        rect_width = 150
        rect_height = 30
        spacing_y = 20  # Space between matches vertically
        round_spacing = 200  # Horizontal spacing between rounds
        match_results = {}

        for key in tournament.bracket.order_of_games_played_bracket[(teams_advancing, tournament.maxTeams)]:
            match_results[key.upper()] = (tournament.bracket.bracket_dict[key].winner.teamName, tournament.bracket.bracket_dict[key].winnerPoints,
                                          tournament.bracket.bracket_dict[key].loser.teamName, tournament.bracket.bracket_dict[key].loserPoints)

        for place, rounds in sorted(match_data.items()):
            # Create a frame for each tab
            if place == -1:
                place = "Crossover"
            place_in_bracket = notebook.add(f"Place {place} Bracket")

            place_frame = ttk.Frame(place_in_bracket)
            place_frame.grid(row=0, column=0)

            
            # Create a canvas inside each frame for drawing
            canvas = tk.Canvas(place_frame, width=1000, height=600)
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
                                # Check if the group_index is within bounds of previous_round_centers
                                if group_index * 2 < len(previous_round_centers):
                                    # Get the centers for the current group from the previous round
                                    prev_centers = previous_round_centers[group_index * 2:group_index * 2 + 2]

                                    if len(prev_centers) == 2:
                                        # If there are two centers, center between them
                                        y_pos = (prev_centers[0][1] + prev_centers[1][1]) // 2
                                    else:
                                        # If there is only one center, use that Y position
                                        y_pos = prev_centers[0][1]
                                else:
                                    # If the group_index is out of bounds, handle appropriately (e.g., default to last center)
                                    y_pos = previous_round_centers[-1][1] + (rect_height + spacing_y)

                        # Draw the winner rectangle
                        canvas.create_rectangle(start_x, y_pos, start_x + rect_width, y_pos + rect_height, fill="blue")
                        canvas.create_text(start_x + 5, y_pos + rect_height // 2, text=f"{winner_name} {winner_score}", anchor="w", fill="white")

                        # Draw the loser rectangle
                        canvas.create_rectangle(start_x, y_pos + rect_height, start_x + rect_width, y_pos + 2 * rect_height, fill="red")
                        canvas.create_text(start_x + 5, y_pos + 1.5 * rect_height, text=f"{loser_name} {loser_score}", anchor="w", fill="white")

                        # Store center positions for next round centering
                        center_x = start_x + rect_width
                        center_y = y_pos + rect_height  # Middle of the lower rectangle
                        current_round_centers.append((center_x, center_y))

                previous_round_centers = current_round_centers
                start_x += round_spacing  # Move to the next round horizontally
    
    def add_simulate_button(self, tournament):
        """Adds a button to simulate the tournament."""
        self.simulate_tournament_button = ctk.CTkButton(self.tournament_tab, text="Simulate Tournament", hover_color="red",
                                                    command=lambda t=tournament: self.simulate_tournament(t))
        self.simulate_tournament_button.grid(row=1, column=0, columnspan=2, pady=(20, 10), sticky="s")
    
    def simulate_tournament(self, tournament):
        self.create_team_pool_object_for_tournament(tournament)
        tournament.run_event()
        self.display_tournament_info(tournament)
        self.simulate_tournament_button.destroy()
    
    def start_simulation(self):
        self.start_simulation_button.destroy()
        self.run_simulation()

    def toggle_pause(self):
        # Toggle the paused state and update the button text
        self.paused = not self.paused
        self.pause_button.configure(text="Resume" if self.paused else "Pause")
        if not self.paused:
            self.run_simulation()  # Resume simulation

    def run_simulation(self):
        if self.paused:
            return

        self.current_date_label.configure(text=f"Current Date: {self.current_date}")

        for tournament in self.tournaments:
            if tournament.start_date == self.current_date:
                if not tournament.completed:
                    self.create_team_pool_object_for_tournament(tournament)
                    ## Only display selected tournament tabs
                    if tournament in self.selected_tournaments:
                        self.display_tournament_info(tournament)
                        self.notebook_tab.set(tournament.name)
                        self.toggle_pause()
                    else:
                        tournament.run_event()
        
        
        # Store the current month before updating the date
        current_month = self.current_date.month
        self.current_date += datetime.timedelta(days=1)

        # Check if the month has changed
        if self.current_date.month != current_month:
            # Call the method to update the calendar view
            self.next_month()
        
        # Schedule the next update if not paused
        if self.current_date < datetime.date(2024, 12, 31):  # Adjust end date as needed
            self.root.after(1000, self.run_simulation) 

# Run the app
teamGenerator = TeamGenerator()
tournamentGenerator = TournamentGenerator("2024", 100, 20, 10)
tournamentDirector = TournamentDirector(teamGenerator, tournamentGenerator)
root = ctk.CTk()
app = TournamentApp(root, teamGenerator, tournamentGenerator, tournamentDirector)
root.mainloop()