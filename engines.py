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
        self.salt = b'salt_value'
    
    def crypto_hashing_processor(self, password_bytes, data_bytes):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(), 
            length=32,
            salt=self.salt,
            iterations=1000,
            backend=default_backend()
        )

        key = kdf.derive(password_bytes)
        cipher = Fernet(base64.urlsafe_b64encode(key))

        return cipher.encrypt(data_bytes) 
    
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
    
# MARK: - Compression Engine

class CompressionEngine(CryptoEngine): 
    def __init__(self): 
        pass 

    def get_current_working_directory(self) -> str: 
        return os.getcwd() 

    def create_compressed_files_directory(self, directory_path):
        compressed_file_directory = os.path.join(directory_path, 'compressed_files')

        try: 
            os.mkdir(compressed_file_directory)
        except FileExistsError:
            print("Directory compressed_files_output already exists")
        except Exception as e:
            print("Uknown error occurred.....") 
            
    def compress_directory_to_rar(self, file_path_of_file_to_compress) -> str:
        result = "file compressed successfully...." 

        if (UtilityEngine.check_if_path_exists(file_path_of_file_to_compress)):
            output_rar_file_name = f"{UtilityEngine.get_file_name_out_of_path(file_path_of_file_to_compress)}.rar"
            output_rar_file_path_placement = os.path.join(os.getcwd(), 'compressed_files', output_rar_file_name)

            try:
                subprocess.run([r"C:\Program Files\WinRAR\WinRAR.exe", 'a', '-r', '-ep', output_rar_file_path_placement, file_path_of_file_to_compress])
            except Exception as e:
                result = e 
        else: 
            result = "Invalid path provided unable to compress file" 

        return result 
    
    @staticmethod
    def is_file_rar_compressed(file_name: str) -> bool: 
        return '.rar' in file_name
    
# MARK: - Encryption Engine

class EncryptionEngine(CryptoEngine):
    def __init__(self):
        super().__init__()

    def create_encrypted_files_directory(self):
        encrypted_file_directory = os.path.join(os.getcwd(), 'encrypted_files')

        try: 
            os.mkdir(encrypted_file_directory)
        except FileExistsError:
            print("Directory encrypted_files already exists")
        except Exception as e:
            print("Uknown error occurred.....") 

        return encrypted_file_directory

    def encrypt_data(self, encrypted_password: bytes, data_bytes: bytes):
        cipher = Fernet(encrypted_password)
        return cipher.encrypt(data_bytes) 

    def encrypt_password(self, password: str): 
        salt_value = b'salt-123'

        password_bytes = UtilityEngine.transform_to_utf_8_bytes_string(password) 

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(), 
            length=32,
            salt=salt_value,
            iterations=1000,
            backend=default_backend()
        )

        hashed_password = kdf.derive(password_bytes)
        hashed_password = base64.urlsafe_b64encode(hashed_password)

        return hashed_password
    
    def encrypt_file_extension(self, file_name: str): 
        return StringUtilities.replace_char_at_index(file_name, -4, 'u') 
    
    def encrypt_file_name(self, file_name: str): 
        file_name = self.encrypt_file_extension(file_name)
        encrypted_file_name = self.ceasars_cipher_encrypt(file_name) 

        return encrypted_file_name
    
    def encrypt_file(self, password: bytes, compressed_file_path: str): 
        '''Encrypts file and outputs it to specific encryped directory'''

        encrypted_directory_path = self.create_encrypted_files_directory() 
        encrypted_directory_path = UtilityEngine.process_path(encrypted_directory_path)

        compressed_file_path = UtilityEngine.process_path(compressed_file_path)
        compressed_file_name = UtilityEngine.get_file_name_out_of_path(compressed_file_path)

        encrypted_file_name = self.encrypt_file_name(compressed_file_name) 

        with open(compressed_file_path, 'rb') as compressed_file:
            data = compressed_file.read() 

            encrypted_data = self.encrypt_data(password, data) 
            encrypted_file_path = os.path.join(encrypted_directory_path, encrypted_file_name) 
            
            with open(encrypted_file_path, 'wb') as enc_file:
                enc_file.write(encrypted_data) 
    
# MARK: - Decryption Engine 

class DecryptionEngine(CryptoEngine):
    def __init__(self): 
        self.__decrypted_file_directory = '' 

    def get_decrypted_file_directory(self) -> str: 
        return self.__decrypted_file_directory

    def create_decrypted_files_directory(self):
        decrypted_file_directory = os.path.join(os.getcwd(), 'decrypted_files')

        try: 
            os.mkdir(decrypted_file_directory)
        except FileExistsError:
            print("Directory decrypted_files already exists")
        except Exception as e:
            print("Uknown error occurred.....") 

        self.__decrypted_file_directory = decrypted_file_directory

        return decrypted_file_directory
    
    def decrypt_data(self, password: bytes, data: bytes): 
        '''data decryption happens here...'''
        cipher = Fernet(password) 
        return cipher.decrypt(data)

    def decrypt_password(self, password: str):
        enc_engine = EncryptionEngine() 
        password_bytes = StringUtilities.transform_to_utf_8_bytes_string(password)

        data_bytes = enc_engine.encrypt_password(password)

        return self.decrypt_data(password_bytes, data_bytes).decode('utf-8')

    def decrypt_file_extension(self, file_name: str):
        return StringUtilities.replace_char_at_index(file_name, -4, '.') 

    def decrypt_file_name(self, encrypted_file_name: str) -> str: 
        file_name = self.decrypt_file_extension(encrypted_file_name) 
        decrypted_file_name = self.ceasars_cipher_decrypt(file_name) 
        
        return decrypted_file_name

    def decrypt_file(self, password: bytes, encrypted_file_path: str) -> None:
        """Decrypts file and outputs it to decrypted_files directory"""

        decrypted_directory_path = self.create_decrypted_files_directory()
        decrypted_directory_path = UtilityEngine.process_path(decrypted_directory_path)

        encrypted_file_path = UtilityEngine.process_path(encrypted_file_path)
        encrypted_file_name = UtilityEngine.get_file_name_out_of_path(encrypted_file_path)

        decrypted_file_name = self.decrypt_file_name(encrypted_file_name) 

        with open(encrypted_file_path, 'rb') as encrypted_file: 
            data = encrypted_file.read()

            decrypted_data = self.decrypt_data(password, data)
            decrypted_file_path = os.path.join(decrypted_directory_path, decrypted_file_name)

            with open(decrypted_file_path, 'wb') as decrypted_file: 
                decrypted_file.write(decrypted_data) 