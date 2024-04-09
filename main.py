import os
import subprocess
import platform

# ======================================================
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
# ======================================================

CLEAR_COMMAND = "clear"

if (platform.system() != "Windows"):
    CLEAR_COMMAND = "cls" 


# MARK: - Crypto Engine 

class CryptoEngine():
    def __init__(self):
        pass 

    def run(self): 
        pass 

    def load_file(self) -> str:
        file_path = input("Enter or Drop File Path: ") 
        file_path = file_path.strip('"')
        # file_path = file_path.strip("'")
        return file_path 

# MARK: - Compression Engine

class CompressionEngine(CryptoEngine): 
    def __init__(self): 
        pass 

    def __compress_directory_to_rar(self):
        directory_to_compress = r"C:\Users\George Santander\Desktop\Compression\things"
        output_zip_file = r"C:\Users\George Santander\Desktop\Compression\output.rar"

        subprocess.run([r"C:\Program Files\WinRAR\WinRAR.exe", 'a', '-r', output_zip_file, directory_to_compress])

    def run(self) -> None: 
        user_option = -1 

        menu_options = (
            "====================================\n"
            "[1]: Compress Directory to RAR\n"
            "[4]: Exit\n"
            "Enter Choice: "
        )

        while (user_option != 4): 
            user_option = int(input(menu_options))
            if (user_option == 1): 
                self.__compress_directory_to_rar() 

# MARK: - File Processing Program: 

class FileProcessingProgram(): 
    def __init__(self): 
        pass 

    def run_program(self) -> None:
        user_option = -1 

        engine_options = {
            1: CompressionEngine
        }


        menu_options = (
            "====================================\n"
            "[1]: Compression\n"
            "[4]: Exit\n"
            "Enter Choice: "
        )

        while (user_option != 4):
            user_option = int(input(menu_options))

            if (user_option == 1): 
                engine = engine_options.get(1)()
                engine.run()
                
if __name__ == "__main__": 
    FileProcessingProgram().run_program() 

