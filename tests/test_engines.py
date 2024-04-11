# MARK: - Unit Test Dependencies 
from dependencies import unittest

from engines import *

# To test code run following code below 
# py -m unittest discover -s tests

# MARK: - Unit Test Cases 

CURRENT_WORKING_DIRECTORY = os.getcwd() 

class TestCryptoEngines(unittest.TestCase):

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

        encrypted_file_name = enc_engine.encrypt_file_name(test_file_name)

        self.assertEqual(expected_encrypted_file_name, encrypted_file_name) 

    # MARK: - Encrypt Password Test

    def test_encrypt_password(self): 
        enc_engine = EncryptionEngine() 

        tested_password = "abc"

        tested_password_len = len(tested_password) 
        encrypted_password_len = len(enc_engine.encrypt_password(tested_password))

        self.assertGreater(encrypted_password_len, tested_password_len)

    # MARK: - Encrypted File Exists Test 

    # def test_if_encrypted_file_got_created(self): 
    #     current_working_directory = os.getcwd()
    #     test_directory = os.path.join(current_working_directory, 'testing', "things.txt")



    #     print(test_directory) 

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

        tested_password = "abc"
        expected_decrypted_password = "abc" 

        decrypted_password = dec_engine.decrypt_password(tested_password)

        self.assertEqual(expected_decrypted_password, decrypted_password)

    # MARK: Check if File is rar Compressed Test

    def test_if_file_is_rar_compressed(self): 
        file_path = r"C:\Users\George Santander\Desktop\Compression and Encryption Program\testing\Lyft and Uber Side Hustle Business Documents.rar"
        
        is_compressed = CompressionEngine.is_file_rar_compressed(file_path) 

        self.assertTrue(is_compressed) 



        


