import numpy as np
from Game import Player

class AIPlayer:
    def __init__(self, name, learning_rate=0.1, factor=0.95, epsilon=0.1):
        self.player = Player(name)
        self.learning_rate = learning_rate
        self.factor = factor
        self.epsilon = epsilon
        self.q_table = {}  
        self.actions = self.generate_actions()  # Fixed list of 30 structured actions
        self.game = None
        self.state = None

    def generate_actions(self):
        return [[0, 0, 0, 0] for _ in range(30)]

    def get_state(self):
        return self.player.get_state()

    def get_actions(self):
        return self.actions

    

    def update_q_table(self, action_index, reward, next_state):
        if next_state not in self.q_table:
            self.q_table[next_state] = [0.0 for _ in self.actions]

        best_next_q_value = max(self.q_table[next_state])
        td_target = reward + self.factor * best_next_q_value
        td_error = td_target - self.q_table[self.state][action_index]

        self.q_table[self.state][action_index] += self.learning_rate * td_error


  







def choose_action(self):
    health, energy = self.get_state()
    opponent_health, opponent_energy = self.game.get_state()
    self.state = (health, energy, opponent_health, opponent_energy)
    actions = generate_actions(energy)


    # Initialize Q-values if they don't exist for the current state
    if self.state not in self.q_table:
        self.q_table[self.state] = [0] * actions.size()  


    # Apply epsilon-greedy policy
    if np.random.rand() < self.epsilon:
        action_index = np.random.choice(actions)
    else:
        q_values = self.q_table[self.state]
        action_index = max(actions, key=lambda action: q_values[action])  # Select action with max Q-value

    return action_index  # Return the index of the chosen action
    




























def generate_actions(energy=5):
    actions = []
    for defense in [1, 2, 3]:

        # Attack
        for element in [1, 2, 3]:  
            for size in [1, 2]:    
                actions.append([defense,1, element, size])

        #Heal
        actions.append([defense,2])  

        #Defend
        for element in [1, 2, 3]:  
            actions.append([defense,3, element])

    # Return the actions that can be taken based on energy
    if energy < 3:
        None
    if energy <1:
        None
    return actions



    

if __name__ == '__main__':
    actions = generate_actions()
    for i, action in enumerate(actions):
        print(f"{i}: {action}")