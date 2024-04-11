# MARK: - Engine Dependencies 
from dependencies import os
from dependencies import base64
from dependencies import subprocess


from utilities import UtilityEngine
from utilities import StringUtilities

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

# MARK: - Crypto Engine

class CryptoEngine():
    def __init__(self):
        pass 
    
    def crypto_hashing_processor(self, data_bytes, algorthim):
        salt = b'salt_value'

        kdf = PBKDF2HMAC(
            algorithm=algorthim(),
            length=32,
            salt=salt,
            iterations=1000,
            backend=default_backend()
        )

        key = kdf.derive(data_bytes)

        encoded_key = base64.urlsafe_b64encode(key) 

        cipher = Fernet(encoded_key)

        return cipher
    
    def ceasars_cipher_encrypt(self, string_data, shift=3): 
        encrypted_text = "" 

        for char in string_data:
            if char.isalpha():
                if char.isupper():
                    encrypted_text += chr((ord(char) + shift - 65) % 26 + 65)
                else:
                    encrypted_text += chr((ord(char) + shift - 97) % 26 + 97)
            else:
                encrypted_text += char 

        return encrypted_text
    
    def ceasars_cipher_decrypt(self, string_data, shift=3): 
        decrypted_text = self.ceasars_cipher_encrypt(string_data, shift * -1)
        return decrypted_text
    
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

    def encrypt_data(self, password_bytes: bytes, data_bytes: bytes):
        return self.crypto_hashing_processor(password_bytes, hashes.SHA256).encrypt(data_bytes) 

    def encrypt_password(self, password: str): 
        password_bytes = UtilityEngine.transform_to_utf_8_bytes_string(password)         
        return self.encrypt_data(password_bytes, password_bytes) 
    
    def encrypt_file_extension(self, file_name: str): 
        return self.replace_char_at_index(file_name, -4, 'u')
    
    def encrypt_file_name(self, file_name: str): 
        file_name = self.encrypt_file_extension(file_name)
        encrypted_file_name = self.ceasars_cipher_encrypt(file_name) 

        return encrypted_file_name
    
    # def encrypt_data(self, encrypted_password_cipher: Fernet, file_path_of_file_to_be_encrypted): 
    #     file_path_of_file_to_be_encrypted = UtilityEngine.process_path(file_path_of_file_to_be_encrypted)
    #     file_name = UtilityEngine.get_file_name_out_of_path(file_path_of_file_to_be_encrypted)
        
    #     encrypted_file_name = self.encrypt_file_name(file_name)


    #     # with open(file_path_of_file_to_be_encrypted, 'rb') as file:
    #     #     data = file.read() 
            
    #     #     encrypted_data = encrypted_password_cipher.encrypt(data) 

    #     #     with open(encrypted_file_name, 'wb') as file:
    #     #         file.write(encrypted_data)

    #     return "success"

# MARK: - Decryption Engine 

class DecryptionEngine(CryptoEngine):
    def __init__(self): 
        pass 

    def decrypt_password(self, password: str):
        enc_engine = EncryptionEngine() 
        password_bytes = StringUtilities.transform_to_utf_8_bytes_string(password)

        data_bytes = enc_engine.encrypt_password(password)

        return self.crypto_hashing_processor(password_bytes, hashes.SHA256).decrypt(data_bytes).decode('utf-8')

    def decrypt_data(self, encrypted_password_cipher: Fernet, file_path_of_compressed_file_to_be_decrypted):
        file_path_of_compressed_file_to_be_decrypted = UtilityEngine.process_path(file_path_of_compressed_file_to_be_decrypted)
        
        # Check if the path exists 

        decrypted_file_name = UtilityEngine.get_file_name_out_of_path(file_path_of_compressed_file_to_be_decrypted)

        print(decrypted_file_name)

    def decrypt_file_extension(self, file_name: str):
        return StringUtilities.replace_char_at_index(file_name, -4, '.') 

    def decrypt_file_name(self, encrypted_file_name: str) -> str: 
        file_name = self.decrypt_file_extension(encrypted_file_name) 
        decrypted_file_name = self.ceasars_cipher_decrypt(file_name) 

        return decrypted_file_name
    

    # def __decrypt_data(self): 
    #     file_path_of_encrypted_file_to_be_decrypted = self.load_file() 

    #     print(file_path_of_encrypted_file_to_be_decrypted)

    #     decrypted_file_name = os.path.basename(file_path_of_encrypted_file_to_be_decrypted)
    #     decrypted_file_name = os.path.splitext(decrypted_file_name)[0]

    #     print(decrypted_file_name)

    #     with open(file_path_of_encrypted_file_to_be_decrypted, 'rb') as file: 
    #         encrypted_data = file.read() 

    #         print("decrypt data please enter password")
    #         password_bytes = self.prompt_user_for_password()

    #         decrypted_data = self.hashing(password_bytes).decrypt(encrypted_data)

    #         with open(decrypted_file_name, 'wb') as d_file:
    #             d_file.write(decrypted_data)


    # def run(self): 
    #     self.__decrypt_data() 