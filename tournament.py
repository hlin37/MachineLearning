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

        self.invited_teams = []

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

        self.pool_score_results = {}

    def add_team(self, team):
        self.teams.append(team)
    
    ## Creates a string for each team with their ranking going into the tournament
    ## Ex: Fury (1)
    def create_base_pools_names_ranks(self):
        if len(self.teams) == self.maxTeams:
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

    def add_to_invited_teams(self, team):
        self.invited_teams.append(team)
    
    def run_event(self):
        # teams_index = None
        teams_advancing = self.number_of_qualified_teams
        if (self.maxTeams in [16, 20] or teams_advancing == 0):
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

        self.adjust_ratings_for_placement()

        self.completed = True

        if self.open_tournament:
            number_of_invites = self.invite_tournament_reference.number_of_qualified_teams

            ## Check if the invite tournament is on the same date as any lower priority tournament
            for index in range(0, number_of_invites):
                ## Loop through each tournament bid-winners and their tournaments:
                tournament_list = self.winners[index].tournament_list
                has_added = False
                for competition in tournament_list:
                    ## If the competition is not the open tournament or the invite tournament
                    if competition != self and competition != self.invite_tournament_reference:
                        ## If a future competition is equal to this invite_tournament's start date
                        if self.invite_tournament_reference.start_date == competition.start_date:
                            ## If the invite tournament has more priority than the competition, then the team wants to go to the invite
                            if self.invite_tournament_reference.priority > competition.priority:
                                ## Therefore, add to invite tournament list of teams the team that won.
                                self.invite_tournament_reference.teams.append(self.winners[index])
                                ## And remove from the team that won, that tournament on the same date.
                                self.winners[index].tournament_list.remove(competition)

                                self.winners[index].tournament_list.append(self.invite_tournament_reference)

                                ## Fill that spot with another team:
                                competition.teams.remove(self.winners[index])
                                competition.teams.append(competition.waitList.pop())
                                has_added = True
                                break
                
                ## If there is no tournament with the same date, add the invite tournament to bid_winner
                if not has_added:
                    self.invite_tournament_reference.teams.append(self.winners[index])
                    self.winners[index].tournament_list.append(self.invite_tournament_reference)
            
            self.invite_tournament_reference.create_base_pools_names_ranks()

    def handle_pool_play(self):
        alpha = "A"
        for pool in self.tournament_pool_objects:
            pool_alphabet = "Pool " + alpha
            self.pool_score_results[pool_alphabet] = []
            win_loss_record = {team: {"wins": 0, "losses": 0} for team in pool}

            team_combinations = list(combinations(pool, 2))
            for match in team_combinations:
                game = Simulation(match[0], match[1])
                game.main()
                winner, loser, winnerPoints, loserPoints = game.return_winner()

                winner.adjust_rating(winnerPoints - loserPoints)
                loser.adjust_rating(loserPoints - winnerPoints)

                self.pool_score_results[pool_alphabet].append(winner.teamName + " | " + loser.teamName + " : " + str(winnerPoints) + "-" + str(loserPoints))

                win_loss_record[winner]["wins"] += 1
                win_loss_record[loser]["losses"] += 1
            
            alpha = chr(ord(alpha) + 1) 
            
            sorted_teams = sorted(win_loss_record.items(), key=lambda x: (-x[1]["wins"], x[1]["losses"]))

            sorted_teams = self.handle_ties(sorted_teams)

            self.pool_results.append(sorted_teams)
    
    def handle_ties(self, sorted_teams):
        i = 0
        while i < len(sorted_teams) - 1:
            j = i
            tied_teams = [sorted_teams[j]]
            
            # Find groups of tied teams
            while j + 1 < len(sorted_teams) and sorted_teams[j][1]["wins"] == sorted_teams[j + 1][1]["wins"]:
                tied_teams.append(sorted_teams[j + 1])
                j += 1

            if len(tied_teams) > 1:
                # Extract team names for the head-to-head comparison
                tied_team_names = [team[0] for team in tied_teams]

                # Get head-to-head records among tied teams
                head_to_head_record = self.head_to_head(tied_team_names)

                # Sort based on head-to-head records, then apply further tiebreakers if necessary
                tied_teams = sorted(
                    tied_teams, 
                    key=lambda x: (head_to_head_record[x[0]]["wins"], -head_to_head_record[x[0]]["losses"]), 
                    reverse=True
                )
                
                # Replace the range in the sorted list with resolved ties
                sorted_teams[i:j + 1] = tied_teams

            i = j + 1
        return sorted_teams

    # Helper methods for tiebreakers
    def head_to_head(self, tied_teams):
        # Create a dictionary for head-to-head records
        head_to_head_record = {team: {"wins": 0, "losses": 0} for team in tied_teams}

        # Iterate over all game results to find matches between tied teams
        for pool_results in self.pool_score_results.values():
            for result in pool_results:
                winner, match_details = result.split(" | ")
                loser = match_details.split(" : ")[0]

                if winner in tied_teams and loser in tied_teams:
                    head_to_head_record[winner]["wins"] += 1
                    head_to_head_record[loser]["losses"] += 1

        return head_to_head_record

    def adjust_ratings_for_placement(self):
        for team in self.teams:
            intitial_seeding = self.teams.index(team)
            final_seeding = self.winners.index(team)

            c = 40
            placement_rating = c * ((intitial_seeding - final_seeding) / self.maxTeams)
            team.rating += placement_rating

class TournamentGenerator:
    def __init__(self, start_year, num_tournaments, num_invite_tournaments, num_national_tournaments):
        self.start_year = start_year
        self.num_tournaments = num_tournaments
        self.num_invite_tournaments = num_invite_tournaments
        self.national_tournaments = num_national_tournaments

        self.sectional_tournaments = []
        self.regional_tournaments = []
        self.final_tournament = []

        self.load_pool_formats()

        self.generated_names = set()

        self.tournaments = self.generate_tournaments()

        self.determine_pool_format()

        # A dictionary to list all tournaments by date
        self.create_tournament_dict()

    def generate_unique_name(self):
        prefixes = ["Winter", "Spring", "Summer", "Fall", "Summit", "Frontier", "Classic", "Crown", "Pinnacle", 
                    "Legacy", "Thunder", "Elite", "Majestic", "Royal", "Grand", "Infinity", "Victory", "Triumph"]
        suffixes = ["Competition", "Cup", "Bowl", "Showdown", "Fest", "Series", "Spectacular", "Clash", "Derby", 
                    "Gathering", "Faceoff", "Meet", "Rumble", "Shootout", "Smash"]
        
        while True:
            name = f"{random.choice(prefixes)} {random.choice(suffixes)}"
            if name in self.generated_names:
                count = 1
                while f"{name} {count}" in self.generated_names:
                    name = f"{random.choice(prefixes)} {random.choice(suffixes)}"
            
            self.generated_names.add(name)
            return name
    
    def generate_open_names(self):
        # List of famous cities in the United States
        cities = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", 
                "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose", 
                "Austin", "Jacksonville", "Fort Worth", "Columbus", "Charlotte", 
                "San Francisco", "Indianapolis", "Seattle", "Denver", "Washington",
                "Boston", "El Paso", "Nashville", "Detroit", "Oklahoma City", "Stanford"]
        
        name = ""
        while name not in self.generated_names or name == "":
            name = random.choice(cities) + " Open"
            self.generated_names.add(name)
        
        return name

    def generate_national_names(self):
        unique_words = [
                        "Apex", "Quantum", "Radiance", "Odyssey", "Harbinger", 
                        "Infinity", "Momentum", "Catalyst", "Euphoria", "Phantom", 
                        "Zenith", "Vortex", "Nexus", "Echo", "Spectra", 
                        "Arc", "Horizon", "Pulse", "Ember", "Ignite", 
                        "Flare", "Torrent", "Synergy", "Fusion", "Eclipse", 
                        "Solstice", "Nova", "Aurora", "Expedition", "Trident",
                        "Rift", "Convergence", "Obsidian", "Chronicle", "Paragon", 
                        "Legacy", "Vertex", "Mirage", "Forge", "Surge", 
                        "Ascension", "Vertex", "Impulse", "Crusade", "Rising", 
                        "Virtue", "Resolve", "Fury", "Emissary", "Echo", 
                        "Blaze", "Havoc"]
        prefixes = ["Northeast", "Northwest", "Southeast", "Southwest", "East", "West", "North", "South"]
        name = ""
        while name not in self.generated_names or name == "":
            name = random.choice(prefixes) + " " + random.choice(unique_words)
            self.generated_names.add(name)
        
        return name

    def generate_tournaments(self):
        # Create the main tournament for the qualifiers
        # self.main_tournament = Tournament(self.main_tournament_name, date(self.start_year, 12, 15))
        # self.tournaments.append(self.main_tournament)

        tournamentCalendar = []

        ## Generate normal events: anyone can attend
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
            name = self.generate_open_names()
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
            name = self.generate_national_names()
            random_date = self.add_random_weeks(open_tournaments[i].start_date)
            min_elo = 0
            max_elo = 0
            national_only_tournament = Tournament(name, random_date, 16, 3, min_elo, max_elo, False, False, False, True)
            tournamentCalendar.append(national_only_tournament)
        
        self.generate_sectional_tournaments()
        self.generate_regionals_tournaments()
        self.generate_final_tournament()

        return tournamentCalendar
    
    def generate_sectional_tournaments(self):
        sections = ["Big Sky", "Capital", "Central Plains", "East Coast", "East New England",
                    "East Plains", "Florida", "Founders", "Gulf Coast", "Metro New York", "Northern Cal",
                    "North Carolina", "Northwest Plains", "Oregon", "Ozarks", "Rocky Mountain", "Southern Cal",
                    "Texas", "Upstate New York", "Washington", "West New England", "West Plains"]
        
        for section in sections:
            name = section + " Sectional Championship"
            start_date = date.today().replace(day=1, month=12).toordinal()
            end_date = date.today().replace(day=10, month=12).toordinal()
            random_day = date.fromordinal(random.randint(start_date, end_date))
            min_elo = 0
            max_elo = 0
            sectional_tournament = Tournament(name, random_day, 0, 4, min_elo, max_elo, False, False, False, False)
            self.sectional_tournaments.append(sectional_tournament)
    
    def generate_regionals_tournaments(self):
        sections = ["Great Lakes", "Mid-Atlantic", "North Central", "Northeast", "Northwest", "South Central",
                    "Southeast", "Southwest"]
        
        for section in sections:
            name = section + " Regional Championship"
            start_date = date.today().replace(day=10, month=12).toordinal()
            end_date = date.today().replace(day=24, month=12).toordinal()
            random_day = date.fromordinal(random.randint(start_date, end_date))
            min_elo = 0
            max_elo = 0
            regional_tournament = Tournament(name, random_day, 0, 5, min_elo, max_elo, False, False, False, False)
            self.regional_tournaments.append(regional_tournament)
    
    def generate_final_tournament(self):
            name = "Ultimate Fribsee Championships"
            day = date.today().replace(day=31, month=12).toordinal()
            min_elo = 0
            max_elo = 0
            final_tournament = Tournament(name, day, 0, 6, min_elo, max_elo, False, False, False, False)
            self.final_tournament.append(final_tournament)
    

    def get_random_date(self):
        start_date = date.today().replace(day=1, month=1).toordinal()
        end_date = date.today().replace(day=30, month=11).toordinal()
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
    
    def create_tournament_dict(self):
        self.tournament_dict = {}
        for t in self.tournaments:
            day = t.start_date
            if day not in self.tournament_dict:
                self.tournament_dict[day] = []
            self.tournament_dict[day].append(t)
    
