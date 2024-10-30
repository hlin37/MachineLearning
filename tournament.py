import random
from datetime import date
import datetime

class Tournament:
    def __init__(self, name, start_date, number_of_teams, priority, min_elo, max_elo, normal_tournament, open_tournament, invite_tournament, national_tournament, open_to_invite_ref):
        self.name = name
        self.start_date = start_date
        self.min_elo = min_elo
        self.max_elo = max_elo
        self.maxTeams = number_of_teams

        self.normal_tournament = normal_tournament
        self.open_tournament = open_tournament
        self.invite_tournament = invite_tournament
        self.national_tournament = national_tournament

        self.priority = priority

        self.open_tournament_to_invite_tournament = open_to_invite_ref
        self.number_of_qualified_teams = 0

        self.teams = []
        self.waitList = []

        self.winners = []

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
    
    def isFull(self):
        if len(self.teams) + 1 + self.number_of_qualified_teams == self.maxTeams:
            return True
        else:
            return False
    
    def add_to_waitlist(self, team):
        self.waitList.append(team)

class TournamentGenerator:
    def __init__(self, start_year, num_tournaments, num_invite_tournaments, num_national_tournaments):
        self.start_year = start_year
        self.num_tournaments = num_tournaments
        self.num_invite_tournaments = num_invite_tournaments
        self.national_tournaments = num_national_tournaments

        self.generated_names = set()

        self.tournaments = self.generate_tournaments()

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
            tournament = Tournament(name, random_date, number_of_teams, 0, min_elo, max_elo, True, False, False, False, None)
            tournamentCalendar.append(tournament)

        # Generate open tournaments to qualify for invite-only events
        invite_tournaments = []
        for _ in range(self.num_invite_tournaments):
            name = self.generate_unique_name() + " Open"
            random_date = self.get_random_date()
            min_elo = random.randint(500, 1500)
            max_elo = min_elo + random.randint(500, 800)
            number_of_teams = random.choice([8, 10, 12, 16, 20])
            qualifier_tournament = Tournament(name, random_date, number_of_teams, 1, min_elo, max_elo, False, True, False, False, None)
            invite_tournaments.append(qualifier_tournament)
            tournamentCalendar.append(qualifier_tournament)
        
        ## Generate invite only tournaments, with a minimum elo to prevent bad teams from joining
        for i in range(len(invite_tournaments)):
            name = invite_tournaments[i].name.removesuffix(" Open") + " Invitational"
            random_date = self.add_random_weeks(invite_tournaments[i].start_date)
            min_elo = random.randint(900, 1400)
            max_elo = random.randint(1400, 1800)
            invite_only_tournament = Tournament(name, random_date, number_of_teams, 2, min_elo, max_elo, False, False, True, False, invite_tournaments[i])
            tournamentCalendar.append(invite_only_tournament)
        
        # Generate national tournaments, where the highest teams join.
        for i in range(self.national_tournaments):
            name = invite_tournaments[i].name.removesuffix(" Open") + " Challenge"
            random_date = self.add_random_weeks(invite_tournaments[i].start_date)
            min_elo = 0
            max_elo = 0
            national_only_tournament = Tournament(name, random_date, 16, 3, min_elo, max_elo, False, False, False, True, None)
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