from team import *
from tournament import *
from handle_tournament import *

import tkinter as tk
from tkinter import ttk, messagebox
import calendar
import math
from tkmacosx import Button

class TournamentApp:
    def __init__(self, root, teamGenerator, tournamentGenerator, tournamentDirector):
        self.root = root
        self.root.title("Ultimate Frisbee Tournament Simulation")

        ## self.teams is Team Objects -> list of all the teams
        ## self.tournamnets is Tournament Objects -> list of all the tournaments
        self.teams = teamGenerator.teamList
        self.tournaments = tournamentGenerator.tournaments

        ## handles which team is going/eligible/invited to which tournament
        self.tournamentDirector = tournamentDirector
        
        ## On the GUI, contains the tournaments that user has selected.
        self.selected_tournaments = []

        ## The player's selected team in a string variable
        self.selected_team_name = None

        self.current_month = 1  # Start with January
        self.current_year = 2024  # Start with the year 2024

        ttk.Label(root, text="Choose Your Team", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)

        self.team_var = tk.StringVar()
        teams_dropdown = ttk.Combobox(root, state="readonly", textvariable=self.team_var)
        teams_dropdown['values'] = [team.teamName for team in self.teams]
        teams_dropdown.current(1)
        teams_dropdown.grid(row=1, column=0, padx=10, pady=10)

        self.confirm_team_button = tk.Button(root, text="Confirm Team", command=self.confirm_team)
        self.confirm_team_button.grid(row=1, column=1, padx=10, pady=10)

        self.select_team_information_label_array = {}

        self.current_date_in_simulation = datetime.date(self.current_year, 1, 1)

        self.paused = False
    
    def confirm_team(self):
        selected_team_name = self.team_var.get()
        if selected_team_name:  # Ensure a team has been selected
            self.selected_team_name = selected_team_name

            ## Remove selected team from the director so that it doesn't add the user-selected team automatically to the tournaments
            self.selected_team = tournamentDirector.remove_from_team_list(self.selected_team_name)
            
            ## Here it selects which tournaments the other teams will be going to
            tournamentDirector.decide_which_tournament()

            self.root.withdraw()
            # messagebox.showinfo("Team Selected", f"You have selected: {self.selected_team_name}")
            self.display_calendar()
        else:
            messagebox.showwarning("Selection Error", "Please select a team.")

    ## Creates a calendar window, a box to display selected tournaments, and information-box for tournament information
    def display_calendar(self):

        self.calendar_window = tk.Toplevel(self.root)
        self.calendar_window.title("Select Tournaments")

        self.notebook = ttk.Notebook(self.calendar_window)
        self.notebook.grid(row=0, column=0, sticky="nsew")

        self.calendar_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.calendar_tab, text="Select Tournaments")

        # Month and Year Navigation at the top of calendar_tab
        nav_frame = tk.Frame(self.calendar_tab)
        nav_frame.grid(row=0, column=0, columnspan=7, pady=10)

        # Previous Button for Previous Month
        self.prev_button = tk.Button(nav_frame, text="Previous", command=self.prev_month)
        self.prev_button.grid(row=0, column=0, padx=5)

        # Current Month Label
        self.current_month_label = tk.Label(nav_frame, text=self.get_month_year_label())
        self.current_month_label.grid(row=0, column=1, padx=10)

        # Next button for next month
        self.next_button = tk.Button(nav_frame, text="Next", command=self.next_month)
        self.next_button.grid(row=0, column=2, padx=5)

        # Calendar grid frame directly below the navigation
        self.calendar_frame = tk.Frame(self.calendar_tab)
        self.calendar_frame.grid(row=1, column=0, columnspan=7, pady=10)

        # Initialize the calendar display in calendar_frame
        self.create_calendar()

        # Variables For Information Box for Selected Tournaments
        self.selected_tournaments_listbox = tk.Listbox(self.calendar_tab, width=30, height=10)
        self.selected_tournaments_listbox.grid(row=2, column=0, columnspan=4, padx=10, pady=10)

        self.select_tournament_information = tk.Label(
            self.calendar_tab, text="", anchor="nw", justify="left", 
            background="white", relief="solid", width=30, height=20, padx=10, pady=10, fg="red"
        )
        self.select_tournament_information.grid(row=2, column=4, columnspan=3, padx=10, pady=10)

        # Event binding to remove a selected tournament
        self.selected_tournaments_listbox.bind("<<ListboxSelect>>", self.remove_selected_tournament)

        # Confirm Tournaments Button below the listbox and label
        self.confirm_tournaments_button = tk.Button(self.calendar_tab, text="Confirm Tournaments", command=self.confirm_tournaments)
        self.confirm_tournaments_button.grid(row=3, column=0, columnspan=7, pady=5)
    
    def prev_month(self):
        if self.current_month == 1:
            self.current_month = 12
        else:
            self.current_month -= 1
        self.update_calendar_display()

    def next_month(self):
        if self.current_month == 12:
            self.current_month = 1
            # self.current_year += 1
        else:
            self.current_month += 1
        self.update_calendar_display()
    
    def update_calendar_display(self):
        # Update the month-year label and refresh the calendar grid
        self.current_month_label.config(text=self.get_month_year_label())

        ## If I am on a certain tab, create new calendar for the selected tournaments
        if (self.notebook.tab(self.notebook.select(), 'text') == "Season 2024"):
            self.create_true_calendar()
        else:
            self.create_calendar()

    def get_month_year_label(self):
        return calendar.month_name[self.current_month] + " " + str(self.current_year)

    def create_calendar(self):
        # Clear all widgets in the calendar frame to start fresh
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        cal = calendar.monthcalendar(self.current_year, self.current_month)

        # Create a dictionary to list all tournaments by date
        tournament_dict = {}
        for t in self.tournaments:
            if t.start_date.month == self.current_month and t.start_date.year == self.current_year:
                day = t.start_date.day
                if day not in tournament_dict:
                    tournament_dict[day] = []
                tournament_dict[day].append(t)

        # Render the calendar with each tournament on a separate button
        for week in cal:
            for day in week:
                if day == 0:
                    day_label = tk.Label(self.calendar_frame, text="  ", width=10, height=3, relief="ridge")
                    day_label.grid(column=week.index(day), row=cal.index(week))
                else:
                    # Frame for the day's tournaments
                    day_frame = tk.Frame(self.calendar_frame, width=12, height=4, relief="ridge", borderwidth=1)
                    day_frame.grid(column=week.index(day), row=cal.index(week), sticky="nsew")
                    
                    # Display each tournament as a separate button
                    if day in tournament_dict:
                        for tournament in tournament_dict[day]:
                            tournament_button = Button(day_frame, text=tournament.name,
                                                        command=lambda t=tournament: self.select_tournament(t))
                            self.highlight_button(tournament_button, tournament)
                            tournament_button.pack(fill="x", padx=1, pady=1)

                            tournament_button.bind("<Enter>", lambda event, t=tournament: self.show_tournament_info(t))
                            tournament_button.bind("<Leave>", lambda event: self.clear_info_display())
                    else:
                        # Show day number if there are no tournaments
                        day_label = tk.Label(day_frame, text=str(day), width=10, height=3)
                        day_label.pack(fill="both")
    
    ## Highlight the button if the user-selected team is elgible for torunament
    def highlight_button(self, button, tournament):
        allowed_to_participate = False
        if tournament.normal_tournament:
            if tournament.min_elo < self.selected_team.elo < tournament.max_elo:
                allowed_to_participate = True
        elif tournament.open_tournament:
            if tournament.min_elo < self.selected_team.elo < tournament.max_elo:
                allowed_to_participate = True
        elif tournament.invite_tournament:
            if tournament.min_elo < self.selected_team.elo < tournament.max_elo:
                allowed_to_participate = True
        elif tournament.national_tournament:
            allowed_to_participate = self.tournamentDirector.eligible_for_tournament(self.selected_team, tournament)

        if allowed_to_participate:
            button.config(bg="SkyBlue1")
            button.update_idletasks() 
    
    ## function to display the tournamnt information like the number of teams going etc.
    def show_tournament_info(self, tournament):

        if not tournament.completed:
            num_teams = len(tournament.teams)
            midpoint = math.ceil(num_teams / 2)

            left_column = [f"{i + 1}. {tournament.teams[i].teamName}" for i in range(midpoint)]
            right_column = [f"{i + 1}. {tournament.teams[i].teamName}" for i in range(midpoint, num_teams)]

            # Pad columns to be the same length, if necessary
            if len(left_column) > len(right_column):
                right_column.append("")

            # Combine both columns into a single text string
            team_info = "\n".join(f"{left:<20} {right}" for left, right in zip(left_column, right_column))

            # Display tournament details in the info display area
            info_text = (
                f"Name: {tournament.name}\n"
                f"Date: {tournament.start_date.strftime('%Y-%m-%d')}\n"
                f"Number of Total Teams: {tournament.maxTeams}\n"
                f"Number of Invited Teams: {(tournament.maxTeams - tournament.number_of_qualified_teams)}\n" 
                f"Number of Qualified Teams: {tournament.number_of_qualified_teams}\n"
                f"Minimum Elo: {tournament.min_elo}\n"
                f"Maximum Elo: {tournament.max_elo}\n"
                f"Teams:\n{team_info}" 
            )
            self.select_tournament_information.config(text=info_text)
        else:
            num_teams = len(tournament.teams)
            midpoint = math.ceil(num_teams / 2)

            left_column = [f"{i + 1}. {tournament.winners[i].teamName}" for i in range(midpoint)]
            right_column = [f"{i + 1}. {tournament.winners[i].teamName}" for i in range(midpoint, num_teams)]

            # Pad columns to be the same length, if necessary
            if len(left_column) > len(right_column):
                right_column.append("")

            # Combine both columns into a single text string
            team_info = "\n".join(f"{left:<20} {right}" for left, right in zip(left_column, right_column))

            # Display tournament details in the info display area
            info_text = (
                f"Name: {tournament.name}\n"
                f"Date: {tournament.start_date.strftime('%Y-%m-%d')}\n"
                f"Number of Total Teams: {tournament.maxTeams}\n"
                f"Number of Invited Teams: {(tournament.maxTeams - tournament.number_of_qualified_teams)}\n" 
                f"Number of Qualified Teams: {tournament.number_of_qualified_teams}\n"
                f"Minimum Elo: {tournament.min_elo}\n"
                f"Maximum Elo: {tournament.max_elo}\n"
                f"Rankings:\n{team_info}" 
            )
            self.select_tournament_information.config(text=info_text)

    ## clear the label box
    def clear_info_display(self):
        # Clear the info display area
        self.select_tournament_information.config(text="")

    ## function to determine how to choose the tournament
    def select_tournament(self, tournament):
        allowed_to_participate = False
        if tournament.normal_tournament:
            if tournament.min_elo < self.selected_team.elo < tournament.max_elo:
                allowed_to_participate = True
        elif tournament.open_tournament:
            if tournament.min_elo < self.selected_team.elo < tournament.max_elo:
                allowed_to_participate = True
        elif tournament.invite_tournament:
            if tournament.min_elo < self.selected_team.elo < tournament.max_elo:
                allowed_to_participate = True
        elif tournament.national_tournament:
            allowed_to_participate = self.tournamentDirector.eligible_for_tournament(self.selected_team, tournament)

        if allowed_to_participate:
            date = tournament.start_date

            # Check if another tournament on the same day is already selected
            for t in self.selected_tournaments:
                if t != tournament:
                    if t.start_date == date:
                        # Remove the other tournament from selection
                        self.selected_tournaments.remove(t)
                        # Find and remove from Listbox
                        idx = self.selected_tournaments_listbox.get(0, tk.END).index(t.name)
                        self.selected_tournaments_listbox.delete(idx)
                        break

            # Toggle selection of the clicked tournament
            if tournament.name in [t.name for t in self.selected_tournaments]:
                # Remove tournament if it's already selected
                self.selected_tournaments.remove(tournament)
                idx = self.selected_tournaments_listbox.get(0, tk.END).index(tournament.name)
                self.selected_tournaments_listbox.delete(idx)
            else:
                # Add tournament if it’s not selected
                self.selected_tournaments.append(tournament)
                self.selected_tournaments_listbox.insert(tk.END, tournament.name)

    def remove_selected_tournament(self, event):
        # Remove selected tournament from the display listbox and selected list
        selected_idx = self.selected_tournaments_listbox.curselection()
        if selected_idx:
            selected_name = self.selected_tournaments_listbox.get(selected_idx)
            self.selected_tournaments.remove(selected_name)
            self.selected_tournaments_listbox.delete(selected_idx)
    
    ## For removal when clicking on the listbox itself?
    def update_selected_tournaments(self):
        if self.selected_tournaments:
            selected_names = list(self.selected_tournaments.values())
            self.selected_tournaments_label.config(text="Selected Tournaments: " + ", ".join(selected_names))
        else:
            self.selected_tournaments_label.config(text="Selected Tournaments: None")

    def confirm_tournaments(self):
        if False:
        # if not self.selected_tournaments:
            messagebox.showwarning("No Selection", "You must select at least one tournament.")
        else:
            # tournament_list = ', '.join(self.selected_tournaments.names)
            # messagebox.showinfo("Tournaments Confirmed", f"Team: {self.selected_team_name}\nTournaments: {tournament_list}")

            ## Add user-selected team to the tournaments selected.
            for tournament in self.selected_tournaments:
                tournament.add_team(self.selected_team)
            
            ## For the tournaments that still have a spot, add the first team on the waitlist
            for tournament in self.tournaments:
                # if not tournament.invite_tournament:
                if len(tournament.teams) < tournament.maxTeams:
                    tournament.add_team(tournament.waitList.pop())
            
                # Sort tournament teams by Elo in descending order
                tournament.teams = sorted(tournament.teams, key=lambda x: x.elo, reverse=True)

                tournament.create_base_pools_names_ranks()

        
            ## For some reason, self.teams does not contain the user-selected team
            self.teams.append(self.selected_team)
            
            self.notebook.forget(0)

            self.display_true_calendar()

    ## Create the new calendar, with that makes the user-selected tournaments salmon-colored.
    def display_true_calendar(self):

        self.current_month = 1  # Start with January
        self.current_year = 2024  # Start with the year 2024

        self.calendar_window.title("Simulation")

        self.calendar_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.calendar_tab, text="Season 2024")

        # Month and Year Navigation at the top of calendar_tab
        nav_frame = tk.Frame(self.calendar_tab)
        nav_frame.grid(row=0, column=0, columnspan=7, pady=10)

        # Previous button
        self.prev_button = tk.Button(nav_frame, text="Previous", command=self.prev_month)
        self.prev_button.grid(row=0, column=0, padx=5)

        # Current Month Label
        self.current_month_label = tk.Label(nav_frame, text=self.get_month_year_label())
        self.current_month_label.grid(row=0, column=1, padx=10)

        self.current_date_label = tk.Label(nav_frame, text=f"Current Date: {self.current_date_in_simulation}", font=("Arial", 16))
        self.current_date_label.grid(row=1, column=1, padx=10)

        # Next button
        self.next_button = tk.Button(nav_frame, text="Next", command=self.next_month)
        self.next_button.grid(row=0, column=2, padx=5)

        # Calendar grid frame directly below the navigation
        self.calendar_frame = tk.Frame(self.calendar_tab)
        self.calendar_frame.grid(row=1, column=0, columnspan=7, pady=10)

        # Initialize the calendar display in calendar_frame
        self.create_true_calendar()

        self.select_tournament_information = tk.Label(
            self.calendar_tab, text="", anchor="nw", justify="left", 
            background="white", relief="solid", width=30, height=20, padx=10, pady=10, fg="red"
        )
        self.select_tournament_information.grid(row=2, column=4, columnspan=3, padx=10, pady=10)

        self.start_simulation_button = tk.Button(self.calendar_tab, text="Start Simulation", command=self.start_simulation)
        self.start_simulation_button.grid(row=3, column=0, columnspan=7, pady=5)

        self.pause_button = tk.Button(self.calendar_tab, text="Pause", command=self.toggle_pause)
        self.pause_button.grid(row=4, column=0, columnspan=7, pady=5)
    
    def create_true_calendar(self):
        # Clear all widgets in the calendar frame to start fresh
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        cal = calendar.monthcalendar(self.current_year, self.current_month)

        # Create a dictionary to list all tournaments by date
        tournament_dict = {}
        for t in self.tournaments:
            if t.start_date.month == self.current_month and t.start_date.year == self.current_year:
                day = t.start_date.day
                if day not in tournament_dict:
                    tournament_dict[day] = []
                tournament_dict[day].append(t)

        # Render the calendar with each tournament on a separate button
        for week in cal:
            for day in week:
                if day == 0:
                    day_label = tk.Label(self.calendar_frame, text="  ", width=10, height=3, relief="ridge")
                    day_label.grid(column=week.index(day), row=cal.index(week))
                else:
                    # Frame for the day's tournaments
                    day_frame = tk.Frame(self.calendar_frame, width=12, height=4, relief="ridge", borderwidth=1)
                    day_frame.grid(column=week.index(day), row=cal.index(week), sticky="nsew")
                    
                    # Display each tournament as a separate button
                    if day in tournament_dict:
                        for tournament in tournament_dict[day]:
                            tournament_button = Button(day_frame, text=tournament.name,
                                                        command=lambda t=tournament: self.display_tournament_info(t))
                            self.highlight_button(tournament_button, tournament)
                            self.highlight_tournament(tournament_button, tournament)
                            tournament_button.pack(fill="x", padx=1, pady=1)

                            tournament_button.bind("<Enter>", lambda event, t=tournament: self.show_tournament_info(t))
                            tournament_button.bind("<Leave>", lambda event: self.clear_info_display())
                    else:
                        # Show day number if there are no tournaments
                        day_label = tk.Label(day_frame, text=str(day), width=10, height=3)
                        day_label.pack(fill="both")
    

    def highlight_tournament(self, button, tournament):
        if tournament in self.selected_tournaments:
            button.config(bg="salmon")
            button.update_idletasks() 
    
    def display_tournament_info(self, tournament):
        if len(tournament.teams) == tournament.maxTeams:
            # Avoid adding the same tab twice
            if tournament.name not in [self.notebook.tab(i, 'text') for i in self.notebook.tabs()]:
                self.tournament_tab = ttk.Frame(self.notebook)
                self.notebook.add(self.tournament_tab, text=tournament.name)

                # Create a sub-notebook for Pool-Play and Bracket tabs
                self.sub_notebook = ttk.Notebook(self.tournament_tab)
                self.sub_notebook.grid(row=0, column=0, sticky="nsew")

                # Create Pool-Play tab
                pool_play_frame = ttk.Frame(self.sub_notebook)
                self.sub_notebook.add(pool_play_frame, text='Pool-Play')

                # Add pool information into the Pool-Play tab
                pool_format = tournament.pool_format
                pool_names = list(pool_format.keys())
                self.pools_frame = ttk.Frame(pool_play_frame)
                self.pools_frame.pack(expand=True, fill='both', padx=10, pady=10)

                # Display pool headers above their respective columns
                for i, header in enumerate(pool_names):
                    entry = tk.Label(self.pools_frame, text=header, font=("Arial", 16), width=20, height=2)
                    entry.grid(row=0, column=i * 2, columnspan=2, padx=5, pady=5)
            else:
                if self.notebook.tab(self.notebook.select(), "text") != tournament.name:
                    for tab_id in self.notebook.tabs():
                        if self.notebook.tab(tab_id, option="text") == tournament.name:
                            self.notebook.select(tab_id)
                            self.toggle_pause()
                            return

            if not tournament.completed:
                for pool_index, pool_name in enumerate(pool_names):
                    row = 1
                    for team in tournament.pool_teams[pool_index]:
                        entry = tk.Label(self.pools_frame, text=team, font=("Arial", 16), width=20, height=2, padx=5, pady=5, borderwidth=1, relief="solid")
                        entry.grid(row=row, column=pool_index * 2)
                        entry.bind("<Enter>", lambda event, t=team: self.show_team_info(t, tournament))
                        entry.bind("<Leave>", lambda event: self.clear_team_display())
                        
                        record_label = tk.Label(self.pools_frame, text="0-0", font=("Arial", 16), width=5, height=2, padx=5, pady=5, borderwidth=1, relief="solid")
                        record_label.grid(row=row, column=(pool_index * 2) + 1)
                        row += 1
            else:
                initial_ranks = {}
                for pool_teams in tournament.pool_teams:
                    for team in pool_teams:
                        team_name, initial_rank = team.rsplit("(", 1)
                        initial_ranks[team_name.strip()] = initial_rank.strip(")")

                for pool_index, pool_results in enumerate(tournament.pool_results):
                    row = 1
                    for team_info in pool_results:
                        team_name = team_info[0].teamName
                        win_loss = f"{team_info[1]['wins']}-{team_info[1]['losses']}"
                        initial_rank = initial_ranks.get(team_name, "N/A")
                        entry_text = f"{team_name} ({initial_rank})"

                        entry = tk.Label(self.pools_frame, text=entry_text, font=("Arial", 16), width=20, height=2, padx=5, pady=5, borderwidth=1, relief="solid")
                        entry.grid(row=row, column=pool_index * 2)
                        entry.bind("<Enter>", lambda event, t=team_info[0].teamName: self.show_team_info(t, tournament))
                        entry.bind("<Leave>", lambda event: self.clear_team_display())
                        
                        record_label = tk.Label(self.pools_frame, text=win_loss, font=("Arial", 16), width=5, height=2, padx=5, pady=5, borderwidth=1, relief="solid")
                        record_label.grid(row=row, column=(pool_index * 2) + 1)
                        row += 1

            if tournament.completed:
                # Create Bracket tab
                bracket_frame = ttk.Frame(self.sub_notebook)
                self.sub_notebook.add(bracket_frame, text='Bracket')

                # Create a nested notebook inside the bracket_frame
                bracket_notebook = ttk.Notebook(bracket_frame)
                bracket_notebook.pack(expand=True, fill='both')  # Pack the nested notebook

                # Draw the full bracket into the nested notebook
                self.draw_full_bracket(bracket_notebook, tournament)

            # Frame to hold the team information on the right side
            info_frame = ttk.Frame(self.tournament_tab)
            info_frame.grid(row=0, column=1, sticky="ne", padx=10, pady=10)

            self.select_team_information = tk.Label(
                info_frame, text="", anchor="nw", justify="left",
                background="white", relief="solid", width=30, height=20, padx=10, pady=10, fg="red"
            )
            self.select_team_information.grid(row=0, column=0)
            
            if tournament not in self.select_team_information_label_array:
                self.select_team_information_label_array[tournament.name] = self.select_team_information

            if not tournament.completed:
                self.simulate_tournament_button = Button(self.tournament_tab, text="Simulate Tournament",command=lambda t=tournament: self.simulate_tournament(t))
                # self.simulate_tournament_button = tk.Button(self.tournament_tab, text="Simulate Tournament", command=self.simulate_tournament)
                self.simulate_tournament_button.grid(row=1, column=0, columnspan=2, pady=(20, 10), sticky="s")
            
            pool_result_frame = ttk.Frame(self.tournament_tab)
            pool_result_frame.grid(row=1, column=0, sticky="ne", padx=10, pady=10)
                
            for index, pool in enumerate(tournament.pool_format.keys()):
                # Create and place the pool header
                header_label = tk.Label(root, text=pool, font=("Arial", 14, "bold"), anchor="center")
                header_label.grid(row=0, column=index, padx=10, pady=5, sticky="nsew")
                
                # Create a frame for each pool's results
                pool_frame = tk.Frame(root, borderwidth=1, relief="solid")
                pool_frame.grid(row=1, column=index, padx=10, pady=5, sticky="nsew")
                
                if tournament.completed:
                    # Add game result labels to each pool frame
                    for game in tournament.pool_score_results.get(pool, []):
                        game_label = tk.Label(pool_frame, text=game, anchor="w")
                        game_label.pack(anchor="w", padx=5, pady=2)
                else:
                    for pool in tournament.tournament_pool_objects:
                        team_combinations = list(combinations(pool, 2))
                        for match in team_combinations:
                            game_text = match[0].name + " | " + match[1].name + " : " + "0 - 0"
                            game_label = tk.Label(pool_frame, text=game_text, anchor="w")
                            game_label.pack(anchor="w", padx=5, pady=2)

    def draw_full_bracket(self, notebook, tournament):
        teams_advancing = tournament.number_of_qualified_teams
        if tournament.maxTeams in [16, 20]:
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
            place_frame = ttk.Frame(notebook)
            if place == -1:
                place = "Crossover"
            notebook.add(place_frame, text=f"Place {place} Bracket")
            
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

    def show_team_info(self, teamName, tournament):

        team_info = None
        for element in self.teams:
            if element.teamName in teamName:
                team_info = element
                break
        
        info_text = (
           f"Name: {team_info.teamName}\n"
           f"Elo: {team_info.elo}\n"
           f"Win: {team_info.wins}\n" 
           f"Loss: {team_info.loss}\n" 
        )

        self.select_team_information = self.select_team_information_label_array[tournament.name]
        self.select_team_information.config(text=info_text)
    
    ## clear the label box
    def clear_team_display(self):
        # Clear the info display area
        self.select_team_information.config(text="")
    
    def start_simulation(self):
        self.start_simulation_button.destroy()
        self.run_simulation()
    
    def run_simulation(self):
        if self.paused:
            return  # Stop if paused
        
        self.current_date_label.config(text=f"Current Date: {self.current_date_in_simulation}")

        # Check if there's a tournament on this date
        for tournament in self.tournaments:
            if tournament.start_date == self.current_date_in_simulation:
                if not tournament.completed:
                    self.create_team_pool_object_for_tournament(tournament)
                    ## Only display selected tournament tabs
                    if tournament in self.selected_tournaments:
                        self.show_tournament_tab(tournament)
                    else:
                        tournament.run_event()
        
        
        # Store the current month before updating the date
        current_month = self.current_date_in_simulation.month
        self.current_date_in_simulation += datetime.timedelta(days=1)

        # Check if the month has changed
        if self.current_date_in_simulation.month != current_month:
            # Call the method to update the calendar view
            self.next_month()
        
        # Schedule the next update if not paused
        if self.current_date_in_simulation < datetime.date(2024, 12, 31):  # Adjust end date as needed
            self.root.after(1000, self.run_simulation) 
    
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

    def toggle_pause(self):
        # Toggle the paused state and update the button text
        self.paused = not self.paused
        self.pause_button.config(text="Resume" if self.paused else "Pause")
        if not self.paused:
            self.run_simulation()  # Resume simulation
    
    def show_tournament_tab(self, tournament):
        # Create or bring the tournament tab to view
        tab_names = [self.notebook.tab(i, option="text") for i in self.notebook.tabs()]
        if tournament.name not in tab_names:
           self.display_tournament_info(tournament)
        
        for tab_id in self.notebook.tabs():
            if self.notebook.tab(tab_id, option="text") == tournament.name:
                self.notebook.select(tab_id)
                self.toggle_pause()
                break
    
    def simulate_tournament(self, tournament):
        self.create_team_pool_object_for_tournament(tournament)
        tournament.run_event()
        self.display_tournament_info(tournament)
    
    ## TO DO: labels for pool-play results in tournament tab, 
    # make sure that the teams if they win the invite tournament, that they aren't going to another event on the same day.
    # test game.py for possible quickness, to allow. also test how fast it runs 30 games on average.

# Run the app
teamGenerator = TeamGenerator()
tournamentGenerator = TournamentGenerator("2024", 100, 1, 10)
tournamentDirector = TournamentDirector(teamGenerator, tournamentGenerator)
root = tk.Tk()
app = TournamentApp(root, teamGenerator, tournamentGenerator, tournamentDirector)
root.mainloop()
