from Enums import Actions, Elements
from Player import Player, AIPlayer
import math


class Game:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2

    def start(self):
        self.choose()

    def get_state(self, player):
        if player == self.player1:
            return self.player2.get_state()
        else:
            return self.player1.get_state()

    def display(self, string):
        if string == "line":
            print('__________________________________')
            print("          ")
            print("          ")

        #print what attacks and blocks were used
        if string == "Attacks":
            p1_action, p1_element, p1_level, p1_defense = self.player1.get_actions()
            p2_action, p2_element, p2_level, p2_defense = self.player2.get_actions()

            if p1_action == Actions.Attack:
                print(f"{self.player1.get_name()} attacks with a {p1_level.Print()} {p1_element.Print()} attack")
                if p2_action == Actions.Block: 
                    if p2_element == p2_defense:
                        print(f"{self.player2.get_name()} defends with a double {p2_element.Print()} Block")
                    else:
                        print(f"{self.player2.get_name()} defends with a {p2_element.Print()} and {p2_defense.Print()} Block")
                else:
                    print(f"{self.player2.get_name()} defends with a {p2_defense.Print()} defense")

            if p2_action == Actions.Attack:
                print(f"{self.player2.get_name()} attacks with a {p2_level.Print()} {p2_element.Print()} attack")
                if p1_action == Actions.Block: 
                    if p1_element == p1_defense:
                        print(f"{self.player1.get_name()} defends with a double {p1_element.Print()} Block")
                    else:
                        print(f"{self.player1.get_name()} defends with a {p1_element.Print()} and {p1_defense.Print()} Block")
                else:
                    print(f"{self.player1.get_name()} defends with a {p1_defense.Print()} defense")

        #prints the damage both players take after the attacks
        if "Damage" in string:
            p1_health = self.player1.get_health()
            print(f"{self.player1.get_name()} takes {string[2]} damage. Health now {p1_health}.")
            p2_health = self.player2.get_health()
            print(f"{self.player2.get_name()} takes {string[1]} damage. Health now {p2_health}.")

    def is_game_over(self):
        p1_health = self.player1.get_health()
        p2_health= self.player2.get_health()
        if p1_health == 0 and p2_health ==0:
            print("gameover tie")
            return 1
        elif p1_health == 0:
            print("gameover p2 wins")
            return 1
        elif p2_health == 0:
            print("gameover p1 wins")
            return 1
        else: return 0

            
        
    def choose(self):
        self.display("line")
        print("Choosing actions:")
        self.player1.choose_action()
        self.display("line")
        self.player2.choose_action()
        self.battle()

    def battle(self):
        print("Battle phase!") 
        self.display("line")
        p1_action, p1_element, p1_level, p1_defense = self.player1.get_actions()
        p2_action, p2_element, p2_level, p2_defense = self.player2.get_actions()
        
        #saves the block type if any
        if p1_action == Actions.Block:p1_block = p1_element
        else: p1_block = Elements.Null
        if p2_action == Actions.Block:p2_block = p2_element
        else: p2_block = Elements.Null

        self.display("Attacks")
    
        #calculate and inflict damage 
        p1_attack = math.floor(p1_level.damage() / p1_element.attacks(p2_defense)) / p1_element.attacks(p2_block)
        self.player2.take_damage(p1_attack)
        p2_attack = math.floor(p2_level.damage() / p2_element.attacks(p1_defense)) / p2_element.attacks(p1_block)
        self.player1.take_damage(p2_attack)

        attacks= "Damage",p1_attack, p2_attack
        self.display(attacks)
        
        #get health and check winner
        if self.is_game_over():
            return


        self.player1.update_energy(p1_level.energy())
        self.player2.update_energy(p2_level.energy())

        if p1_action == Actions.Heal:
            self.player1.heal()
            p1_health = self.player1.get_health()
            print(f"{self.player1.get_name()} heals. Health now {p1_health}.")
        if p2_action == Actions.Heal:
            self.player2.heal()
            p2_health= self.player2.get_health()
            print(f"{self.player2.get_name()} heals. Health now {p2_health}.")

        #self.player1.fit()
        #self.player2.fit()

        self.choose()







def main():
    print("Game started!")
    ai = AIPlayer("AI Bob")
    ai2 = AIPlayer("AI cat")
    player = Player("Bob")
    player2= Player("cat")
    game = Game(ai, ai2)  
    ai.set_game(game)
    ai2.set_game(game)
    game.start()


if __name__ == "__main__":
    main()
