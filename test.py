import unittest
from unittest.mock import patch
from Game import main 

#3x6+ 3x1+3x3=30

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
heal = "2"
#Block
block_fire = ["3", "1"]
block_ice = ["3", "2"]
block_water = ["3", "3"]

class TestWin(unittest.TestCase):

    def setUp(self):
        # This runs before each test method
        self.data = [1, 2, 3]
        
    @patch('builtins.input', side_effect= fire + big_fire+
                                          ice +block_ice+
                                          fire + big_fire+
                                          ice +block_ice+
                                          fire + small_fire+
                                          ice +block_ice)  #fire attack against ice block until win
    def test_main(self, mock_input):
        result = main() 

if __name__ == '__main__':
    unittest.main()
