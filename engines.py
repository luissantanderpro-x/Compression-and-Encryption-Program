# MARK: - Engine Dependencies 
from dependencies import os
from dependencies import base64
from dependencies import subprocess

from utilities import UtilityEngine
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

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

    def load_file(self, file_path):
        file_path = file_path.strip('"')

        if (os.path.exists(file_path)):
            print("exists") 
        else:
            print('does not exist')
            
        return file_path
    
    def prompt_user_for_password(self) -> bytes: 
        password = input("Enter a Password: ")
        return password.encode('utf-8')
    

# MARK: - Compression Engine

class CompressionEngine(CryptoEngine): 
    def __init__(self): 
        pass 

    def compress_directory_to_rar(self, file_path) -> str:
        result = "file compressed successfully...." 

        directory_to_compress = file_path

        if (UtilityEngine.check_if_path_exists(directory_to_compress)):
            output_rar_file = f"{UtilityEngine.get_file_name_out_of_path(directory_to_compress)}.rar"

            try:
                subprocess.run([r"C:\Program Files\WinRAR\WinRAR.exe", 'a', '-r', '-ep', output_rar_file, directory_to_compress])
            except Exception as e:
                result = e 
        else: 
            result = "Invalid path provided unable to compress file" 

        return result 
    
# MARK: - Encryption Engine

class EncryptionEngine(CryptoEngine):
    def __init__(self):
        pass 
    
    def encrypt_data(self): 
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

# MARK: - Decryption Engine 

class DecryptionEngine(CryptoEngine):
    def __init__(self): 
        pass 

    def __decrypt_data(self): 
        file_path_of_encrypted_file_to_be_decrypted = self.load_file() 

        print(file_path_of_encrypted_file_to_be_decrypted)

        decrypted_file_name = os.path.basename(file_path_of_encrypted_file_to_be_decrypted)
        decrypted_file_name = os.path.splitext(decrypted_file_name)[0]

        print(decrypted_file_name)

        with open(file_path_of_encrypted_file_to_be_decrypted, 'rb') as file: 
            encrypted_data = file.read() 

            print("decrypt data please enter password")
            password_bytes = self.prompt_user_for_password()

            decrypted_data = self.hashing(password_bytes).decrypt(encrypted_data)

            with open(decrypted_file_name, 'wb') as d_file:
                d_file.write(decrypted_data)


    def run(self): 
        self.__decrypt_data() 