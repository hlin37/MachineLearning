from team import *
from tournament import *
import random

class TournamentDirector:

    def __init__(self, teamGenerator, tournamentGenerator):
        self.teams = teamGenerator.teamList
        self.tournaments = tournamentGenerator.tournaments
    
    def remove_from_team_list(self, playerTeam):
        for element in self.teams:
            if element.teamName == playerTeam:
                self.teams.remove(element)

    def decide_which_tournament(self):

        tournament_dict = {}
        for t in self.tournaments:
            if t.start_date not in tournament_dict:
                tournament_dict[t.start_date] = []
            tournament_dict[t.start_date].append(t)
        
        team_sorted_by_elo = sorted(self.teams, key=lambda x: x.elo, reverse=True)

        for tournament in self.tournaments:
            if tournament.national_tournament:
                for team in team_sorted_by_elo:
                    choice = random.choice([0,1])
                    if choice == 1:
                        if tournament.isFull():
                            tournament.add_to_waitlist(team)
                        else:
                            tournament.add_team(team)
                            team.add_to_tournament_list(tournament, tournament_dict)
            elif tournament.invite_tournament:
                number_of_qualified_teams = random.choice([2,4,6])
                eligble_index = self.find_indices(team_sorted_by_elo, tournament.min_elo, tournament.max_elo)
                allowed_teams = team_sorted_by_elo[eligble_index[0]:eligble_index[1]]
                for i in range(number_of_qualified_teams):
                    tournament.add_team(None)
                
                for team in allowed_teams:
                    choice = random.choice([0,1])
                    if choice == 1:
                        if tournament.isFull():
                            tournament.add_to_waitlist(team)
                        else:
                            tournament.add_team(team)
                            team.add_to_tournament_list(tournament, tournament_dict)
            else:
                eligble_index = self.find_indices(team_sorted_by_elo, tournament.min_elo, tournament.max_elo)
                allowed_teams = team_sorted_by_elo[eligble_index[1]:eligble_index[0]]

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

            
# Testing purposes
# teamGenerator = TeamGenerator()
# tournamentGenerator = TournamentGenerator("2024", 100, 20, 10)
# director = TournamentDirector(teamGenerator, tournamentGenerator)