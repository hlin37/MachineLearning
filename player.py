import pandas as pd

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
        self.attributes = self.read_in_attributes()
    
    def read_in_attributes(self):
        entire_attribute_df = pd.read_excel('player_stats.xlsx')

        entire_attribute_df = entire_attribute_df.replace(to_replace= r'\\', value= '', regex=True)

        player_row = entire_attribute_df[entire_attribute_df['name'] == self.name]
        
        # Check if player exists in the file
        if player_row.empty:
            print(f"Player {self.name} not found in the Excel file.")
            return
        
        # Drop the 'name' column and load the stats into self.attribute
        stats = player_row.drop(columns=['name']).iloc[0].to_dict()
        
        return stats
    
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
    


