# MARK: - Unit Test Dependencies 
from dependencies import unittest

from engines import *

"""To run all test cases"""
# py -m unittest discover -s tests

"""To run Specific Unitest Code Downn below"""
# py -m unittest discover -k test_encrypt_compressed_file

# MARK: - Unit Test Cases 

CURRENT_WORKING_DIRECTORY = os.getcwd() 

class TestCryptoEngines(unittest.TestCase):

    # MARK: - Test Salt Value
    
    '''Test if salt value was extracted from a file.'''
    def test_get_salt_from_config_file(self):
        crypto_engine = CryptoEngine() 

        file_path = r'testing\secret_test.txt'

        res = crypto_engine.get_salt_from_config_file(file_path)

        self.assertEqual('test_salt', res) 

    # MARK: - Test if compressed files output directory got created 

    def test_if_compressed_files_output_directory_exists(self): 
        comp_engine = CompressionEngine() 

        comp_engine.create_compressed_files_directory(CURRENT_WORKING_DIRECTORY)

        self.assertTrue(os.path.exists('compressed_files_output')) 

    # MARK: - Test if Compression Engine compressed specified file 

    def test_if_file_got_compressed_to_rar(self): 
        comp_engine = CompressionEngine() 

        file_path_of_file_to_be_compressed = os.path.join(CURRENT_WORKING_DIRECTORY, 'testing', 'things')

        expected_compressed_file_path = os.path.join(CURRENT_WORKING_DIRECTORY, 'things.rar') 

        comp_engine.compress_directory_to_rar(file_path_of_file_to_be_compressed) 

        self.assertTrue(os.path.exists(expected_compressed_file_path))

    # MARK: - Encrypt File Name Test

    def test_encrypting_file_name(self): 
        enc_engine = EncryptionEngine() 

        test_file_name = 'tested_file.rar'
        expected_encrypted_file_name = "whvwhg_ilohxudu"

        result = enc_engine.encrypt_file_name(test_file_name)

        params = (
            'Inputs\n'
            '==============================\n'
            f'File Name: {test_file_name}\n'
            'Result\n'
            '==============================\n'
            f'Expected file name: {expected_encrypted_file_name}\n'
            f'Result: {result}\n'
        )

        print(params)

        self.assertEqual(expected_encrypted_file_name, result) 

    # MARK: - Encrypt Password Test

    def test_encrypt_password(self): 
        enc_engine = EncryptionEngine() 

        tested_password = "abc123"

        tested_password_len = len(tested_password) 

        encrypted_password = enc_engine.encrypt_password(tested_password) 
        encrypted_password_len = len(encrypted_password)

        print(encrypted_password) 


        self.assertGreater(encrypted_password_len, tested_password_len)

    # MARK: - Encrypted File Exists Test 
# py -m unittest discover -k test_encrypt_compressed_file
    def test_encrypt_compressed_file(self): 
        """tests if file got encrypted successfully......"""
        
        enc_engine = EncryptionEngine() 

        tested_password = 'abc'
        encrypted_password = enc_engine.encrypt_password(tested_password) 

        
        compressed_file_path = os.path.join(CURRENT_WORKING_DIRECTORY, 'compressed_files', 'things.rar')

        enc_engine.encrypt_file(encrypted_password, compressed_file_path)

        expected_encrypted_file_name = "wklqjvxudu"
        expected_encrypted_file_path = os.path.join(CURRENT_WORKING_DIRECTORY, 'encrypted_files', expected_encrypted_file_name)

        self.assertTrue(os.path.exists(expected_encrypted_file_path))   

    # MARK: Decrypt File Name Test 

    def test_decrypt_file_name(self): 
        crypto = DecryptionEngine() 

        test_encrypted_file_name = "whvwhg_ilohxudu"
        expected_decrypted_file_name = "tested_file.rar" 

        decrypted_file_name = crypto.decrypt_file_name(test_encrypted_file_name)

        self.assertEqual(expected_decrypted_file_name, decrypted_file_name)

    # MARK: Decrypt Password Test 

    def test_decrypted_password(self): 
        dec_engine = DecryptionEngine() 
        enc_engine = EncryptionEngine() 

        tested_password = "abc123"
        expected_decrypted_password = "abc123" 

        decrypted_password = dec_engine.decrypt_password(tested_password)

        self.assertEqual(expected_decrypted_password, decrypted_password)

    # MARK: Check if File is rar Compressed Test

    def test_if_file_is_rar_compressed(self): 
        file_path = r'testing\things'
        
        is_compressed = CompressionEngine.is_file_rar_compressed(file_path) 

        self.assertTrue(is_compressed) 

    # MARK: Check if decrypted file exists test

    def test_if_encrypted_file_got_decrypted_and_staged(self): 
        dec_engine = DecryptionEngine() 
        enc_engine = EncryptionEngine() 

        tested_password = "abc123" 
        tested_password_encrypted = enc_engine.encrypt_password(tested_password) 

        encrypted_file_path = os.path.join(CURRENT_WORKING_DIRECTORY, 'encrypted_files', 'wklqjvxudu')

        dec_engine.decrypt_file(tested_password_encrypted, encrypted_file_path) 

        decrypted_file_path = os.path.join(CURRENT_WORKING_DIRECTORY, 'decrypted_files', 'things.rar') 

        self.assertTrue(os.path.exists(decrypted_file_path)) 