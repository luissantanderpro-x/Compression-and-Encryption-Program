# MARK: - Unit Test Dependencies 
from dependencies import unittest

from views import *

# py -m unittest discover -k test_encrypt_compressed_filed

class TestCryptikViews(unittest.TestCase):

    # MARK: - Compress File Prompt Test

    def test_compress_file_to_rar_prompt(self): 
        compression_view = CompressionEngineTerminalUIView()

        # tested_file_path = r'C:\Users\George Santander\Desktop\Compression and Encryption Program\testing\testing'
        tested_file_path = r'C:\Users\George Santander\Desktop\Compression and Encryption Program\testing\things'
        res = compression_view.test_compress_file_to_rar_localized_func(tested_file_path)

        print(res)

        self.assertTrue(True) 

