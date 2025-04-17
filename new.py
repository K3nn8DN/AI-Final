import numpy as np
from Game import Player



def generate_actions(energy=5):
        actions = []
        for defense in [1, 2, 3]:

            # Attack
            if energy > 0:
                for element in [1, 2, 3]:  
                    if energy > 2:
                        for size in [1, 2]:    
                            actions.append([defense,1, element, size])
                    else:
                        actions.append([defense,1, element, 1])

            #Heal
            actions.append([defense,2])  

            #Defend
            for element in [1, 2, 3]:  
                actions.append([defense,3, element])

        return actions



    

if __name__ == '__main__':
    actions = generate_actions(0)
    for i, action in enumerate(actions):
        print(f"{i}: {action}")