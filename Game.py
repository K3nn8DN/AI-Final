"""


AI extends the player class 
    __init__()
    chooseaction() uses choose() to pick actions
    `fit(state, action, reward, next_state)`
    `update_q_value(state, action, reward, next_state)`
    player - ai controlls a player

"""

from enum import Enum
import math


class Actions(Enum):
    Attack = 1
    Heal = 2
    Block = 3


class Elements(Enum):
    Null = 0
    fire = 1
    ice = 2
    water = 3

    def attacks(self,oponent):# how much is it decresed by if self attacks oponent 
        if self == Elements.fire and oponent == Elements.water:
            return 2
        if self == Elements.water and oponent == Elements.ice:
            return 2
        if self == Elements.ice and oponent == Elements.fire:
            return 2
        return 1 
    
    def Print(self):
        if self == Elements.fire:
            return "fire"
        if self == Elements.water:
            return "water"
        if self == Elements.ice:
            return "ice"
        return ""


class Attack_Level(Enum):
    Null = 0
    small = 1
    big = 2

    def damage(self):
        if self == Attack_Level.small:
            return 2
        if self == Attack_Level.big:
            return 4
        return 0 
    
    def energy(self):
        if self == Attack_Level.small:
            return 1
        if self == Attack_Level.big:
            return 3
        return 0 
    def Print(self):
        if self == Attack_Level.small:
            return "low level"
        if self == Attack_Level.big:
            return "high level"
        return "" 





class Game:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.choose()

    def display(self, string):
        if string == "line":
            print('__________________________________')
            print("          ")
            print("          ")

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

        if "Damage" in string:
            p1_health = self.player1.get_health()
            print(f"{self.player1.get_name()} takes {string[2]} damage. Health now {p1_health}.")
            p2_health = self.player2.get_health()
            print(f"{self.player2.get_name()} takes {string[1]} damage. Health now {p2_health}.")
            
            
        

    def choose(self):
        self.display("line")
        print("Choosing actions:")
        self.player1.choose_action()
        self.display("line")
        self.display("line")
        self.display("line")
        self.display("line")
        self.player2.choose_action()
        self.battle()

    def battle(self):
        print("Battle phase!") 
        self.display("line")
        p1_action, p1_element, p1_level, p1_defense = self.player1.get_actions()
        p2_action, p2_element, p2_level, p2_defense = self.player2.get_actions()
        
        if p1_action == Actions.Block:p1_block = p1_element
        else: p1_block = Elements.Null

        if p2_action == Actions.Block:p2_block = p2_element
        else: p2_block = Elements.Null

        self.display("Attacks",)
        

        p1_attack = math.floor(p1_level.damage() / p1_element.attacks(p2_defense)) / p1_element.attacks(p2_block)
        self.player2.take_damage(p1_attack)
        p2_attack = math.floor(p2_level.damage() / p2_element.attacks(p1_defense)) / p2_element.attacks(p1_block)
        self.player1.take_damage(p2_attack)
        attacks= "Damage",p1_attack, p2_attack
        self.display(attacks)
        

        p1_health = self.player1.get_health()
        p2_health= self.player2.get_health()
        if p1_health == 0 and p2_health ==0:
            return print("gameover tie")
        elif p1_health == 0:
            return print("gameover p2 wins")
        elif p2_health == 0:
            return print("gameover p1 wins")
        else:


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

            self.choose()





class Player:
    def __init__(self, name):
        self.name = name
        self.health = 10
        self.energy = 5
        self.action = None,None,None,None
        

    def choose_action(self):
        # Prompt player for their choice of action
        print(f"{self.name}, it's your turn! You have {self.health} health and {self.energy} energy!")
        while True:
            defense_choice = input(f"Choose your defense element (1=fire, 2=ice, 3=water): ")
            if defense_choice in ["1", "2", "3"]:
                break
            print("Invalid element choice! Please choose fire, ice, or water.")
        
        # Choose action: Attack, Heal, or Block
        while True:
            action_choice = input(f"Choose your action (1=Attack, 2=Heal, 3=Block): ")
            if action_choice in ["1", "2", "3"]:
                if action_choice == "1" and self.energy == 0:
                    print("not enough energy")
                else: break
            else: print("Invalid input! Please choose 1, 2, or 3.")

        
        # Choose attack element (fire, ice, water)
        element_choice = 0
        if action_choice != "2":
            while True:
                element_choice = input(f"Choose your attack element (1=fire, 2=ice, 3=water): ")
                if element_choice in ["1", "2", "3"]:
                    break
                print("Invalid element choice! Please choose fire, ice, or water.")

        # Choose attack level
        level_choice = 0
        if action_choice == "1":
            while True:
                level_choice = input(f"Choose your attack level (1=Small, 2=Big): ")
                if level_choice in ["1", "2"]:
                    if level_choice == "2" and self.energy < 3:
                        print("not enough energy")
                    else: break
                else: print("Invalid level! Please choose 1 or 2.")
        
        self.action = Actions(int(action_choice)),Elements(int(element_choice)),Attack_Level(int(level_choice)), Elements(int(defense_choice))


    def take_damage(self, amount):
        self.health = max(0, self.health - amount)
        
    def heal(self):
        self.health = self.health + 1

    def update_energy(self, amount):
        self.energy = min(5, self.energy - amount + 1)

    def get_health(self):
        return self.health

    def get_actions(self):
        return self.action
    
    def get_name(self):
        return self.name
    






class AIPlayer:# make a list of oponents moves and uppdate it in battle phase  
    def __init__(self, name):
        self.player = Player(name)

    def choose_action(self):
        if self.player.energy >= 3:
            action = "Big Attack"
        else:
            action = "Small Attack"
        print(f"{self.player.name} (AI) chooses {action}")
        return action

    def take_damage(self, amount):
        self.player.take_damage(amount)
  
    def heal(self):
        self.player.heal()

    def update_energy(self, amount):
        self.player.update_energy(amount)

    def get_health(self):
        return self.player.get_health()

    def get_actions(self):
        return self.player.get_actions()
    
    def get_name(self):
        return self.player.get_name()










def main():
    print("Game started!")
    ai = AIPlayer("AI Bob")
    player = Player("Bob")
    player2= Player("cat")
    game = Game(player, player2)  


if __name__ == "__main__":
    main()
