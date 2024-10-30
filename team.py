from player import Player
import uuid
import random

class Team:

    # def __init__(self, teamName, teamID, start):
    #     self.roster = []
    #     self.teamName = teamName
    #     self.teamID = teamID
    #     self.numberOfPoints = 0
    #     # self.createTeam(start)
    #     self.elo = 0
    

    def __init__(self, teamName, teamID, conference, region, team_elo, roster):
        self.roster = roster
        self.teamName = teamName
        self.teamID = teamID
        self.numberOfPoints = 0
        self.conference = conference
        self.region = region
        self.ranking = None
        self.elo = team_elo
        
        self.tournament_list = []
    
    def returnBoxScore(self):
        for i in range(7):
            print(self.roster[i].name, end = " ")
            print(self.roster[i].statsDictionary)
    
    def add_to_tournament_list(self, tournament, tournament_dict):
        if len(tournament_dict[tournament.start_date]) > 1:
            for element in tournament_dict[tournament.start_date]:
                if element in self.tournament_list:
                    if (tournament.priority > element.priority):
                        self.tournament_list.remove(element)
                        self.tournament_list.append(tournament)
        else:
            self.tournament_list.append(tournament)
            
    
    # def createTeam(self, start):
    #     counter = start
    #     f = open('names.txt', 'r')
    #     names = f.readlines()
    #     while abs(start - counter) < 7:
    #         player = Player(names[counter])
    #         self.roster.append(player)
    #         counter += 1
    #         player.setTeam(self)
        
    #     f.close()

class TeamGenerator:
    def __init__(self):
        self.numberOfPlayers = 14
        self.first_names = self.read_names("first-names.txt")
        self.last_names = self.read_names("last-names.txt")
        self.teamList = self.read_in_teams(self.numberOfPlayers)
    
    def read_names(self, file_path):
        with open(file_path, "r") as file:
            return [line.strip() for line in file if line.strip()]  # Read and strip names
    
    def read_in_teams(self, numberOfPlayers):
        teams = []
        
        counter = 1
        with open("usau_mens_teams.txt", "r") as file:
            next(file)  # Skip the header
            
            for line in file:
                columns = line.strip().split("\t")
                
                if len(columns) > 1:
                    team_name = columns[1].strip()
                    team_id = counter
                    
                    # Handle team elo more succinctly
                    try:
                        team_elo = int(columns[2].strip())
                        team_elo = max(team_elo, 500)  # Ensure ELO is at least 500
                    except (ValueError, IndexError):
                        team_elo = random.randint(500, 900)

                    # Create the roster with random first and last names
                    roster = [Player(random.choice(self.first_names) + " " + random.choice(self.last_names)) for _ in range(numberOfPlayers)]

                    team = Team(team_name, team_id, columns[8].strip(), columns[7].strip(), team_elo, roster)
                    teams.append(team)

                    counter += 1
        
        return teams


    
    # def read_in_locations(self):
    #    regions_dict = {}

    #    with open("locations.txt", "r") as file:
    #     lines = file.readlines()

    #     region_name = None
    #     conferences = []

    #     for line in lines:
    #         line = line.strip()

    #         if line:  # If the line is not empty
    #             if not region_name:  # First line of a section is the region name
    #                 region_name = line
    #             else:  # Subsequent lines are conferences
    #                 conferences.append(line)
    #         else:  # Empty line signals the end of a region section
    #             if region_name and conferences:
    #                 regions_dict[region_name] = conferences
    #             region_name = None
    #             conferences = []

    #     # Add the last region if the file does not end with a blank line
    #     if region_name and conferences:
    #         regions_dict[region_name] = conferences

    #     return regions_dict


