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
        for _ in range(4): self.display("line")
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
        self.health = min(10, self.health + 2)

    def update_energy(self, amount):
        self.energy = min(5, self.energy - amount + 1)

    def get_health(self):
        return self.health
    
    def get_state(self):
        return self.health, self.energy

    def get_actions(self):
        return self.action
    
    def get_name(self):
        return self.name
    
    def fit():
        None
    



import numpy as np
class AIPlayer:# make a list of oponents moves and uppdate it in battle phase  
    def __init__(self, name, learning_rate=0.1, factor=0.95, epsilon=0.1):
        self.player = Player(name)
        self.state_size = 4356
        self.action_size=30
        self.q_table = {}
        self.learning_rate=learning_rate
        self.factor=factor
        self.epsilon=epsilon
        self.game=None
        self.state =None

    def take_damage(self, amount):
        self.player.take_damage(amount)
  
    def heal(self):
        self.player.heal()

    def update_energy(self, amount):
        self.player.update_energy(amount)

    def get_health(self):
        return self.player.get_health()
    
    def get_state(self):
        return self.player.get_state()

    def get_actions(self):
        return self.action
    
    def get_name(self):
        return self.player.get_name()
    
    def set_game(self, game):
        self.game = game
    

    def fit(self,action,reward, next_state, state=0,):
        if state != 0:
            self.state = state

    def generate_actions(self, energy=5):
        actions = []
        for defense in [1, 2, 3]:

            # Attack
            if energy > 0:
                for element in [1, 2, 3]:  
                    if energy > 2:
                        for size in [1, 2]:    
                            actions.append((Actions(1), Elements(element), Attack_Level(size), Elements(defense))) 
                    else:
                        actions.append((Actions(1), Elements(element), Attack_Level(1), Elements(defense)))  

            # Heal
            actions.append((Actions(2),Elements(0),Attack_Level(0), Elements(defense))) 

            # Defend
            for element in [1, 2, 3]:  
                actions.append((Actions(3), Elements(element),Attack_Level(0), Elements(defense))) 

        return actions


    
    def choose_action(self):
        health, energy = self.get_state()
        opponent_health, opponent_energy = self.game.get_state(self.player)
        self.state = (health, energy, opponent_health, opponent_energy)
        actions = self.generate_actions(energy)


        # Initialize Q-values if they don't exist for the current state
        if self.state not in self.q_table:
            self.q_table[self.state] = [0] * len(actions)  


        # Apply epsilon-greedy policy
        if np.random.rand() < self.epsilon:
            action_index = np.random.choice(len(actions))
        else:
            q_values = self.q_table[self.state]
            action_index = 0
            best_q_value = q_values[0]

            for i in range(self.action_size):  
                if q_values[i] > best_q_value:
                    best_q_value = q_values[i]
                    action_index = i


        self.action = actions[action_index]
          
    



def main():
    print("Game started!")
    ai = AIPlayer("AI Bob")
    player = Player("Bob")
    player2= Player("cat")
    game = Game(ai, player2)  
    ai.set_game(game)
    game.start()


if __name__ == "__main__":
    main()
