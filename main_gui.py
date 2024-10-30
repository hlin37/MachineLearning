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

        self.teams = teamGenerator.teamList
        self.tournaments = tournamentGenerator.tournaments

        self.tournamentDirector = tournamentDirector

        self.selected_tournaments = []

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

    def confirm_team(self):
        selected_team_name = self.team_var.get()
        if selected_team_name:  # Ensure a team has been selected
            self.selected_team_name = selected_team_name
            self.selected_team = tournamentDirector.remove_from_team_list(self.selected_team_name)
            
            ## Here it selects which tournaments each team will be going to
            tournamentDirector.decide_which_tournament()

            messagebox.showinfo("Team Selected", f"You have selected: {self.selected_team_name}")
            self.display_calendar()
        else:
            messagebox.showwarning("Selection Error", "Please select a team.")

    def display_calendar(self):
        self.calendar_window = tk.Toplevel(self.root)
        self.calendar_window.title("Select Tournaments")

        # Month and Year Navigation
        nav_frame = tk.Frame(self.calendar_window)
        nav_frame.grid(row=0, column=0, columnspan=7, pady=10)  # Add padding for spacing

        # Previous button
        self.prev_button = tk.Button(nav_frame, text="Previous", command=self.prev_month)
        self.prev_button.grid(row=0, column=0, padx=5)

        # Current Month Label
        self.current_month_label = tk.Label(nav_frame, text=self.get_month_year_label())
        self.current_month_label.grid(row=0, column=1, padx=10)

        # Next button
        self.next_button = tk.Button(nav_frame, text="Next", command=self.next_month)
        self.next_button.grid(row=0, column=2, padx=5)

        self.selected_tournaments_listbox = tk.Listbox(self.calendar_window, width=30, height=10)
        self.selected_tournaments_listbox.grid(row=1, column=8, rowspan=6, padx=10, pady=10)

        self.select_tournament_information = tk.Label(self.calendar_window, text="", anchor="nw", justify="left", 
                                     background="white", relief="solid", width=30, height=20, padx=10, pady=10, fg="red")
        self.select_tournament_information.grid(row=1, column=9, rowspan=6, padx=10, pady=10)

        self.selected_tournaments_listbox.bind("<<ListboxSelect>>", self.remove_selected_tournament)

        # Confirm Tournaments Button
        self.confirm_tournaments_button = tk.Button(self.calendar_window, text="Confirm Tournaments", command=self.confirm_tournaments)
        self.confirm_tournaments_button.grid(column=8, row=7, pady=5)

        # Create the calendar grid frame below the navigation
        self.calendar_frame = tk.Frame(self.calendar_window)
        self.calendar_frame.grid(row=1, column=0, columnspan=7, pady=10)

        # Initialize the calendar display
        self.create_calendar()

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
    
    def show_tournament_info(self, tournament):

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

    def clear_info_display(self):
        # Clear the info display area
        self.select_tournament_information.config(text="")


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
            day = tournament.start_date.day

            # Check if another tournament on the same day is already selected
            for t in self.selected_tournaments:
                if t != tournament:
                    if t.start_date.day == day:
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
    
    def update_selected_tournaments(self):
        if self.selected_tournaments:
            selected_names = list(self.selected_tournaments.values())
            self.selected_tournaments_label.config(text="Selected Tournaments: " + ", ".join(selected_names))
        else:
            self.selected_tournaments_label.config(text="Selected Tournaments: None")

    def confirm_tournaments(self):
        if not self.selected_tournaments:
            messagebox.showwarning("No Selection", "You must select at least one tournament.")
        else:
            # tournament_list = ', '.join(self.selected_tournaments.names)
            # messagebox.showinfo("Tournaments Confirmed", f"Team: {self.selected_team_name}\nTournaments: {tournament_list}")

            for tournament in self.selected_tournaments:
                tournament.add_team(self.selected_team)
            
            for tournament in self.tournaments:
                if not tournament.invite_tournament:
                    if len(tournament.teams) < tournament.maxTeams:
                        tournament.add_team(tournament.waitList.pop())
        
        self.display_true_calendar()

    def display_true_calendar(self):
        self.calendar_window = tk.Toplevel(self.root)
        self.calendar_window.title("Season 2024")

        # Month and Year Navigation
        nav_frame = tk.Frame(self.calendar_window)
        nav_frame.grid(row=0, column=0, columnspan=7, pady=10)  # Add padding for spacing

        # Previous button
        self.prev_button = tk.Button(nav_frame, text="Previous", command=self.prev_month)
        self.prev_button.grid(row=0, column=0, padx=5)

        # Current Month Label
        self.current_month_label = tk.Label(nav_frame, text=self.get_month_year_label())
        self.current_month_label.grid(row=0, column=1, padx=10)

        # Next button
        self.next_button = tk.Button(nav_frame, text="Next", command=self.next_month)
        self.next_button.grid(row=0, column=2, padx=5)

        self.select_tournament_information = tk.Label(self.calendar_window, text="", anchor="nw", justify="left", 
                                     background="white", relief="solid", width=30, height=20, padx=10, pady=10, fg="red")
        self.select_tournament_information.grid(row=1, column=9, rowspan=6, padx=10, pady=10)


        # Create the calendar grid frame below the navigation
        self.calendar_frame = tk.Frame(self.calendar_window)
        self.calendar_frame.grid(row=1, column=0, columnspan=7, pady=10)

        # Initialize the calendar display
        self.create_true_calendar()

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
                            tournament_button.pack(fill="x", padx=1, pady=1)

                            tournament_button.bind("<Enter>", lambda event, t=tournament: self.show_tournament_info(t))
                            tournament_button.bind("<Leave>", lambda event: self.clear_info_display())
                    else:
                        # Show day number if there are no tournaments
                        day_label = tk.Label(day_frame, text=str(day), width=10, height=3)
                        day_label.pack(fill="both")
    
    def display_tournament_info(self, tournament):
        self.tournament_window = tk.Toplevel(self.root)
        tournament_text = tournament.name
        self.tournament_window.title(tournament_text)

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
        self.create_calendar()


    def get_month_year_label(self):
        return calendar.month_name[self.current_month] + " " + str(self.current_year)

# Run the app
teamGenerator = TeamGenerator()
tournamentGenerator = TournamentGenerator("2024", 100, 20, 10)
tournamentDirector = TournamentDirector(teamGenerator, tournamentGenerator)
root = tk.Tk()
app = TournamentApp(root, teamGenerator, tournamentGenerator, tournamentDirector)
root.mainloop()
