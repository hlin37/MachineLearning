import random
import numpy as np
from collections import defaultdict

class CFRAgent:
    def __init__(self, num_iterations, deck=[1,2,3,4,5,6,7,8,9,10,11,12,13], num_cards=5):
        self.num_iterations = num_iterations
        self.deck = deck * 4  # Standard deck of cards (4 suits of each value)
        self.num_cards = num_cards

        # Tables to store regret and strategy for each information set
        self.regret_table = defaultdict(lambda: defaultdict(float))
        self.strategy_table = defaultdict(lambda: defaultdict(float))
        self.strategy_sum = defaultdict(lambda: defaultdict(float))

        # Actions: bids (quantity, face value) or challenge
        self.all_actions = self.create_all_actions()
    
    def create_all_actions(self):
        actions = []
        with open("poker_actions.txt", "r") as f:
            for line in f:
                actions.append(line)
        
        f.close()

        return actions
        

    def get_strategy(self, info_set):
        """Get the strategy for the given info set."""
        strategy = self.strategy_table[info_set]
        regret_sum = sum(max(self.regret_table[info_set][action], 0) for action in self.all_actions)

        # Update the strategy based on regret-matching
        if regret_sum > 0:
            for action in self.all_actions:
                strategy[action] = max(self.regret_table[info_set][action], 0) / regret_sum
        else:
            # If no positive regrets, assign uniform probabilities
            num_actions = len(self.all_actions)
            for action in self.all_actions:
                strategy[action] = 1.0 / num_actions

        # Update the strategy sum for averaging
        for action in self.all_actions:
            self.strategy_sum[info_set][action] += strategy[action]

        return strategy

    def choose_action(self, strategy):
        """Select an action based on the strategy probabilities."""
        actions, probabilities = zip(*strategy.items())
        return np.random.choice(actions, p=probabilities)

    def update_regret(self, info_set, action, regret):
        """Update the regret for a specific action in an information set."""
        self.regret_table[info_set][action] += regret

    def average_strategy(self, info_set):
        """Compute the average strategy across all iterations."""
        avg_strategy = self.strategy_sum[info_set]
        total_sum = sum(avg_strategy.values())

        if total_sum > 0:
            for action in avg_strategy:
                avg_strategy[action] /= total_sum
        else:
            num_actions = len(self.all_actions)
            for action in avg_strategy:
                avg_strategy[action] = 1.0 / num_actions

        return avg_strategy

    def get_info_set(self, hand, current_bid, history):
        """Construct an information set based on the hand, current bid, and history."""
        return (tuple(sorted(hand)), current_bid, tuple(history))

    def calculate_regret(self, player_hand, opponent_hand, current_bid, action):
        """Calculate the counterfactual regret for a given action."""
        # For a challenge action, calculate regret based on whether the opponent's bid is true
        if action == 'challenge':
            count_in_hands = player_hand.count(current_bid[1]) + opponent_hand.count(current_bid[1])
            if count_in_hands >= current_bid[0]:
                return -1  # Challenger loses
            else:
                return 1  # Challenger wins
        else:
            # Regret for bidding is complex; we simplify here for now
            return 0

    def resolve_challenge(self, challenger_hand, opponent_hand, current_bid):
        """Resolve a challenge action."""
        count_in_hands = challenger_hand.count(current_bid[1]) + opponent_hand.count(current_bid[1])
        if count_in_hands >= current_bid[0]:
            return "Lose Challenge"
        else:
            return "Win Challenge"

    def play_game(self):
        """Simulate a game of Liar's Poker using CFR between two agents."""
        random.shuffle(self.deck)
        player_hand = random.sample(self.deck, self.num_cards)
        opponent_hand = random.sample(self.deck, self.num_cards)

        current_bid = None
        history = []
        player_turn = True  # Track whose turn it is

        while True:
            if player_turn:
                info_set = self.get_info_set(player_hand, current_bid, history)
                strategy = self.get_strategy(info_set)
                action = self.choose_action(strategy)
                history.append(action)

                if action == 'challenge':
                    self.resolve_challenge(player_hand, opponent_hand, current_bid)
                    break
                else:
                    current_bid = action
            else:
                info_set = self.get_info_set(opponent_hand, current_bid, history)
                strategy = self.get_strategy(info_set)
                action = self.choose_action(strategy)
                history.append(action)

                if action == 'challenge':
                    self.resolve_challenge(opponent_hand, player_hand, current_bid)
                    break
                else:
                    current_bid = action

            player_turn = not player_turn

    def cfr(self, player_hand, opponent_hand, current_bid, history, iteration, player_turn=True):
        """Recursive CFR algorithm for regret minimization."""
        info_set = self.get_info_set(player_hand, current_bid, history)
        strategy = self.get_strategy(info_set)

        if player_turn:
            # Player's turn to act
            for action in self.all_actions:
                regret = self.calculate_regret(player_hand, opponent_hand, current_bid, action)
                self.update_regret(info_set, action, regret)

        else:
            # Opponent's turn to act
            for action in self.all_actions:
                regret = self.calculate_regret(opponent_hand, player_hand, current_bid, action)
                self.update_regret(info_set, action, regret)

    def train(self):
        """Train the CFR agent over multiple iterations."""
        for iteration in range(self.num_iterations):
            # Randomly generate hands for both players
            random.shuffle(self.deck)
            player_hand = random.sample(self.deck, self.num_cards)
            opponent_hand = random.sample(self.deck, self.num_cards)

            # Start the game with an empty history
            self.play_game()

# Example Usage
if __name__ == "__main__":
    agent = CFRAgent(num_iterations=10000)
    agent.train()
    print("Training complete. CFR agent ready.")
