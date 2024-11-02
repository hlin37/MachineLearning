from bracket import *
from game import *

import random
from datetime import date
import datetime
from itertools import combinations
import json

class Tournament:
    def __init__(self, name, start_date, number_of_teams, priority, min_elo, max_elo, normal_tournament, open_tournament, invite_tournament, national_tournament):
        
        self.name = name
        self.start_date = start_date
        self.min_elo = min_elo
        self.max_elo = max_elo
        self.maxTeams = number_of_teams

        self.normal_tournament = normal_tournament
        self.open_tournament = open_tournament
        self.invite_tournament = invite_tournament
        self.national_tournament = national_tournament
        
        ## Higher-level tournaments are larger in priority.
        self.priority = priority

        ## Reference to the open tournament that qualifies for this invite tournament. 
        ## If this tournament is an invite tournament, the value will be a reference. If not, then the value is None
        ## Type: Tournament
        self.invite_tournament_reference = None

        ## Number of Qualified Teams From the Open Tournament
        self.number_of_qualified_teams = 0

        ## Format of the pools
        self.pool_format = None

        ## List of teams going
        self.teams = []

        ## Waitlist of teams
        self.waitList = []

        ## Once tournament is over, store the winners
        self.winners = []

        ## array holding the arrays of the teams.
        ## the arrays of the teams are the pools
        self.tournament_pool_objects = []

        self.pool_results = []

        self.completed = False

        ## A dictionary that stores a team object key to the initial ranking string going into the tournament
        ## Ex: Key: Team Object -> Value: Fury (1)
        self.team_name_to_ranking = {}

        ## An array that stores arrays of strings i.e Fury (1)
        ## Ex:[0: ["Fury (1)", "Brute (2)"]]
        self.pool_teams = []

        self.bracket = None

    def add_team(self, team):
        # if self.main_tournament:
        #     if team.qualified_for_tournament(self.qualifier_tournament):
        #         if len(self.teams) < self.maxTeams:
        #             self.teams.append(team)
        #     else:
        #         x = 0
        # else:
        #     if len(self.teams) < self.maxTeams:
        #         if self.min_elo <= team['elo'] <= self.max_elo:
        #             self.teams.append(team)

        self.teams.append(team)
    
    ## Creates a string for each team with their ranking going into the tournament
    ## Ex: Fury (1)
    def create_base_pools_names_ranks(self):
        if not self.invite_tournament:
            for pool, seeding in self.pool_format.items():
                pool_teams = []
                for seed in seeding:
                    seed_rank = int(seed.replace("Seed #", ""))
                    name_and_rank = self.teams[seed_rank - 1].teamName + " (" + str(seed_rank) + ")"
                    pool_teams.append(name_and_rank)
                    self.team_name_to_ranking[self.teams[seed_rank - 1]] = name_and_rank
                self.pool_teams.append(pool_teams)
                
    
    def isFull(self):
        if len(self.teams) + 1 + self.number_of_qualified_teams == self.maxTeams:
            return True
        else:
            return False
    
    def add_to_waitlist(self, team):
        self.waitList.append(team)

    
    def run_event(self):
        # teams_index = None
        teams_advancing = self.number_of_qualified_teams
        if (teams_advancing == 0):
            teams_advancing = 1
        self.bracket = Bracket(teams_advancing, self.maxTeams)
        self.handle_pool_play()
        self.bracket.create_bracket(self.pool_results, True)

        # if self.maxTeams in [16,20]:
        #     teams_index = 1
        # else:
        #     teams_index = teams_advancing
        for key in self.bracket.order_of_games_played_bracket[(teams_advancing, self.maxTeams)]:
        # for key in self.bracket.order_of_games_played_bracket[(teams_index, self.maxTeams)]:
            ## Update the bracket
            self.bracket.create_bracket(self.pool_results, False)
            game = Simulation(self.bracket.bracket_dict[key].team1, self.bracket.bracket_dict[key].team2)
            game.main()
            winner, loser, winnerPoints, loserPoints = game.return_winner()
            self.bracket.bracket_dict[key].winner = winner
            self.bracket.bracket_dict[key].winnerPoints = winnerPoints
            self.bracket.bracket_dict[key].loser = loser
            self.bracket.bracket_dict[key].loserPoints = loserPoints

        self.bracket.determine_rankings()
        self.winners = self.bracket.rankings

        self.completed = True

        if self.open_tournament:
            number_of_invites = self.invite_tournament_reference.number_of_qualified_teams
            self.invite_tournament_reference.teams.append(self.winners[0:number_of_invites-1])
    

    def handle_pool_play(self):
        for pool in self.tournament_pool_objects:
            win_loss_record = {team: {"wins": 0, "losses": 0} for team in pool}

            team_combinations = list(combinations(pool, 2))
            for match in team_combinations:
                game = Simulation(match[0], match[1])
                game.main()
                winner, loser, winnerPoints, loserPoints = game.return_winner()

                win_loss_record[winner]["wins"] += 1
                win_loss_record[loser]["losses"] += 1
            
            sorted_teams = sorted(win_loss_record.items(), key=lambda x: (-x[1]["wins"], x[1]["losses"]))

            self.pool_results.append(sorted_teams)


class TournamentGenerator:
    def __init__(self, start_year, num_tournaments, num_invite_tournaments, num_national_tournaments):
        self.start_year = start_year
        self.num_tournaments = num_tournaments
        self.num_invite_tournaments = num_invite_tournaments
        self.national_tournaments = num_national_tournaments

        self.load_pool_formats()

        self.generated_names = set()

        self.tournaments = self.generate_tournaments()

        self.determine_pool_format()

    def generate_unique_name(self):
        prefixes = ["Winter", "Spring", "Summer", "Fall", "Championship", "Open", "Classic", "Challenge", "Showdown", 
                    "Legacy", "Thunder", "Elite", "Majestic", "Royal", "Grand", "Infinity", "Victory", "Triumph"]
        suffixes = ["Competition", "Cup", "Bowl", "Tournament", "Fest", "Series", "Spectacular", "Clash", "Derby", 
                    "Gathering", "Faceoff", "Meet", "Rumble", "Shootout", "Smash"]
        
        while True:
            name = f"{random.choice(prefixes)} {random.choice(suffixes)}"
            if name in self.generated_names:
                count = 1
                while f"{name} {count}" in self.generated_names:
                    name = f"{random.choice(prefixes)} {random.choice(suffixes)}"
                #     count += 1
                # name = f"{name} {count}"
            
            self.generated_names.add(name)
            return name

    def generate_tournaments(self):
        # Create the main tournament for the qualifiers
        # self.main_tournament = Tournament(self.main_tournament_name, date(self.start_year, 12, 15))
        # self.tournaments.append(self.main_tournament)

        tournamentCalendar = []

        # Generate normal events: anyone can attend
        for _ in range(self.num_tournaments):
            name = self.generate_unique_name()
            random_date = self.get_random_date()
            min_elo = random.randint(500, 1500)
            max_elo = min_elo + random.randint(500, 800)
            number_of_teams = random.choice([8, 10, 12, 16])
            tournament = Tournament(name, random_date, number_of_teams, 0, min_elo, max_elo, True, False, False, False)
            tournamentCalendar.append(tournament)

        # Generate open tournaments to qualify for invite-only events
        open_tournaments = []
        for _ in range(self.num_invite_tournaments):
            name = self.generate_unique_name() + " Open"
            random_date = self.get_random_date()
            min_elo = random.randint(500, 1500)
            max_elo = min_elo + random.randint(500, 800)
            number_of_teams = random.choice([8, 10, 12, 16, 20])
            qualifier_tournament = Tournament(name, random_date, number_of_teams, 1, min_elo, max_elo, False, True, False, False)
            open_tournaments.append(qualifier_tournament)
            tournamentCalendar.append(qualifier_tournament)
        
        ## Generate invite only tournaments, with a minimum elo to prevent bad teams from joining
        for i in range(len(open_tournaments)):
            name = open_tournaments[i].name.removesuffix(" Open") + " Invitational"
            random_date = self.add_random_weeks(open_tournaments[i].start_date)
            min_elo = random.randint(900, 1400)
            max_elo = random.randint(1400, 1800)
            invite_only_tournament = Tournament(name, random_date, 16, 2, min_elo, max_elo, False, False, True, False)
            open_tournaments[i].invite_tournament_reference = invite_only_tournament
            tournamentCalendar.append(invite_only_tournament)
        
        # Generate national tournaments, where the highest teams join.
        for i in range(self.national_tournaments):
            name = open_tournaments[i].name.removesuffix(" Open") + " Challenge"
            random_date = self.add_random_weeks(open_tournaments[i].start_date)
            min_elo = 0
            max_elo = 0
            national_only_tournament = Tournament(name, random_date, 16, 3, min_elo, max_elo, False, False, False, True)
            tournamentCalendar.append(national_only_tournament)

        return tournamentCalendar

    def get_random_date(self):
        start_date = date.today().replace(day=1, month=1).toordinal()
        end_date = date.today().replace(day=30, month=12).toordinal()
        random_day = date.fromordinal(random.randint(start_date, end_date))

        return random_day

    def add_random_weeks(self, date):
        num_weeks = random.choice([1, 2])
        days_to_add = 7 * num_weeks
        return date + datetime.timedelta(days=days_to_add)

    def load_pool_formats(self):
        f = open("tournament_structure.json")
        self.entire_pool_formats = json.load(f)
        f.close()
    
    def determine_pool_format(self):
        for tournament in self.tournaments:
            pool_formats_for_teams = self.entire_pool_formats[str(tournament.maxTeams)]
            choice = random.choice([0, len(pool_formats_for_teams) - 1])

            format_choice = list(pool_formats_for_teams.keys())[choice]

            tournament.pool_format = pool_formats_for_teams[format_choice]
    
