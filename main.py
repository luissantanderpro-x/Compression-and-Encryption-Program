import os
import subprocess
import base64
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

    def hashing(self, password_bytes): 
        salt = b'salt_value'

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=1000,
            backend=default_backend()
        )

        key = kdf.derive(password_bytes)

        encoded_key = base64.urlsafe_b64encode(key) 

        cipher = Fernet(encoded_key)

        return cipher

    def load_file(self) -> str:
        file_path = input("Enter or Drop File Path: ") 
        file_path = file_path.strip('"')
        return file_path 
    
    def prompt_user_for_password(self) -> bytes: 
        password = input("Enter a Password: ")
        return password.encode('utf-8')
    

# MARK: - Encryption Engine

class EncryptionEngine(CryptoEngine):
    def __init__(self):
        pass 
    
    def __encrypt_data(self): 
        password_bytes = self.prompt_user_for_password() 

        file_path_of_file_to_be_encrypted = self.load_file() 

        encrypted_file_name = os.path.basename(file_path_of_file_to_be_encrypted)

        encrypted_file_name = f"{encrypted_file_name}.enc"

        print(encrypted_file_name)

        with open(file_path_of_file_to_be_encrypted, 'rb') as file:
            data = file.read() 
            
            encrypted_data = self.hashing(password_bytes).encrypt(data)

            with open(encrypted_file_name, 'wb') as file:
                file.write(encrypted_data)

    def run(self): 
        self.__encrypt_data()
        

# MARK: - Decryption Engine 

class DecryptionEngine(CryptoEngine):
    def __init__(self): 
        pass 

    def __decrypt_data(self): 
        file_path_of_encrypted_file_to_be_decrypted = self.load_file() 

        print(file_path_of_encrypted_file_to_be_decrypted)

    def run(self): 
        self.__decrypt_data() 





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

        os.system(CLEAR_COMMAND)

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
                user_option = 4
            else:
                print("Invalid Option")

# MARK: - File Processing Program: 

class FileProcessingProgram(): 
    def __init__(self): 
        pass 

    def run_program(self) -> None:
        user_option = -1 

        engine_options = {
            1: CompressionEngine,
            2: EncryptionEngine,
            3: DecryptionEngine
        }


        menu_options = (
            "====================================\n"
            "[1]: Compression\n"
            "[2]: Encrypt Data\n",
            "[3]: Decrypt Data\n", 
            "[4]: Exit\n"
            "Enter Choice: "
        )

        while (user_option != 4):
            user_option = int(input(menu_options))

            if (user_option == 1): 
                engine = engine_options.get(1)()
                engine.run()
                
if __name__ == "__main__": 
    DecryptionEngine().run() 
