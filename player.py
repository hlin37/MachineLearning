class Player:

    name = ""
    team = None

    statsDictionary = None

    def __init__(self, name):
        self.name = name.strip()
        self.statsDictionary = {
            "numberOfAssists" : 0,
            "numberOfGoals" : 0,
            "numberOfTurnovers" : 0,
            "numberOfBlocks" : 0,
            "numberOfDrops" :  0,
        }
    
    def setTeam(self, team):
        self.team = team
    

    def addScore(self):
        self.statsDictionary["numberOfGoals"] += 1
    
    def addAssist(self):
        self.statsDictionary["numberOfAssists"] += 1
    
    def addTurnover(self):
        self.statsDictionary["numberOfTurnovers"] += 1

    def addDrop(self):
        self.statsDictionary["numberOfDrops"] += 1
    
    def addBlock(self):
        self.statsDictionary["numberOfBlocks"] += 1
    


