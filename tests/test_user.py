import unittest
from app.models import User



class TestUser(unittest.TestCase):
    """
    The test for the articles class

    Args:
        unittest : The unittest
    """
    def setUp(self):
        """
        This is the set up that runs before the test
        """
        self.new_user= User("suez","suezanwar54@gmail.com",124,'default.png',

        )
        
    def test_news_source_(self):
        """
        Test if the instance created by article class
        """
        self.assertTrue(isinstance(self.new_user,User))
        
if __name__ == '__main__':
    unittest.main()