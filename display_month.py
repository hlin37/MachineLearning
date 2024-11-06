import calendar
import customtkinter as ctk  # Assuming you're using customtkinter
import datetime
import math

class DisplayMonth:
    def __init__(self, calender_frame, selected_tournaments_frame, tournament_information_label, year, month, tournament_generator, main_interface):
        self.calender_frame = calender_frame
        self.selected_tournaments_frame = selected_tournaments_frame
        self.tournament_information_label = tournament_information_label
        self.main_interface = main_interface
        self.year = year
        self.month = month
        self.tournament_generator = tournament_generator

        # Create the month frame within the parent frame
        self.month_frame = ctk.CTkFrame(self.calender_frame)
        self.month_frame.grid(row=2, column=0, columnspan=7, pady=10)
        # Display the month
        self.display_month()

    def display_month(self):

        cal = calendar.monthcalendar(self.year, self.month)

        for week_index, week in enumerate(cal):
            for day_index, day in enumerate(week):
                if day != 0:
                    day_frame = ctk.CTkFrame(self.month_frame, width=60, height=60, border_width=1, border_color="white", fg_color="black")
                    day_frame.grid(row=week_index, column=day_index, sticky="nsew", padx=5, pady=5)

                    # # Configure the grid to expand properly
                    # self.month_frame.grid_columnconfigure(day_index, weight=1)  # Allow columns to expand
                    # self.month_frame.grid_rowconfigure(week_index + 1, weight=1)  # Allow rows to expand

                    # Display each tournament as a separate button
                    date = datetime.date(self.year, self.month, day)
                    if date in self.tournament_generator.tournament_dict:
                        for tournament in self.tournament_generator.tournament_dict[date]:
                            if not self.main_interface.in_simulation:
                                tournament_button = ctk.CTkButton(day_frame, text=tournament.name, text_color="black",
                                                                command=lambda t=tournament: self.select_tournament(t))
                                self.highlight_button(tournament_button, tournament)
                                tournament_button.pack(fill="both", padx=5, pady=5)

                                tournament_button.bind("<Enter>", lambda event, t=tournament: self.show_tournament_info(t))
                                tournament_button.bind("<Leave>", lambda event: self.clear_info_display())
                            else:
                                tournament_button = ctk.CTkButton(day_frame, text=tournament.name, text_color="black",
                                                        command=lambda t=tournament: self.main_interface.display_tournament_info(t))
                                self.highlight_button(tournament_button, tournament)
                                self.highlight_tournament(tournament_button, tournament)

                                tournament_button.bind("<Enter>", lambda event, t=tournament: self.show_tournament_info(t))
                                tournament_button.bind("<Leave>", lambda event: self.clear_info_display())
                                tournament_button.pack(fill="x", padx=1, pady=1)
                    else:
                        # Show day number if there are no tournaments
                        day_label = ctk.CTkLabel(day_frame, text=str(day), width=10, height=3)
                        day_label.pack(fill="both", expand=True)
    
    def select_tournament(self, tournament):
        allowed_to_participate = False
        if tournament.normal_tournament:
            if tournament.min_elo < self.main_interface.selected_team.elo < tournament.max_elo:
                allowed_to_participate = True
        elif tournament.open_tournament:
            if tournament.min_elo < self.main_interface.selected_team.elo < tournament.max_elo:
                allowed_to_participate = True
        elif tournament.invite_tournament:
            if tournament.min_elo < self.main_interface.selected_team.elo < tournament.max_elo:
                allowed_to_participate = True
        elif tournament.national_tournament:
            allowed_to_participate = self.main_interface.tournament_director.eligible_for_tournament(self.main_interface.selected_team, tournament)

        if allowed_to_participate:
            date = tournament.start_date

            for element in self.main_interface.selected_tournaments:
                if element != tournament:
                    if element.start_date == date:
                        self.main_interface.selected_tournaments.remove(element)

                        for label in self.selected_tournaments_frame.winfo_children():
                            if label.cget("text") == tournament.name:
                                label.destroy()
                                break
                        break
            
            if tournament.name in [t.name for t in self.main_interface.selected_tournaments]:
                self.main_interface.selected_tournaments.remove(tournament)
                for label in self.selected_tournaments_frame.winfo_children():
                    if label.cget("text") == tournament.name:
                        label.destroy()
                        break
            else:
                self.main_interface.selected_tournaments.append(tournament)
                tournament_label = ctk.CTkLabel(self.selected_tournaments_frame, text=tournament.name, anchor="nw", justify="left", 
                                                width=30, height=20, padx=10, pady=10, text_color="red",)
                tournament_label.grid(row=len(self.main_interface.selected_tournaments) - 1, column=0)

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

            self.tournament_information_label.configure(text=info_text)

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

            self.tournament_information_label.configure(text=info_text)
    
    ## clear the label box
    def clear_info_display(self):
        # Clear the info display area
        self.tournament_information_label.configure(text="")

    ## Highlight the button if the user-selected team is eligible for torunament
    def highlight_button(self, button, tournament):
        allowed_to_participate = False
        if tournament.normal_tournament:
            if tournament.min_elo < self.main_interface.selected_team.elo < tournament.max_elo:
                allowed_to_participate = True
        elif tournament.open_tournament:
            if tournament.min_elo < self.main_interface.selected_team.elo < tournament.max_elo:
                allowed_to_participate = True
        elif tournament.invite_tournament:
            if tournament.min_elo < self.main_interface.selected_team.elo < tournament.max_elo:
                allowed_to_participate = True
        elif tournament.national_tournament:
            allowed_to_participate = self.main_interface.tournament_director.eligible_for_tournament(self.main_interface.selected_team, tournament)

        if allowed_to_participate:
            button.configure(fg_color="#87CEEB")
        else:
            if tournament.open_tournament:
                button.configure(fg_color="#ffe4e1")
            elif tournament.invite_tournament:
                button.configure(fg_color="#b8860b")
            elif tournament.national_tournament:
                button.config(fg_color="#c71585")
    
    def highlight_tournament(self, button, tournament):
        if tournament in self.main_interface.selected_tournaments:
            button.configure(fg_color="#FA8072")
