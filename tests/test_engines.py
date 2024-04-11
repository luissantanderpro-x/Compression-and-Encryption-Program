# MARK: - Unit Test Dependencies 
from dependencies import unittest

from engines import CryptoEngine
from engines import EncryptionEngine
from engines import DecryptionEngine

# To test code run following code below 
# py -m unittest discover -s tests

# MARK: - Unit Test Cases 





class TestCryptoEngines(unittest.TestCase):

    # MARK: - Encrypt File Name Test

    def test_encrypting_file_name(self): 
        enc_engine = EncryptionEngine() 

        test_file_name = 'tested_file.rar'
        expected_encrypted_file_name = "whvwhg_ilohxudu"

        encrypted_file_name = enc_engine.encrypt_file_name(test_file_name)

        self.assertEqual(expected_encrypted_file_name, encrypted_file_name) 

    # MARK: Decrypt File Name Test 

    def test_decrypt_file_name(self): 
        crypto = CryptoEngine() 

        test_encrypted_file_name = "whvwhg_ilohxudu"
        expected_decrypted_file_name = "tested_file.rar" 

        decrypted_file_name = crypto.decrypt_file_name(test_encrypted_file_name)

        self.assertEqual(expected_decrypted_file_name, decrypted_file_name)

    # MARK: Encrypt Password Test

    def test_encrypt_password(self): 
        enc_engine = EncryptionEngine() 

        tested_password = "abc"

        tested_password_len = len(tested_password) 
        encrypted_password_len = len(enc_engine.encrypt_password(tested_password))

        self.assertGreater(encrypted_password_len, tested_password_len)

    # MARK: Decrypt Password Test 

    def test_decrypted_password(self): 
        dec_engine = DecryptionEngine() 

        tested_password = "abc"
        expected_decrypted_password = "abc" 

        decrypted_password = dec_engine.decrypt_password(tested_password)

        self.assertEqual(expected_decrypted_password, decrypted_password)


        


