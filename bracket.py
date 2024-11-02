class Bracket:
    
    ## TO DO: FOR THE 1,16 and 1,20 bracket, I need to do the 9th 10th game
    ## u.loser vs y.loser for 9/10
    def __init__(self, teams_advancing, numberOfTeams):
        self.bracket_dict = {}

        self.rankings = []

        self.teams_advancing = teams_advancing

        self.numberOfTeams = numberOfTeams

        self.pool_dict = {}

        for element in range(91, 127):
            self.bracket_dict[chr(element)] = BracketNode(chr(element))

        self.order_of_games_played_bracket = {(1,8) : 'abcdefghijkl',
                                              (2,8) : 'abdecfghijk',
                                              (4,8) : 'abdecfgh',
                                              (6,8) : 'abcdefghijklm',
                                              (1,10) : 'abcdefghijklm',
                                              (2,10) : 'abdecfghijkl',
                                              (4,10) : 'abdecfghi',
                                              (6,10) : 'abcdefghijk',
                                              (1,12) : 'abcdefghijklmnopq',
                                              (2,12) : 'abcdefghijklm',
                                              (4,12) : 'abdecfghijklm',
                                              (6,12) : 'abcdefghijklmnopq',
                                              (1,16): 'abcdefghijklmnopqrstuvwxyz{|}~[',
                                              (1,20) : "abcdefghijklmnopqrstuvwxyz{|}~[]^_`"}

        self.round_letters = {
            (1, 8) :  {1: ["ABCD", "EF", "G"], 3: ["K"], 5: ["HI", "J"], 7: ["L"]},
            (2, 8) : {1: ["AB", "C"], 2: ["DE", "FG", "H", "I"], 5: ["J"], 7: ["K"],},
            (4, 8) : {1: ["A"], 2: ["B", "C"], 4: ["DE", "F", "G"], 7: ["H"]},
            (6, 8) : {1: ["AB", "CD", "E"], 2: ["F", "G"], 4: ["HI", "J", "K"], 6: ["L", "M"]},
            (1, 10) : {1: ['ABCD', "EF", "G"], 3: ["K"], 5: ["HI", "J"], 7: ["L"], 9: ["M"]},
            (2, 10) : {1: ["AB", "C"], 2: ["DE", "FG", "H", "I"], 5: ["J"], 7: ["K"], 9: ["L"]},
            (4, 10) : {1: ["A"], 2: ["B", "C"], 4: ["DE", "F", "G"], 7: ["H"], 9: ["I"]},
            (6, 10) : {1: ["AB", "C"], 2: ["D", "E"], 5: ["F"], 6: ["GH", "I", "J"], 9: ["K"]},
            (1, 12) : {1: ['ABCD', "EF", "G"], 3: ["K"], 5: ["HI", "J"], 7: ["L"], 9: ["MN", "O"], 10: ["P", "Q"]},
            (2, 12) : {1: ["A"], 2: ["BC", "D", "E"], 5: ["F"], 7: ["GH", "IJ", "K"], 9: ["L"], 11: ["M"]},
            (4, 12) : {1: ["A"], 2: ["B", "C"], 4: ["DE", "F", "G"], 7: ["H"], 9: ["IJ", "K"], 10:["L", "M"]},
            (6, 12) : {1: ['AB', "C"], 2: ["D", "E"], 4: ["GH", "I", "F"], 6: ["JK", "LM", "N"], 9: ["O"], 11: ["P"]},
            (1, 16) : {1: ["ABCD", "EFGH", "IJ", "K"], -1: ["PQ"], 3: ["L"], 5: ["MN", "O"], 7: ["RSVW", "TX", "UY", "Z"], 11:["{"], 13:["|}", "~"], 15: ["["]},
            (1, 20) : {1: ["ABCD", "EFGH", "IJ", "K"], -1: ["PQ"], 3: ["L"], 5: ["MN", "O"], 7: ["RSVW", "TX", "UY", "Z"], 11:["{"], 13:["|}", "~"], 15: ["["], 17:["]^", "_"], 19: ["`"]}
        }
        

    def create_bracket(self, pool_teams, update_bracket):

        if update_bracket:
            row = 0
            for pool in pool_teams:
                counter = 0
                for team in pool:
                    self.pool_dict.update({(row, counter): pool_teams[row][counter][0]})
                    counter += 1
                row += 1

        ## Bracket 8.1
        if (self.teams_advancing == 1 and self.numberOfTeams == 8):
            if update_bracket:
                self.bracket_dict['a'].add_team(self.pool_dict[(0,0)], self.pool_dict[(1,3)])
                self.bracket_dict['b'].add_team(self.pool_dict[(1,1)], self.pool_dict[(0,2)])
                self.bracket_dict['c'].add_team(self.pool_dict[(0,1)], self.pool_dict[(1,2)])
                self.bracket_dict['d'].add_team(self.pool_dict[(1,0)], self.pool_dict[(0,3)])
            else:
                self.bracket_dict['e'].add_team(self.bracket_dict['a'].winner, self.bracket_dict['b'].winner)
                self.bracket_dict['f'].add_team(self.bracket_dict['c'].winner, self.bracket_dict['d'].winner)
                self.bracket_dict['g'].add_team(self.bracket_dict['e'].winner, self.bracket_dict['f'].winner)
                self.bracket_dict['h'].add_team(self.bracket_dict['a'].loser, self.bracket_dict['b'].loser)
                self.bracket_dict['i'].add_team(self.bracket_dict['c'].loser, self.bracket_dict['d'].loser)
                self.bracket_dict['j'].add_team(self.bracket_dict['h'].winner, self.bracket_dict['i'].winner)
                self.bracket_dict['k'].add_team(self.bracket_dict['e'].loser, self.bracket_dict['f'].loser)
                self.bracket_dict['l'].add_team(self.bracket_dict['h'].loser, self.bracket_dict['i'].loser)

        ## Bracket 8.2.1
        elif (self.teams_advancing == 2 and self.numberOfTeams == 8):
            if update_bracket:
                self.bracket_dict['a'].add_team(self.pool_dict[(0,0)], self.pool_dict[(1,1)])
                self.bracket_dict['b'].add_team(self.pool_dict[(0,1)], self.pool_dict[(1,0)])
                self.bracket_dict['d'].add_team(self.pool_dict[(0,2)], self.pool_dict[(1,3)])
                self.bracket_dict['e'].add_team(self.pool_dict[(0,3)], self.pool_dict[(1,2)])
            else:
                self.bracket_dict['c'].add_team(self.bracket_dict['a'].winner, self.bracket_dict['b'].winner)
                self.bracket_dict['f'].add_team(self.bracket_dict['a'].loser, self.bracket_dict['d'].winner)
                self.bracket_dict['g'].add_team(self.bracket_dict['b'].loser, self.bracket_dict['e'].winner)
                self.bracket_dict['h'].add_team(self.bracket_dict['f'].winner, self.bracket_dict['g'].winner)
                self.bracket_dict['i'].add_team(self.bracket_dict['c'].loser, self.bracket_dict['h'].winner)
                self.bracket_dict['j'].add_team(self.bracket_dict['d'].loser, self.bracket_dict['e'].loser)
                self.bracket_dict['k'].add_team(self.bracket_dict['f'].loser, self.bracket_dict['g'].loser)
        
        ## Bracket 8.4
        elif (self.teams_advancing == 4 and self.numberOfTeams == 8):
            if update_bracket:
                self.bracket_dict['a'].add_team(self.pool_dict[(0,0)], self.pool_dict[(1,0)])
                self.bracket_dict['b'].add_team(self.pool_dict[(0,1)], self.pool_dict[(1,1)])
                self.bracket_dict['d'].add_team(self.pool_dict[(0,2)], self.pool_dict[(1,3)])
                self.bracket_dict['e'].add_team(self.pool_dict[(0,3)], self.pool_dict[(1,2)])
            else:
                self.bracket_dict['c'].add_team(self.bracket_dict['a'].loser, self.bracket_dict['b'].winner)
                self.bracket_dict['f'].add_team(self.bracket_dict['d'].winner, self.bracket_dict['e'].winner)
                self.bracket_dict['g'].add_team(self.bracket_dict['f'].winner, self.bracket_dict['b'].loser)
                self.bracket_dict['h'].add_team(self.bracket_dict['d'].loser, self.bracket_dict['e'].loser)
        
        ## Bracket 8.5
        elif self.teams_advancing == 6 and self.numberOfTeams == 8:
            if update_bracket:
                self.bracket_dict['a'].add_team(self.pool_dict[(0,2)], self.pool_dict[(1,1)])
                self.bracket_dict['b'].add_team(self.pool_dict[(0,1)], self.pool_dict[(1,2)])
            else:
                self.bracket_dict['c'].add_team(self.pool_dict[(0,0)], self.bracket_dict['a'].winner)
                self.bracket_dict['d'].add_team(self.pool_dict[(1,0)], self.bracket_dict['b'].winner)

                self.bracket_dict['e'].add_team(self.bracket_dict['c'].winner, self.bracket_dict['d'].winner)
                self.bracket_dict['f'].add_team(self.bracket_dict['c'].loser, self.bracket_dict['d'].loser)
                self.bracket_dict['g'].add_team(self.bracket_dict['e'].loser, self.bracket_dict['f'].winner)
                self.bracket_dict['h'].add_team(self.bracket_dict['a'].loser, self.pool_dict[(1,3)])
                self.bracket_dict['i'].add_team(self.bracket_dict['b'].loser, self.pool_dict[(0,3)])

                self.bracket_dict['j'].add_team(self.bracket_dict['h'].winner, self.bracket_dict['i'].winner)
                self.bracket_dict['k'].add_team(self.bracket_dict['f'].loser, self.bracket_dict['j'].winner)

                self.bracket_dict['l'].add_team(self.bracket_dict['h'].loser, self.bracket_dict['i'].loser)
                self.bracket_dict['m'].add_team(self.bracket_dict['j'].loser, self.bracket_dict['l'].winner)
        
        ## Bracket 8.1 but added the fifth-place pool losers to determine 10th place
        elif (self.teams_advancing == 1 and self.numberOfTeams == 10):
            if update_bracket:
                self.bracket_dict['a'].add_team(self.pool_dict[(0,0)], self.pool_dict[(1,3)])
                self.bracket_dict['b'].add_team(self.pool_dict[(1,1)], self.pool_dict[(0,2)])
                self.bracket_dict['c'].add_team(self.pool_dict[(0,1)], self.pool_dict[(1,2)])
                self.bracket_dict['d'].add_team(self.pool_dict[(1,0)], self.pool_dict[(0,3)])
                self.bracket_dict['m'].add_team(self.pool_dict[(0,4)], self.pool_dict[(1,4)])
            else:
                self.bracket_dict['e'].add_team(self.bracket_dict['a'].winner, self.bracket_dict['b'].winner)
                self.bracket_dict['f'].add_team(self.bracket_dict['c'].winner, self.bracket_dict['d'].winner)
                self.bracket_dict['g'].add_team(self.bracket_dict['e'].winner, self.bracket_dict['f'].winner)
                self.bracket_dict['h'].add_team(self.bracket_dict['a'].loser, self.bracket_dict['b'].loser)
                self.bracket_dict['i'].add_team(self.bracket_dict['c'].loser, self.bracket_dict['d'].loser)
                self.bracket_dict['j'].add_team(self.bracket_dict['h'].winner, self.bracket_dict['i'].winner)
                self.bracket_dict['k'].add_team(self.bracket_dict['e'].loser, self.bracket_dict['f'].loser)
                self.bracket_dict['l'].add_team(self.bracket_dict['h'].loser, self.bracket_dict['i'].loser)
        
        ## Bracket 8.2.1
        elif (self.teams_advancing == 2 and self.numberOfTeams == 10):
            if update_bracket:
                self.bracket_dict['a'].add_team(self.pool_dict[(0,0)], self.pool_dict[(1,1)])
                self.bracket_dict['b'].add_team(self.pool_dict[(0,1)], self.pool_dict[(1,0)])
                self.bracket_dict['d'].add_team(self.pool_dict[(0,2)], self.pool_dict[(1,3)])
                self.bracket_dict['e'].add_team(self.pool_dict[(0,3)], self.pool_dict[(1,2)])
                self.bracket_dict['l'].add_team(self.pool_dict[(0,4)], self.pool_dict[(1,4)])
            else:
                self.bracket_dict['c'].add_team(self.bracket_dict['a'].winner, self.bracket_dict['b'].winner)
                self.bracket_dict['f'].add_team(self.bracket_dict['a'].loser, self.bracket_dict['d'].winner)
                self.bracket_dict['g'].add_team(self.bracket_dict['b'].loser, self.bracket_dict['e'].winner)
                self.bracket_dict['h'].add_team(self.bracket_dict['f'].winner, self.bracket_dict['g'].winner)
                self.bracket_dict['i'].add_team(self.bracket_dict['c'].loser, self.bracket_dict['h'].winner)
                self.bracket_dict['j'].add_team(self.bracket_dict['d'].loser, self.bracket_dict['e'].loser)
                self.bracket_dict['k'].add_team(self.bracket_dict['f'].loser, self.bracket_dict['g'].loser)

        ## Bracket 8.4
        elif (self.teams_advancing == 4 and self.numberOfTeams == 10):
            if update_bracket:
                self.bracket_dict['a'].add_team(self.pool_dict[(0,0)], self.pool_dict[(1,0)])
                self.bracket_dict['b'].add_team(self.pool_dict[(0,1)], self.pool_dict[(1,1)])
                self.bracket_dict['d'].add_team(self.pool_dict[(0,2)], self.pool_dict[(1,3)])
                self.bracket_dict['e'].add_team(self.pool_dict[(0,3)], self.pool_dict[(1,2)])
                self.bracket_dict['i'].add_team(self.pool_dict[(0,4)], self.pool_dict[(1,4)])
            else:
                self.bracket_dict['c'].add_team(self.bracket_dict['a'].loser, self.bracket_dict['b'].winner)
                self.bracket_dict['f'].add_team(self.bracket_dict['d'].winner, self.bracket_dict['e'].winner)
                self.bracket_dict['g'].add_team(self.bracket_dict['f'].winner, self.bracket_dict['b'].loser)
                self.bracket_dict['h'].add_team(self.bracket_dict['d'].loser, self.bracket_dict['e'].loser)
        
        ## Bracket 4.2.2 for the top 2 teams in each pool. Bracket 6.2 for the bottom 3 to determine 2 winners
        elif (self.teams_advancing == 6 and self.numberOfTeams == 10):
            if update_bracket:
                self.bracket_dict['a'].add_team(self.pool_dict[(0,0)], self.pool_dict[(1,1)])
                self.bracket_dict['b'].add_team(self.pool_dict[(1,0)], self.pool_dict[(0,1)])
                self.bracket_dict['f'].add_team(self.pool_dict[(0,2)], self.pool_dict[(1,2)])
                self.bracket_dict['g'].add_team(self.pool_dict[(0,3)], self.pool_dict[(1,4)])
                self.bracket_dict['h'].add_team(self.pool_dict[(1,3)], self.pool_dict[(0,4)])
            else:
                self.bracket_dict['c'].add_team(self.bracket_dict['a'].winner, self.bracket_dict['b'].winner)
                self.bracket_dict['d'].add_team(self.bracket_dict['a'].loser, self.bracket_dict['b'].loser)
                self.bracket_dict['e'].add_team(self.bracket_dict['c'].loser, self.bracket_dict['d'].winner)
                self.bracket_dict['i'].add_team(self.bracket_dict['g'].winner, self.bracket_dict['h'].winner)
                self.bracket_dict['j'].add_team(self.bracket_dict['f'].loser, self.bracket_dict['d'].winner)
                self.bracket_dict['k'].add_team(self.bracket_dict['g'].loser, self.bracket_dict['h'].loser)
        
        ## Bracket 8.1 for the top 4 teams in each pool. Bracket 4.2.2 for the bottom 2 teams in each pool
        elif (self.teams_advancing == 1 and self.numberOfTeams == 12):
            if update_bracket:
                self.bracket_dict['a'].add_team(self.pool_dict[(0,0)], self.pool_dict[(1,3)])
                self.bracket_dict['b'].add_team(self.pool_dict[(1,1)], self.pool_dict[(0,2)])
                self.bracket_dict['c'].add_team(self.pool_dict[(0,1)], self.pool_dict[(1,2)])
                self.bracket_dict['d'].add_team(self.pool_dict[(1,0)], self.pool_dict[(0,3)])
                self.bracket_dict['m'].add_team(self.pool_dict[(0,4)], self.pool_dict[(1,5)])
                self.bracket_dict['n'].add_team(self.pool_dict[(1,4)], self.pool_dict[(0,5)])
            else:
                self.bracket_dict['e'].add_team(self.bracket_dict['a'].winner, self.bracket_dict['b'].winner)
                self.bracket_dict['f'].add_team(self.bracket_dict['c'].winner, self.bracket_dict['d'].winner)
                self.bracket_dict['g'].add_team(self.bracket_dict['e'].winner, self.bracket_dict['f'].winner)
                self.bracket_dict['h'].add_team(self.bracket_dict['a'].loser, self.bracket_dict['b'].loser)
                self.bracket_dict['i'].add_team(self.bracket_dict['c'].loser, self.bracket_dict['d'].loser)
                self.bracket_dict['j'].add_team(self.bracket_dict['h'].winner, self.bracket_dict['i'].winner)
                self.bracket_dict['k'].add_team(self.bracket_dict['e'].loser, self.bracket_dict['f'].loser)
                self.bracket_dict['l'].add_team(self.bracket_dict['h'].loser, self.bracket_dict['i'].loser)

                self.bracket_dict['o'].add_team(self.bracket_dict['m'].winner, self.bracket_dict['n'].winner)
                self.bracket_dict['p'].add_team(self.bracket_dict['m'].loser, self.bracket_dict['n'].loser)
                self.bracket_dict['q'].add_team(self.bracket_dict['o'].loser, self.bracket_dict['p'].winner)
    
        ## Bracket 6.2 for the top 3 teams. Bracket 6.1.2 for the bottom 3 seeds
        elif (self.teams_advancing == 2 and self.numberOfTeams == 12):
            if update_bracket:
                self.bracket_dict['a'].add_team(self.pool_dict[(0,0)], self.pool_dict[(1,0)])
                self.bracket_dict['b'].add_team(self.pool_dict[(0,1)], self.pool_dict[(1,2)])
                self.bracket_dict['c'].add_team(self.pool_dict[(1,1)], self.pool_dict[(0,2)])
                self.bracket_dict['g'].add_team(self.pool_dict[(0,5)], self.pool_dict[(1,4)])
                self.bracket_dict['h'].add_team(self.pool_dict[(0,4)], self.pool_dict[(1,5)])
            else:
                self.bracket_dict['d'].add_team(self.bracket_dict['b'].winner, self.bracket_dict['c'].winner)
                self.bracket_dict['e'].add_team(self.bracket_dict['a'].loser, self.bracket_dict['d'].winner)

                self.bracket_dict['f'].add_team(self.bracket_dict['b'].loser, self.bracket_dict['c'].loser)

                self.bracket_dict['i'].add_team(self.pool_dict[(0,3)], self.bracket_dict['g'].winner)
                self.bracket_dict['j'].add_team(self.pool_dict[(1,3)], self.bracket_dict['h'].winner)

                self.bracket_dict['k'].add_team(self.bracket_dict['i'].winner, self.bracket_dict['j'].winner)
                self.bracket_dict['l'].add_team(self.bracket_dict['i'].loser, self.bracket_dict['j'].loser)
                self.bracket_dict['m'].add_team(self.bracket_dict['g'].loser, self.bracket_dict['h'].loser)
            
        elif (self.teams_advancing == 4 and self.numberOfTeams == 12):
            if update_bracket:
                self.bracket_dict['a'].add_team(self.pool_dict[(0,0)], self.pool_dict[(1,0)])
                self.bracket_dict['b'].add_team(self.pool_dict[(0,1)], self.pool_dict[(1,1)])
                self.bracket_dict['d'].add_team(self.pool_dict[(0,2)], self.pool_dict[(1,3)])
                self.bracket_dict['e'].add_team(self.pool_dict[(0,3)], self.pool_dict[(1,2)])
                self.bracket_dict['i'].add_team(self.pool_dict[(0,4)], self.pool_dict[(1,5)])
                self.bracket_dict['j'].add_team(self.pool_dict[(1,4)], self.pool_dict[(0,5)])
            else:
                self.bracket_dict['c'].add_team(self.bracket_dict['a'].loser, self.bracket_dict['b'].winner)
                self.bracket_dict['f'].add_team(self.bracket_dict['d'].winner, self.bracket_dict['e'].winner)
                self.bracket_dict['g'].add_team(self.bracket_dict['f'].winner, self.bracket_dict['b'].loser)
                self.bracket_dict['h'].add_team(self.bracket_dict['d'].loser, self.bracket_dict['e'].loser)
                self.bracket_dict['k'].add_team(self.bracket_dict['i'].winner, self.bracket_dict['j'].winner)
                self.bracket_dict['l'].add_team(self.bracket_dict['i'].loser, self.bracket_dict['j'].loser)
                self.bracket_dict['m'].add_team(self.bracket_dict['k'].loser, self.bracket_dict['l'].winner)
    
        elif (self.teams_advancing == 6 and self.numberOfTeams == 12):
            if update_bracket:
                self.bracket_dict['a'].add_team(self.pool_dict[(0,0)], self.pool_dict[(1,1)])
                self.bracket_dict['b'].add_team(self.pool_dict[(1,0)], self.pool_dict[(0,1)])

                self.bracket_dict['g'].add_team(self.pool_dict[(0,2)], self.pool_dict[(1,3)])
                self.bracket_dict['h'].add_team(self.pool_dict[(0,3)], self.pool_dict[(1,2)])

                self.bracket_dict['j'].add_team(self.pool_dict[(0,4)], self.pool_dict[(1,5)])
                self.bracket_dict['k'].add_team(self.pool_dict[(0,5)], self.pool_dict[(1,4)])
            else:
                self.bracket_dict['c'].add_team(self.bracket_dict['a'].winner, self.bracket_dict['b'].winner)
                self.bracket_dict['d'].add_team(self.bracket_dict['a'].loser, self.bracket_dict['b'].loser)
                self.bracket_dict['e'].add_team(self.bracket_dict['c'].loser, self.bracket_dict['d'].winner)

                self.bracket_dict['i'].add_team(self.bracket_dict['g'].winner, self.bracket_dict['h'].winner)

                self.bracket_dict['f'].add_team(self.bracket_dict['d'].loser, self.bracket_dict['i'].winner)

                self.bracket_dict['l'].add_team(self.bracket_dict['j'].winner, self.bracket_dict['g'].loser)
                self.bracket_dict['m'].add_team(self.bracket_dict['h'].loser, self.bracket_dict['k'].winner)

                self.bracket_dict['n'].add_team(self.bracket_dict['l'].winner, self.bracket_dict['m'].winner)

                self.bracket_dict['o'].add_team(self.bracket_dict['l'].loser, self.bracket_dict['m'].loser)

                self.bracket_dict['p'].add_team(self.bracket_dict['j'].loser, self.bracket_dict['k'].loser)

        elif (self.teams_advancing == 1 and self.numberOfTeams == 16):
            if update_bracket:
                self.bracket_dict['a'].add_team(self.pool_dict[(1,1)], self.pool_dict[(2,2)]) ##6ixers, Schwa
                self.bracket_dict['b'].add_team(self.pool_dict[(1,2)], self.pool_dict[(2,1)]) ##Bent Molly
                self.bracket_dict['c'].add_team(self.pool_dict[(0,2)], self.pool_dict[(3,1)]) ##Riot, Traffic
                self.bracket_dict['d'].add_team(self.pool_dict[(0,1)], self.pool_dict[(3,2)]) ##Iris Flipside
                self.bracket_dict['p'].add_team(self.pool_dict[(1,3)], self.pool_dict[(2,3)]) ##Parcha Pop
                self.bracket_dict['q'].add_team(self.pool_dict[(0,3)], self.pool_dict[(3,3)]) ## Nemesis Grit
            else:
                self.bracket_dict['e'].add_team(self.pool_dict[(0,0)], self.bracket_dict['a'].winner) ##Fury, 6xiers
                self.bracket_dict['f'].add_team(self.pool_dict[(3,0)], self.bracket_dict['b'].winner) ##Molly Phoenix
                self.bracket_dict['g'].add_team(self.pool_dict[(2,0)], self.bracket_dict['c'].winner) ##Brute Riot
                self.bracket_dict['h'].add_team(self.pool_dict[(1,0)], self.bracket_dict['d'].winner) ##Flip Scandal
                self.bracket_dict['i'].add_team(self.bracket_dict['e'].winner, self.bracket_dict['f'].winner)
                self.bracket_dict['j'].add_team(self.bracket_dict['g'].winner, self.bracket_dict['h'].winner)
                self.bracket_dict['k'].add_team(self.bracket_dict['i'].winner, self.bracket_dict['j'].winner)

                self.bracket_dict['l'].add_team(self.bracket_dict['i'].loser, self.bracket_dict['j'].loser) ##Molly Brute for 3rd/4th place

                self.bracket_dict['m'].add_team(self.bracket_dict['e'].loser, self.bracket_dict['f'].loser) ##Phoenix 6ixers
                self.bracket_dict['n'].add_team(self.bracket_dict['g'].loser, self.bracket_dict['h'].loser) ##Flipside Riot

                self.bracket_dict['o'].add_team(self.bracket_dict['m'].winner, self.bracket_dict['n'].winner) ##6ixers, Flipside for 5th place, 6th place


                self.bracket_dict['r'].add_team(self.bracket_dict['p'].winner, self.bracket_dict['d'].loser) ##Parcha Iris
                self.bracket_dict['s'].add_team(self.bracket_dict['q'].loser, self.bracket_dict['b'].loser) ##Nemesis BENT

                self.bracket_dict['t'].add_team(self.bracket_dict['r'].winner, self.bracket_dict['s'].winner) ##Iris BENT

                self.bracket_dict['u'].add_team(self.bracket_dict['t'].winner, self.bracket_dict['m'].loser) ##Phoenix Bent loser is 9th

                self.bracket_dict['v'].add_team(self.bracket_dict['c'].loser, self.bracket_dict['q'].winner) ##Traffic Grit
                self.bracket_dict['w'].add_team(self.bracket_dict['a'].loser, self.bracket_dict['p'].loser) ##Pop Schwa

                self.bracket_dict['x'].add_team(self.bracket_dict['v'].winner, self.bracket_dict['w'].winner) ##Traffic Schwa

                self.bracket_dict['y'].add_team(self.bracket_dict['n'].loser, self.bracket_dict['x'].winner) ##Traffic Riot loser is 10th

                self.bracket_dict['z'].add_team(self.bracket_dict['u'].winner, self.bracket_dict['y'].winner) ##for 7th and 8th place

                self.bracket_dict['{'].add_team(self.bracket_dict['t'].loser, self.bracket_dict['x'].loser) ##for 11th and 12th place

                self.bracket_dict['|'].add_team(self.bracket_dict['s'].loser, self.bracket_dict['r'].loser) 

                self.bracket_dict['}'].add_team(self.bracket_dict['v'].loser, self.bracket_dict['w'].loser)

                self.bracket_dict['~'].add_team(self.bracket_dict['|'].winner, self.bracket_dict['}'].winner) ##for 13th 14th place
                    
                self.bracket_dict['['].add_team(self.bracket_dict['|'].loser, self.bracket_dict['}'].loser) ##for 15th 16th place

        
        elif (self.teams_advancing == 1 and self.numberOfTeams == 20):
            if update_bracket:
                self.bracket_dict['a'].add_team(self.pool_dict[(1,1)], self.pool_dict[(2,2)]) ## Oregon Pitt
                self.bracket_dict['b'].add_team(self.pool_dict[(1,2)], self.pool_dict[(2,1)]) ## NC State UMass
                self.bracket_dict['c'].add_team(self.pool_dict[(0,2)], self.pool_dict[(3,1)]) ## Texas Col
                self.bracket_dict['d'].add_team(self.pool_dict[(0,1)], self.pool_dict[(3,2)]) ## Brown Mich
                self.bracket_dict['p'].add_team(self.pool_dict[(1,3)], self.pool_dict[(2,3)])
                self.bracket_dict['q'].add_team(self.pool_dict[(0,3)], self.pool_dict[(3,3)])
                self.bracket_dict[']'].add_team(self.pool_dict[(0,4)], self.pool_dict[(3,4)])
                self.bracket_dict['^'].add_team(self.pool_dict[(1,4)], self.pool_dict[(2,4)])
            else:
                self.bracket_dict['e'].add_team(self.pool_dict[(0,0)], self.bracket_dict['a'].winner) ## UNC Oregon
                self.bracket_dict['f'].add_team(self.pool_dict[(3,0)], self.bracket_dict['b'].winner) ## Cal NC
                self.bracket_dict['g'].add_team(self.pool_dict[(2,0)], self.bracket_dict['c'].winner) ## Col Minnesota
                self.bracket_dict['h'].add_team(self.pool_dict[(1,0)], self.bracket_dict['d'].winner) ## Brown Georgia

                self.bracket_dict['i'].add_team(self.bracket_dict['e'].winner, self.bracket_dict['f'].winner) # UNC Cal
                self.bracket_dict['j'].add_team(self.bracket_dict['g'].winner, self.bracket_dict['h'].winner) # Brown Georgia

                self.bracket_dict['k'].add_team(self.bracket_dict['i'].winner, self.bracket_dict['j'].winner) # UNC Brown for first and second

                self.bracket_dict['l'].add_team(self.bracket_dict['i'].loser, self.bracket_dict['j'].loser) ## Col UNC for 3rd 4th

                self.bracket_dict['m'].add_team(self.bracket_dict['e'].loser, self.bracket_dict['f'].loser) ##Phoenix 6ixers
                self.bracket_dict['n'].add_team(self.bracket_dict['g'].loser, self.bracket_dict['h'].loser) ##Flipside Riot

                self.bracket_dict['o'].add_team(self.bracket_dict['m'].winner, self.bracket_dict['n'].winner) ##6ixers, Flipside for 5th place, 6th place

                self.bracket_dict['r'].add_team(self.bracket_dict['p'].winner, self.bracket_dict['d'].loser) ##Parcha Iris
                self.bracket_dict['s'].add_team(self.bracket_dict['q'].loser, self.bracket_dict['b'].loser) ##Nemesis BENT

                self.bracket_dict['t'].add_team(self.bracket_dict['r'].winner, self.bracket_dict['s'].winner) ##Iris BENT

                self.bracket_dict['u'].add_team(self.bracket_dict['t'].winner, self.bracket_dict['m'].loser) ##Phoenix Bent loser is 9th

                self.bracket_dict['v'].add_team(self.bracket_dict['c'].loser, self.bracket_dict['q'].winner) ##Traffic Grit
                self.bracket_dict['w'].add_team(self.bracket_dict['a'].loser, self.bracket_dict['p'].loser) ##Pop Schwa

                self.bracket_dict['x'].add_team(self.bracket_dict['v'].winner, self.bracket_dict['w'].winner) ##Traffic Schwa

                self.bracket_dict['y'].add_team(self.bracket_dict['n'].loser, self.bracket_dict['x'].winner) ##Traffic Riot loser is 10th

                self.bracket_dict['z'].add_team(self.bracket_dict['u'].winner, self.bracket_dict['y'].winner) ##for 7th and 8th place

                self.bracket_dict['{'].add_team(self.bracket_dict['t'].loser, self.bracket_dict['x'].loser) ##for 11th and 12th place

                self.bracket_dict['|'].add_team(self.bracket_dict['s'].loser, self.bracket_dict['r'].loser) 

                self.bracket_dict['}'].add_team(self.bracket_dict['v'].loser, self.bracket_dict['w'].loser)

                self.bracket_dict['~'].add_team(self.bracket_dict['|'].winner, self.bracket_dict['}'].winner) ##for 13th 14th place
                    
                self.bracket_dict['['].add_team(self.bracket_dict['|'].loser, self.bracket_dict['}'].loser) ##for 15th 16th place

                self.bracket_dict['_'].add_team(self.bracket_dict[']'].winner, self.bracket_dict['^'].winner) ## for 17th 18th place

                self.bracket_dict['`'].add_team(self.bracket_dict[']'].loser, self.bracket_dict['^'].loser) ##for 19th 20th place


    def determine_rankings(self):
        if self.teams_advancing == 1 and self.numberOfTeams == 8:
            self.rankings = [self.bracket_dict['g'].winner, self.bracket_dict['g'].loser, self.bracket_dict['k'].winner,
                    self.bracket_dict['k'].loser, self.bracket_dict['j'].winner, self.bracket_dict['j'].loser,
                    self.bracket_dict['l'].winner, self.bracket_dict['l'].loser]
            
        elif (self.teams_advancing == 2 and self.numberOfTeams == 8):
            self.rankings = [self.bracket_dict['c'].winner, self.bracket_dict['i'].winner, self.bracket_dict['i'].loser,
                    self.bracket_dict['h'].loser, self.bracket_dict['k'].winner, self.bracket_dict['k'].loser,
                    self.bracket_dict['j'].winner, self.bracket_dict['j'].loser]
            
        elif (self.teams_advancing == 4 and self.numberOfTeams == 8):
            self.rankings = [self.bracket_dict['a'].winner, self.bracket_dict['c'].winner, self.bracket_dict['c'].loser,
                    self.bracket_dict['g'].winner, self.bracket_dict['g'].loser, self.bracket_dict['f'].loser,
                    self.bracket_dict['h'].winner, self.bracket_dict['h'].loser]
            
        elif self.teams_advancing == 6 and self.numberOfTeams == 8:
            self.rankings = [self.bracket_dict['e'].winner, self.bracket_dict['g'].winner, self.bracket_dict['g'].loser,
                    self.bracket_dict['k'].winner, self.bracket_dict['k'].loser, self.bracket_dict['m'].winner,
                    self.bracket_dict['m'].loser, self.bracket_dict['l'].loser]
        
        elif self.teams_advancing == 1 and self.numberOfTeams == 10:
            self.rankings = [self.bracket_dict['g'].winner, self.bracket_dict['g'].loser, self.bracket_dict['k'].winner,
                    self.bracket_dict['k'].loser, self.bracket_dict['j'].winner, self.bracket_dict['j'].loser,
                    self.bracket_dict['l'].winner, self.bracket_dict['l'].loser, self.bracket_dict['m'].winner,
                    self.bracket_dict['m'].loser]
        
        elif self.teams_advancing == 2 and self.numberOfTeams == 10:
           self.rankings = [self.bracket_dict['c'].winner, self.bracket_dict['i'].winner, self.bracket_dict['i'].loser,
                    self.bracket_dict['h'].loser, self.bracket_dict['k'].winner, self.bracket_dict['k'].loser,
                    self.bracket_dict['j'].winner, self.bracket_dict['j'].loser, self.bracket_dict['l'].winner,
                    self.bracket_dict['l'].loser]
        
        elif (self.teams_advancing == 4 and self.numberOfTeams == 10):
            self.rankings = [self.bracket_dict['a'].winner, self.bracket_dict['c'].winner, self.bracket_dict['c'].loser,
                    self.bracket_dict['g'].winner, self.bracket_dict['g'].loser, self.bracket_dict['f'].loser,
                    self.bracket_dict['h'].winner, self.bracket_dict['h'].loser, self.bracket_dict['i'].winner,
                    self.bracket_dict['i'].loser]
        
        elif (self.teams_advancing == 6 and self.numberOfTeams == 10):
            self.rankings = [self.bracket_dict['c'].winner, self.bracket_dict['e'].winner, self.bracket_dict['e'].loser,
                    self.bracket_dict['d'].loser, self.bracket_dict['f'].winner, self.bracket_dict['j'].winner,
                    self.bracket_dict['j'].loser. self.bracket_dict['i'].loser, self.bracket_dict['k'].winner,
                    self.bracket_dict['k'].loser]
        
        elif (self.teams_advancing == 1 and self.numberOfTeams == 12):
             self.rankings = [self.bracket_dict['g'].winner, self.bracket_dict['g'].loser, self.bracket_dict['k'].winner,
                    self.bracket_dict['k'].loser, self.bracket_dict['j'].winner, self.bracket_dict['j'].loser,
                    self.bracket_dict['l'].winner, self.bracket_dict['l'].loser, self.bracket_dict['o'].winner, 
                    self.bracket_dict['q'].winner, self.bracket_dict['q'].loser, self.bracket_dict['p'].loser]
             
        elif (self.teams_advancing == 2 and self.numberOfTeams == 12):
             self.rankings = [self.bracket_dict['a'].winner, self.bracket_dict['e'].winner, self.bracket_dict['e'].loser,
                              self.bracket_dict['d'].loser, self.bracket_dict['f'].winner, self.bracket_dict['f'].loser,
                              self.bracket_dict['k'].winner, self.bracket_dict['k'].loser, self.bracket_dict['l'].winner, 
                              self.bracket_dict['l'].loser, self.bracket_dict['m'].winner, self.bracket_dict['m'].loser]
             
        elif (self.teams_advancing == 4 and self.numberOfTeams == 12):
            self.rankings = [self.bracket_dict['a'].winner, self.bracket_dict['c'].winner, self.bracket_dict['c'].loser,
                    self.bracket_dict['g'].winner, self.bracket_dict['g'].loser, self.bracket_dict['f'].loser,
                    self.bracket_dict['h'].winner, self.bracket_dict['h'].loser, self.bracket_dict['k'].winner, 
                    self.bracket_dict['m'].winner, self.bracket_dict['m'].loser, self.bracket_dict['l'].loser]
        
        elif (self.teams_advancing == 6 and self.numberOfTeams == 12):
            self.rankings = [self.bracket_dict['c'].winner, self.bracket_dict['e'].winner, self.bracket_dict['e'].loser,
                             self.bracket_dict['f'].winner, self.bracket_dict['f'].loser, self.bracket_dict['n'].winner, 
                             self.bracket_dict['n'].loser, self.bracket_dict['l'].loser, self.bracket_dict['o'].winner, 
                             self.bracket_dict['o'].loser, self.bracket_dict['p'].winner, self.bracket_dict['p'].loser]
        
        elif (self.numberOfTeams == 16):
            self.rankings = [self.bracket_dict['k'].winner, self.bracket_dict['k'].loser, self.bracket_dict['l'].winner,
                       self.bracket_dict['l'].loser, self.bracket_dict['o'].winner, self.bracket_dict['o'].loser,
                       self.bracket_dict['z'].winner, self.bracket_dict['z'].loser, self.bracket_dict['u'].loser,
                       self.bracket_dict['y'].loser, self.bracket_dict['{'].winner, self.bracket_dict['{'].loser,
                       self.bracket_dict['~'].winner, self.bracket_dict['~'].loser, self.bracket_dict['['].winner,
                       self.bracket_dict['['].loser]
        
        elif (self.numberOfTeams == 20):
            self.rankings = [self.bracket_dict['k'].winner, self.bracket_dict['k'].loser, self.bracket_dict['l'].winner,
                       self.bracket_dict['l'].loser, self.bracket_dict['o'].winner, self.bracket_dict['o'].loser,
                       self.bracket_dict['z'].winner, self.bracket_dict['z'].loser, self.bracket_dict['u'].loser,
                       self.bracket_dict['y'].loser, self.bracket_dict['{'].winner, self.bracket_dict['{'].loser,
                       self.bracket_dict['~'].winner, self.bracket_dict['~'].loser, self.bracket_dict['['].winner,
                       self.bracket_dict['['].loser, self.bracket_dict['_'].winner, self.bracket_dict['_'].loser,
                       self.bracket_dict['`'].winner, self.bracket_dict['`'].loser]

class BracketNode:

    def __init__(self, letter):
        self.winner = None
        self.loser = None
        self.letter = letter
        self.winnerPoints = 0
        self.loserPoints = 0
    
    def add_team(self, team1, team2):
        self.team1 = team1
        self.team2 = team2