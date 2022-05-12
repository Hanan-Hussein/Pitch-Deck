import unittest
from app.models import Pitch


class test_pitch(unittest.TestCase):
    """
    The test for the pitch class

    Args:
        unittest : The unittest
    """
    def setUp(self):
        """
        This is the set up that runs before the test
        """
        self.new_news_source = Pitch("Food","new recipe invented","10","0","nice idea","Agriculture","9/05/2022")
        
    def test_news_source_(self):
        """
        Test if the instance created by news_source
        """
        self.assertTrue(isinstance(self.new_news_source,Pitch))
        
if __name__ == '__main__':
    unittest.main()