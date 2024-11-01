from team import *
from tournament import *
import random
# import json

class TournamentDirector:

    def __init__(self, teamGenerator, tournamentGenerator):
        self.all_teams = teamGenerator.teamList
        self.tournaments = tournamentGenerator.tournaments

        self.all_teams_sorted_by_elo = sorted(self.all_teams, key=lambda x: x.elo, reverse=True)
    
    def remove_from_team_list(self, playerTeam):
        for element in self.all_teams:
            if element.teamName == playerTeam:
                self.all_teams.remove(element)
                return element

    def decide_which_tournament(self):

        tournament_dict = {}
        for t in self.tournaments:
            if t.start_date not in tournament_dict:
                tournament_dict[t.start_date] = []
            tournament_dict[t.start_date].append(t)
        
        self.team_sorted_by_elo = sorted(self.all_teams, key=lambda x: x.elo, reverse=True)

        for tournament in self.tournaments:
            if tournament.national_tournament:
                for team in self.team_sorted_by_elo:
                    choice = random.choice([0,1])
                    if choice == 1:
                        if tournament.isFull():
                            tournament.add_to_waitlist(team)
                        else:
                            tournament.add_team(team)
                            team.add_to_tournament_list(tournament, tournament_dict)
            elif tournament.invite_tournament:
                number_of_qualified_teams = random.choice([2,4,6])
                eligble_index = self.find_indices(self.team_sorted_by_elo, tournament.min_elo, tournament.max_elo)
                allowed_teams = self.team_sorted_by_elo[eligble_index[1]:eligble_index[0]]

                tournament.number_of_qualified_teams = number_of_qualified_teams

                # for i in range(number_of_qualified_teams):
                #     tournament.add_team(None)
                
                for team in allowed_teams:
                    choice = random.choice([0,1])
                    if choice == 1:
                        if tournament.isFull():
                            tournament.add_to_waitlist(team)
                        else:
                            tournament.add_team(team)
                            team.add_to_tournament_list(tournament, tournament_dict)
                
                
            else:
                eligble_index = self.find_indices(self.team_sorted_by_elo, tournament.min_elo, tournament.max_elo)
                allowed_teams = self.team_sorted_by_elo[eligble_index[1]:eligble_index[0]]

                for team in allowed_teams:
                    choice = random.choice([0,1])
                    if choice == 1:
                        if tournament.isFull():
                            tournament.add_to_waitlist(team)
                        else:
                            tournament.add_team(team)
                            team.add_to_tournament_list(tournament, tournament_dict)
                    
    
    def find_indices(self, arr, min_val, max_val):
        smallest_index = None
        largest_index = None
        
        # Find the smallest index with an element greater than the minimum
        for i in range(len(arr) - 1, -1, -1):
            if arr[i].elo > min_val:
                smallest_index = i
                break
        
        # Find the largest index with an element smaller than the maximum
        for j in range(len(arr)):
            if arr[j].elo < max_val:
                largest_index = j
                break
        
        return smallest_index, largest_index

    def eligible_for_tournament(self, team, tournament):
        if self.all_teams_sorted_by_elo.index(team) <= tournament.maxTeams:
            return True
        else:
            return False
    
    # def load_pool_formats(self):
    #     f = open("tournament_structure.json")
    #     self.entire_pool_formats = json.load(f)
    #     f.close()
    
    # def determine_pool_format(self, number_of_teams):
    #     pool_formats_for_teams = self.entire_pool_formats[str(number_of_teams)]
    #     choice = random.choice([0, len(pool_formats_for_teams) - 1])

    #     format_choice = list(pool_formats_for_teams.keys())[choice]

    #     return pool_formats_for_teams[format_choice]
    
            
# Testing purposes
# teamGenerator = TeamGenerator()
# tournamentGenerator = TournamentGenerator("2024", 100, 20, 10)
# director = TournamentDirector(teamGenerator, tournamentGenerator)