from player import Player

class Team:

    def __init__(self, teamName, teamID, start):
        self.roster = []
        self.teamName = teamName
        self.teamID = teamID
        self.numberOfPoints = 0
        self.createTeam(start)
    
    
    def returnBoxScore(self):
        for i in range(7):
            print(self.roster[i].name, end = " ")
            print(self.roster[i].statsDictionary)
    
    def createTeam(self, start):
        counter = start
        f = open('names.txt', 'r')
        names = f.readlines()
        while abs(start - counter) < 7:
            player = Player(names[counter])
            self.roster.append(player)
            counter += 1
            player.setTeam(self)
        
        f.close()
        
