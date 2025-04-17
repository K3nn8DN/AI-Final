from enum import Enum

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
