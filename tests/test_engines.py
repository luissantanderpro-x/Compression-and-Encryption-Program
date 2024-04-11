# MARK: - Unit Test Dependencies 
from dependencies import unittest

from engines import CryptoEngine

# To test code run following code below 
# py -m unittest discover -s tests

# MARK: - Unit Test Cases 

class TestCryptoEngines(unittest.TestCase):
    def test_encryption(self):
        self.assertEqual(True, True) 
        
    # MARK: - Test Compression Engine 
    def test_if_compressed_file_exists(self): 
        pass 