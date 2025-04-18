import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from  Enums import Actions, Elements
from Player import  AIPlayer
import math


class WinCount:
    player1_win = 0
    player2_win = 0
    tie = 0

    @classmethod
    def update_wins(cls, a):
        if a == 1:
            cls.player1_win += 1
        elif a == 2:
            cls.player2_win += 1
        elif a == 0:
            cls.tie += 1

    @classmethod
    def return_wins(cls):
        print(f"p1_wins = {cls.player1_win} | p2_wins = {cls.player2_win} | Ties = {cls.tie}")

    @classmethod
    def reset_wins(cls):
        cls.player1_win = 0
        cls.player2_win = 0
        cls.tie = 0



class Game:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2

    def start(self):
        self.player1.reset()
        self.player2.reset()
        self.choose()

    def get_state(self, player):
        if player == self.player1:
            return self.player2.get_state()
        else:
            return self.player1.get_state()

    def is_game_over(self):
        p1_health = self.player1.get_health()
        p2_health= self.player2.get_health()
        if p1_health == 0 and p2_health ==0:
            WinCount.update_wins(0)
            self.player1.fit(50)
            self.player2.fit(50)
            self.player1.save_q_table()
            self.player2.save_q_table()
            return 1
        elif p1_health == 0:
            WinCount.update_wins(2)
            self.player1.fit(-100)
            self.player2.fit(100)
            self.player1.save_q_table()
            self.player2.save_q_table()
            return 1
        elif p2_health == 0:
            WinCount.update_wins(1)
            self.player1.fit(100)
            self.player2.fit(-100)
            self.player1.save_q_table()
            self.player2.save_q_table()
            return 1
        else: return 0

            
        
    def choose(self):
        self.player1.choose_action()
        self.player2.choose_action()
        self.battle()

    def battle(self):
        p1_action, p1_element, p1_level, p1_defense = self.player1.get_actions()
        p2_action, p2_element, p2_level, p2_defense = self.player2.get_actions()
        
        #saves the block type if any
        if p1_action == Actions.Block:p1_block = p1_element
        else: p1_block = Elements.Null
        if p2_action == Actions.Block:p2_block = p2_element
        else: p2_block = Elements.Null

    
        #calculate and inflict damage 
        p1_attack = math.floor(p1_level.damage() / p1_element.attacks(p2_defense)) / p1_element.attacks(p2_block)
        self.player2.take_damage(p1_attack)
        p2_attack = math.floor(p2_level.damage() / p2_element.attacks(p1_defense)) / p2_element.attacks(p1_block)
        self.player1.take_damage(p2_attack)
        
        #get health and check winner
        if self.is_game_over():
            return


        self.player1.update_energy(p1_level.energy())
        self.player2.update_energy(p2_level.energy())

        if p1_action == Actions.Heal:
            self.player1.heal()
            p1_health = self.player1.get_health()
        if p2_action == Actions.Heal:
            self.player2.heal()
            p2_health= self.player2.get_health()

        self.player1.fit(-1)
        self.player2.fit(-1)

        self.choose()


def main():
    ai3 = AIPlayer("nnn", learning_rate=0.1, factor=0.95, epsilon=0.6)  
    ai6 = AIPlayer("fff", learning_rate=0.3, factor=0.88, epsilon=0.4) 
    ai1 = AIPlayer("sss", learning_rate=0.1, factor=0.99, epsilon=0.1)  


    game1 = Game(ai1, ai3)
    game2 = Game(ai1, ai6)
    game3 = Game(ai3, ai6)

    # Play the games
    games = [game1, game2, game3]

    for game in games:
        # Set the game for both players
        game.player1.set_game(game)
        game.player2.set_game(game)
        print(game.player1.get_name() + " vs " + game.player2.get_name())


        # Play 1000 games
        for _ in range(1000):
            game.start()

        # After 1000 games, print the win counts
        WinCount.return_wins()
        WinCount.reset_wins()


if __name__ == "__main__":
    main()
