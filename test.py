import unittest
from unittest.mock import patch
from Game import Game 
from Player import Player, AIPlayer



#Defense 1=fire, 2=ice, 3=water
fire = ["1"]
ice = ["2"]
water = ["3"]
#Attack 1=Attack (1=fire, 2=ice, 3=water)  (1=Small, 2=Big)
big_fire = ["1","1","2"]
big_ice = ["1","2","2"]
big_water = ["1","3","2"]
small_fire = ["1","1","1"]
small_ice = ["1","2","1"]
small_water = ["1","3","1"]
#heal
heal = ["2"]
#Block
block_fire = ["3", "1"]
block_ice = ["3", "2"]
block_water = ["3", "3"]

class TestWin(unittest.TestCase):

    def setUp(self):
        ai = AIPlayer("art")
        player = Player("player")
        self.game = Game(player, ai)  
        ai.set_game(self.game)

    @patch('builtins.input', side_effect= fire + big_fire+
                                          ice + block_ice+
                                          fire + big_fire+
                                          ice + block_ice+
                                          fire + small_fire+
                                          ice + block_ice)  
    def test_player_2_wins(self, mock_input):
        result = self.game.start() 
        self.assertEqual(result, "player_2")


    @patch('builtins.input', side_effect= water + big_fire+
                                          ice + big_ice+
                                          water + heal+
                                          water + block_ice+
                                          fire + small_fire+
                                          ice + big_fire)  
    def test_player_1_wins(self, mock_input):
        result = self.game.start() 
        self.assertEqual(result, "player_1") 

    
    @patch('builtins.input', side_effect= fire + big_water+
                                          fire + big_ice+
                                          ice + heal+
                                          water + block_ice+
                                          fire + small_fire+
                                          ice + big_fire)  
    def test_player_2_wins_again(self, mock_input):
        result = self.game.start() 
        self.assertEqual(result, "player_2") 



if __name__ == '__main__':
    unittest.main()
