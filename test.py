import unittest
from unittest.mock import patch
from Game import main  # Make sure the 'main' function is imported correctly.


class TestAskTwoNumbers(unittest.TestCase):
    @patch('builtins.input', side_effect=['1', '1', '1', '2'
                                          , '2', '3','2',
                                          '1', '1', '1', '2'
                                          , '2', '3','2',
                                          '1', '1', '1', '1'
                                          , '2', '3','2'])  # Mock input to return '1' first, then '4'
    def test_main(self, mock_input):
        result = main() 

if __name__ == '__main__':
    unittest.main()
