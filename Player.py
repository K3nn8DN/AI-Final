from Enums import Actions, Elements, Attack_Level
import numpy as np
import json
import ast


class Player:
    def __init__(self, name):
        self.name = name
        self.health = 10
        self.energy = 5
        self.action = None,None,None,None

    def reset(self):
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
    




class AIPlayer:
    def __init__(self, name, learning_rate=0.1, factor=0.95, epsilon=0.1):
        self.player = Player(name)
        self.q_table = {}
        self.learning_rate=learning_rate
        self.factor=factor
        self.epsilon=epsilon
        self.game=None
        self.state =None

    def reset(self):
        self.load_q_table()
        self.player.reset()

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
        return self.action[0]
    
    def get_name(self):
        return self.player.get_name()
    
    def set_game(self, game):
        self.game = game

    

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
        self.state = (health, energy, *self.game.get_state(self.player))
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

            for i in range(len(actions)):  
                if q_values[i] > best_q_value:
                    best_q_value = q_values[i]
                    action_index = i


        self.action = actions[action_index], action_index



    def fit(self,reward,next_state=-1,actionindex=-1, state=-1,):
        if state == -1:
            state = self.state 
        if actionindex == -1:
            actionindex = self.action[1]
        if next_state == -1:
            next_state = (*self.get_state(), *self.game.get_state(self.player))
        
        # Find the best Q-value for the next state or initialize as 0
        best_next_q_value = max(self.q_table.get(next_state, [0,0]))  

        td_target = reward + self.factor * best_next_q_value
        td_error = td_target - self.q_table[state][actionindex]
        self.q_table[state][actionindex] += self.learning_rate * td_error




    def save_q_table(self):
        filename=self.get_name() +"_q_table.json"
        with open(filename, "w") as f:
            items = []
            for k, v in self.q_table.items():
                k_str = str(k)                  
                v_str = json.dumps(v)           
                line = f'  "{k_str}": {v_str}'  
                items.append(line)
            f.write("{\n" + ",\n".join(items) + "\n}")
        

    def load_q_table(self):
        filename=self.get_name() +"_q_table.json"
        try:
            with open(filename, "r") as json_file:
                q_table_from_file = json.load(json_file)

            q_table_loaded = {}  

            for state_str, q_values in q_table_from_file.items():
                state_tuple = ast.literal_eval(state_str)
                q_table_loaded[state_tuple] = q_values

            self.q_table = q_table_loaded

        except FileNotFoundError:
            print(f"No saved Q-table found at {filename}. Starting with an empty table.")



class EasyAIPlayer(AIPlayer):
    def choose_action(self):
        health, energy = self.get_state()
        self.state = (health, energy)
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

            for i in range(len(actions)):  
                if q_values[i] > best_q_value:
                    best_q_value = q_values[i]
                    action_index = i


        self.action = actions[action_index], action_index


          
    
