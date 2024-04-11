# MARK: - Unit Test Dependencies 
from dependencies import unittest

from engines import CryptoEngine

# To test code run following code below 
# py -m unittest discover -s tests

# MARK: - Unit Test Cases 

class TestCryptoEngines(unittest.TestCase):
    # def test_encryption(self):
    #     self.assertEqual(True, True) 
        
    # MARK: - Encryption Engine Tests 

    def test_encrypting_file_name(self): 
        crypto = CryptoEngine() 
        file_name = 'tested_file.rar'
        encrypted_file_name = crypto.encrypt_file_name("abc123", file_name)

        len_file_name = len(file_name) 
        len_encrypted_file_name = len(encrypted_file_name)

        print(encrypted_file_name)

        self.assertGreater(len_encrypted_file_name, len_file_name)