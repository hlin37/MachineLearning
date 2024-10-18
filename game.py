from collections import defaultdict
import re
import numpy as np
import pandas as pd
import random
import math
from team import Team

class Simulation:

    # List of actions
    actions = ["Pull", "Swing", "Pass", "Dump", "Dish", "Huck", "Stall", "Block", "Dropped pass",
            "Dropped huck", "Throwaway", "Huck throwaway", "Score"]
    

    def __init__(self, team1, team2):
        self.yard_distribution = self.createYardDistibution()
        self.action_counts = self.createActionCounts()
        self.action_to_index = {action: i for i, action in enumerate(self.actions)}
        self.baseTransitionMatrix = self.readManualTransitionMatrix()
        self.discXCoordinate = 0
        self.goingLeftToRight = True
        self.pointScored = False

        self.team1 = team1
        self.team2 = team2

        self.teamOnOffense = None
        self.teamOnDefense = None
    
    def createYardDistibution(self):
        # Dictionary to store yard values for each action
        yard_distribution = defaultdict(list)

        # Function to extract yards and action from each line
        def extract_yards_action(line):
            match = re.match(r"(\d+)\s+(.*)", line)
            if match:
                yards = int(match.group(1))
                action = match.group(2)
                for act in self.actions:
                    if act in action:
                        return yards, act
            return None, None

        # Reading the file and filling yard_distribution
        with open("gameEvent.txt", "r") as file:
            for line in file:
                yards, action = extract_yards_action(line)
                if action:
                    yard_distribution[action].append(yards)
        
        yard_distribution["Huck throwaway"] = yard_distribution["Huck"]
        yard_distribution["Dropped huck"] = yard_distribution["Huck"]
        
        return yard_distribution
    
    def createActionCounts(self):
        # Dictionary to store the count of each action
        action_counts = defaultdict(int)

        # Function to extract the action from each line
        def extract_action(line):
            for act in self.actions:
                if act in line:
                    return act
            return None

        # Reading the file and counting occurrences of each action
        with open("gameEvent.txt", "r") as file:
            for line in file:
                action = extract_action(line)
                if action:
                    action_counts[action] += 1
        
        action_counts["Huck throwaway"] = action_counts["Huck"]
        action_counts["Dropped huck"] = action_counts["Huck"]
        
        return action_counts
    
    def readManualTransitionMatrix(self):

        # Base transition matrix (Markov Chain)
        transition_df = pd.read_excel('manualCreatedActionMatrix.xlsx')  # index_col=0 sets the first column as the index

        # Convert the DataFrame to a NumPy array
        transition_matrix = transition_df.to_numpy()
    
        return transition_matrix

    # Continuous scaling functions for each action based on distance
    def huck_modifier(self, distance):
        return max(0.1, distance / 100)  # Huck becomes less likely as distance decreases

    def score_modifier(self, distance):
        return min(2.0, (100 - distance) / 50)  # Scoring becomes more likely closer to the goal

    def pass_modifier(self, distance):
        return max(0.8, 1 - (100 - distance) / 300)  # Slightly less frequent closer to goal

    def dump_dish_modifier(self, distance):
        return min(2.0, (100 - distance) / 50)  # Short passes become more likely near the goal

    def swing_modifier(self, distance):
        return max(0.8, 1 - (100 - distance) / 200)  # Slightly less frequent near the goal

    def stall_modifier(self, distance):
        return 1.0  # Stall rate remains constant

    def drop_modifier(self, distance):
        return min(1.5, 1 + (100 - distance) / 200)  # Drops increase slightly closer to goal

    def block_modifier(self, distance):
        return min(2.0, (100 - distance) / 50)  # Blocks more likely near goal

    def throwaway_modifier(self, distance):
        return min(1.5, 1 + (100 - distance) / 200)  # Throwaways more likely closer to goal

    # Function to dynamically adjust the transition matrix based on continuous distance functions
    def adjust_probabilities_club_ultimate(self, distance_to_goal):
        adjustment_matrix = np.ones_like(self.baseTransitionMatrix)

        # Get the continuous modifiers for each action based on the current distance
        huck_mod = self.huck_modifier(distance_to_goal)
        score_mod = self.score_modifier(distance_to_goal)
        pass_mod = self.pass_modifier(distance_to_goal)
        dump_dish_mod = self.dump_dish_modifier(distance_to_goal)
        swing_mod = self.swing_modifier(distance_to_goal)
        drop_mod = self.drop_modifier(distance_to_goal)
        block_mod = self.block_modifier(distance_to_goal)
        throwaway_mod = self.throwaway_modifier(distance_to_goal)

        # Apply modifications to relevant actions
        huck_idx = self.action_to_index["Huck"]
        score_idx = self.action_to_index["Score"]
        pass_idx = self.action_to_index["Pass"]
        dump_idx = self.action_to_index["Dump"]
        dish_idx = self.action_to_index["Dish"]
        swing_idx = self.action_to_index["Swing"]
        drop_idx = self.action_to_index["Dropped pass"]
        dropped_huck_idx = self.action_to_index["Dropped huck"]
        block_idx = self.action_to_index["Block"]
        throwaway_idx = self.action_to_index["Throwaway"]
        huck_throwaway_idx = self.action_to_index["Huck throwaway"]

        for i in range(len(self.actions)):
            adjustment_matrix[i][huck_idx] *= huck_mod
            adjustment_matrix[i][score_idx] *= score_mod
            adjustment_matrix[i][pass_idx] *= pass_mod
            adjustment_matrix[i][dump_idx] *= dump_dish_mod
            adjustment_matrix[i][dish_idx] *= dump_dish_mod
            adjustment_matrix[i][swing_idx] *= swing_mod
            adjustment_matrix[i][drop_idx] *= drop_mod
            adjustment_matrix[i][throwaway_idx] *= throwaway_mod
            adjustment_matrix[i][dropped_huck_idx] *= drop_mod
            adjustment_matrix[i][huck_throwaway_idx] *= throwaway_mod
            if (distance_to_goal <= 40):
                adjustment_matrix[i][dropped_huck_idx] *= drop_mod
                adjustment_matrix[i][drop_idx] += adjustment_matrix[i][dropped_huck_idx]
                adjustment_matrix[i][dropped_huck_idx] = 0

                adjustment_matrix[i][huck_throwaway_idx] *= throwaway_mod
                adjustment_matrix[i][throwaway_idx] += adjustment_matrix[i][huck_throwaway_idx]
                adjustment_matrix[i][huck_throwaway_idx] = 0

                adjustment_matrix[i][huck_idx] *= huck_mod
                adjustment_matrix[i][pass_idx] += adjustment_matrix[i][huck_idx]
                adjustment_matrix[i][huck_idx] = 0
        
            adjustment_matrix[i][block_idx] *= block_mod

        # Adjust the original transition matrix with the continuous modifiers
        adjusted_matrix = self.baseTransitionMatrix * adjustment_matrix

        # Re-normalize each row to ensure probabilities sum to 1
        row_sums = np.sum(adjusted_matrix, axis=1, keepdims=True)
        adjusted_matrix = np.divide(adjusted_matrix, row_sums, where=row_sums != 0)

        return adjusted_matrix
    
    def predict_next_action_markov(self, current_action, distance_to_goal):

        """Predicts the next action using only the Markov Chain."""
        # Adjust Markov Chain probabilities based on distance
        adjusted_matrix = self.adjust_probabilities_club_ultimate(distance_to_goal)

        # Get probabilities from Markov Chain
        current_idx = self.action_to_index[current_action]
        markov_probabilities = adjusted_matrix[current_idx]

        # Sample the next action based on the probabilities
        next_action_idx = np.random.choice(len(self.actions), p=markov_probabilities)
        return self.actions[next_action_idx]
    
    def randomYardsForAction(self, action):
        if action == "Pull":

            action_yard_counts = self.yard_distribution[action]
            action_action_counts = self.action_counts[action]

            # 2. Normalize frequencies
            probabilities = [count / action_action_counts for count in np.histogram(action_yard_counts, bins=20)[0]]
            yard_values = np.histogram(action_yard_counts, bins=20)[1]  # Get bin edges

            # # 3. Create probability distribution (list of tuples)
            # distribution = list(zip(yard_values[:-1], probabilities))  # Adjust if binning is different

            # 4. Randomly sample
            random_yard = np.random.choice(yard_values[:-1], p=probabilities)  # Choose random yard
            
            return int(random_yard)

        elif action == "Dump":
            amountOfYardsBehind = 0
            if (self.goingLeftToRight):
                amountOfYardsBehind = self.discXCoordinate
            else:
                amountOfYardsBehind = 110 - self.discXCoordinate
            
            action_yard_counts =  [x for x in self.yard_distribution[action] if 0 <= x < amountOfYardsBehind]
            action_action_counts = len(action_yard_counts)

            if (action_action_counts != 0):

                probabilities = [count / action_action_counts for count in np.histogram(action_yard_counts, bins=20)[0]]
                yard_values = np.histogram(action_yard_counts, bins=20)[1]  # Get bin edges

                # # 3. Create probability distribution (list of tuples)
                # distribution = list(zip(yard_values[:-1], probabilities))  # Adjust if binning is different

                # 4. Randomly sample
                random_yard = np.random.choice(yard_values[:-1], p=probabilities)  # Choose random yard
            else:
                random_yard = random.randint(1, 5)
            
            return int(random_yard)

        elif action == "Score":
            amountOfYardsAhead  = 0
            amountOfYardsToEndzone = 0
            if (self.goingLeftToRight):
                amountOfYardsAhead = 110 - self.discXCoordinate 
                amountOfYardsToEndzone = 90 - self.discXCoordinate
            else:
                amountOfYardsAhead = self.discXCoordinate
                amountOfYardsToEndzone = self.discXCoordinate - 20

            return random.randint(amountOfYardsToEndzone, amountOfYardsAhead)
        
        else:
            amountOfYardsAhead  = 0
            if (self.goingLeftToRight):
                amountOfYardsAhead = 110 - self.discXCoordinate 
            else:
                amountOfYardsAhead = self.discXCoordinate
            
            action_yard_counts =  [x for x in self.yard_distribution[action] if 0 <= x < amountOfYardsAhead]
            action_action_counts = len(action_yard_counts)

            probabilities = [count / action_action_counts for count in np.histogram(action_yard_counts, bins=20)[0]]
            yard_values = np.histogram(action_yard_counts, bins=20)[1]  # Get bin edges

            # # 3. Create probability distribution (list of tuples)
            # distribution = list(zip(yard_values[:-1], probabilities))  # Adjust if binning is different

            # 4. Randomly sample
            random_yard = np.random.choice(yard_values[:-1], p=probabilities)  # Choose random yard
            
            return int(random_yard)
    
    def startWithPull(self):
        next_action = "Pull"
        yardsRemaining = self.randomYardsForAction(next_action)
        if (self.goingLeftToRight):
            self.discXCoordinate = 90 - yardsRemaining
        else:
            self.discXCoordinate = 20 + yardsRemaining
        ## print("Predicted Next Action: " + next_action + " " + str(yardsRemaining))

        ## print("This is disc coordinate: " + str(self.discXCoordinate))

        if (self.discXCoordinate > 110 or self.discXCoordinate < 0):
            ## print("The pull has went out of bounds")
            if (self.goingLeftToRight):
                self.discXCoordinate = 20
            else:
                self.discXCoordinate = 90
            
            ## print("This is disc coordinate: " + str(self.discXCoordinate))
        
        return next_action, yardsRemaining
    
    ## Each action will gain some yards. This function updates the x-coordinate for the yards gained for each action.
    def updateYardsAndAction(self, next_action, yardsGainedForAction, yardsRemaining):
        turnover = False
        ## If the action is a turnover, add yards and change possession
        if next_action in ["Block", "Dropped pass", "Dropped huck", "Stall", "Huck Throwaway", "Throwaway"]:
            if (self.goingLeftToRight):
                self.discXCoordinate += yardsGainedForAction
                yardsRemaining = self.discXCoordinate - 20
            else:
                self.discXCoordinate -= yardsGainedForAction
                yardsRemaining = 90 - self.discXCoordinate
            self.goingLeftToRight = not self.goingLeftToRight

            turnover = True

        ## If the action is a dump, we have to lose yards.
        elif next_action == "Dump":
            if (self.goingLeftToRight):
                self.discXCoordinate -= yardsGainedForAction
                yardsRemaining = 90 - self.discXCoordinate
            else:
                self.discXCoordinate += yardsGainedForAction
                yardsRemaining = self.discXCoordinate - 20
        
        ## All other actions, add yards.
        else:
            if (self.goingLeftToRight):
                self.discXCoordinate += yardsGainedForAction
                yardsRemaining = 90 - self.discXCoordinate
            else:
                self.discXCoordinate -= yardsGainedForAction
                yardsRemaining = self.discXCoordinate - 20
        
        return turnover, yardsRemaining
    
    ## If offense turns the disc over in their own endzone, the defense gets to bring it to the front line.
    ## If offense scores in the opponent's endzone, it is a score.
    def discInEndzone(self, next_action, yardsGainedForAction, catcher, thrower, defender):
        isScore = False
        if (self.goingLeftToRight):
            if self.discXCoordinate > 90:
                ## If there is a turnover in the endzone, bring it back to the endzone line.
                if next_action in ["Block", "Dropped pass", "Dropped huck", "Stall", "Huck Throwaway", "Throwaway"]:
                    self.discXCoordinate = 90
                    
                ## If there is a score in the endzone, plus team on offense point by 1
                else:
                    self.pointScored = True

                    catcher, thrower, defender = self.choosePlayerForAction(next_action, catcher, thrower, defender)

                    ## print(str(yardsGainedForAction) + " " + next_action + " from " + thrower.name + " to " + catcher.name)
                    ## print("This is disc coordinate: " + str(self.discXCoordinate))
                    ## print("We have scored")
                    
                    isScore = True
        else:
            if self.discXCoordinate < 20:
                if next_action in ["Block", "Dropped pass", "Dropped huck", "Stall", "Huck Throwaway", "Throwaway"]:
                    self.discXCoordinate = 20
                else:

                    self.pointScored = True
                    catcher, thrower, defender = self.choosePlayerForAction(next_action, catcher, thrower, defender)

                    ## print(str(yardsGainedForAction) + " " + next_action + " from " + thrower.name + " to " + catcher.name)
                    ## print("This is disc coordinate: " + str(self.discXCoordinate))
                    ## print("We have scored")
                    
                    isScore = True
        
        return catcher, thrower, defender, isScore
    
    ## If there is a turnover, change the offense and defense.
    ## If no turnover, continue play but make the person who caught it the thrower now.
    def changeOffense(self, next_action, yardsGainedForAction, catcher, thrower, defender, turnover):
        if (turnover):

                catcher, thrower, defender = self.choosePlayerForAction(next_action, catcher, thrower, defender)
                # if next_action in ["Block", "Stall"]:
                    
                #     ## print(str(yardsGainedForAction) + " " + next_action + " from " + defender.name)
                # else:
                #     if (catcher == None):
                #         ## print(str(yardsGainedForAction) + " " + next_action + " from " + thrower.name)
                #     else:
                #         continue
                #         ## print(str(yardsGainedForAction) + " " + next_action + " from " + thrower.name + " to " + catcher.name)

                if (self.teamOnOffense == team1):
                    ## print("Team One Turnover")
                    ## print("Team Two On Offense")
                    self.teamOnOffense = team2
                    self.teamOnDefense = team1
                else:
                    ## print("Team Two Turnover")
                    ## print("Team One On Offense")
                    self.teamOnOffense = team1
                    self.teamOnDefense = team2
                
                thrower = None
                catcher = None
                defender = None
            
        else: 

            catcher, thrower, defender = self.choosePlayerForAction(next_action, catcher, thrower, defender)

            ## print(str(yardsGainedForAction) + " " + next_action + " from " + thrower.name + " to " + catcher.name)

            thrower = catcher

            ## print("This is disc coordinate: " + str(self.discXCoordinate))
        
        return catcher, thrower, defender

    
    def runFrisbeeGame(self):

        thrower = None
        catcher = None
        defender = None

        while (catcher != thrower):
            catcher = self.teamOnOffense.roster[random.randint(0,6)]

        ## First Action of a frisbee game is to pull

        next_action, yardsRemaining = self.startWithPull()

        while ("Score" != next_action):

            next_action = self.predict_next_action_markov(next_action, yardsRemaining)
            yardsGainedForAction = self.randomYardsForAction(next_action)

            turnover, yardsRemaining = self.updateYardsAndAction(next_action, yardsGainedForAction, yardsRemaining)

            catcher, thrower, defender, isScore = self.discInEndzone(next_action, yardsGainedForAction, catcher, thrower, defender)


            if (isScore):
                break

            catcher, thrower, defender = self.changeOffense(next_action, yardsGainedForAction, catcher, thrower, defender, turnover)  


    
    def choosePlayerForAction(self, action, catcher, thrower, defender):
        if (catcher == None and thrower == None and defender == None):
            defender = self.teamOnDefense.roster[random.randint(0,6)]
            thrower = self.teamOnOffense.roster[random.randint(0,6)]
            catcher = self.teamOnOffense.roster[random.randint(0,6)]
        else:
            if action in ["Block", "Stall"]:
                defender = self.teamOnDefense.roster[random.randint(0,6)]
                defender.addBlock()
            elif action in ["Dropped pass", "Dropped huck"]:

                catcher = self.teamOnOffense.roster[random.randint(0,6)]

                while (catcher == thrower):
                    catcher = self.teamOnOffense.roster[random.randint(0,6)]

                thrower.addTurnover()
                catcher.addDrop()

            elif action in ["Swing", "Dump", "Pass", "Huck", "Score", "Dish"]:

                catcher = self.teamOnOffense.roster[random.randint(0,6)]

                while (catcher == thrower):
                    catcher = self.teamOnOffense.roster[random.randint(0,6)]

                if (self.pointScored):
                    thrower.addAssist()
                    catcher.addScore()

            elif action in ["Huck Throwaway", "Throwaway"]:
        
                thrower.addTurnover()
                catcher = None

            elif action in ["Pull"]:
                thrower = self.teamOnDefense.roster[random.randint(0,6)]

                thrower.addPull()
            
        return catcher, thrower, defender

    
    def main(self):
        
        self.teamOnOffense = team1
        self.teamOnDefense = team2

        counter = 0
        while (counter < 100):
            while (self.team1.numberOfPoints < 15 and self.team2.numberOfPoints < 15):
                self.runFrisbeeGame()
                if (self.pointScored):
                    self.pointScored = False

                    if (self.teamOnOffense == team1):
                        ## ## print("Team One Scored")
                        self.team1.numberOfPoints += 1
                        self.teamOnOffense = team2
                        self.teamOnDefense = team1
                    else:
                        ## ## print("Team Two Scored")
                        self.team2.numberOfPoints += 1
                        self.teamOnOffense = team1
                        self.teamOnDefense = team2
            
            print ("Team One : Team Two " + str(self.team1.numberOfPoints) + " - " + str(self.team2.numberOfPoints))
            counter += 1
            self.teamOnOffense = team1
            self.teamOnDefense = team2
            self.team1.numberOfPoints = 0
            self.team2.numberOfPoints = 0
            
            # print ("Team One : Team Two " + str(self.team1.numberOfPoints) + " - " + str(self.team2.numberOfPoints))
        
        
        # for player in self.teamOnOffense.roster:
        #     ## ## print(player.name + ": ", end = "")
        #     ## ## print(player.statsDictionary)
        
        # for player in self.teamOnDefense.roster:
        #     ## ## print(player.name + ": ", end = "")
        #     ## ## print(player.statsDictionary)
    


team1 = Team("FirstTeam", 0, 0)
team2 = Team("SecondTeam", 1, 7)
sim = Simulation(team1, team2)
sim.main()