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

CLEAR_COMMAND = "cls"

if (platform.system() != "Windows"):
    CLEAR_COMMAND = "clear" 


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



# MARK: - Utility Engine

class UtilityEngine(): 
    def __init__(): 
        pass 

    @staticmethod
    def get_file_name_out_of_path(file_path: str) -> str: 
        return os.path.basename(file_path)
    
    @staticmethod
    def check_if_path_exists(file_path: str) -> bool: 
        return os.path.exists(file_path)
    
    @staticmethod
    def clear_terminal():
        os.system(CLEAR_COMMAND)



# MARK: - Compression Engine Terminal UI Prompts

class CompressionEngineTerminalUIView():
    def __init__(self): 
        self.engine = CompressionEngine()


    def __prompt_menu_display(self, msg="", bars_size=30): 
        UtilityEngine.clear_terminal() 

        menu_options = (
            "=" * bars_size + "\n" + 
            f"{msg}" + 
            "=" * bars_size + "\n" 
        )

        print(menu_options)

    def __compression_prompt(self): 
        msg = "Please Enter a file path or drag file \n"
        bars_size = len(msg) 
        self.__prompt_menu_display(msg, bars_size)

        file_path = input("File Path: ")

        file_path = self.engine.load_file(file_path) 


        if (UtilityEngine.check_if_path_exists(file_path)): 
            file_name = UtilityEngine.get_file_name_out_of_path(file_path)
            msg = "Would you like to proceed in compressing file: "
            msg += file_name + "\n" 
            bars_size = len(msg)
            msg += "[1]: Yes\n"
            msg += "[2]: No\n"

            user_option = -1 

            while (user_option != 2): 
                self.__prompt_menu_display(msg, bars_size) 

                user_option = int(input("Enter choice: "))

                if user_option == 1: 
                    msg = f"compressing file: {file_name}\n"

                    bars_size = len(msg)

                    self.__prompt_menu_display(msg, bars_size) 

                    res = self.engine.compress_directory_to_rar(file_path)

                    print(res) 
                    input("Press Enter to return to main menu: ")

                    user_option = 2
        else:
            print("file does not exist") 
            input("Press Enter to return to main menu: ")

    def init_prompt(self): 
        msg = "[1]: Compress Directory to RAR\n" 
        bars_size = len(msg) 
        msg += "[4]: Exit\n" 

        user_option = -1 

        while (user_option != 4): 
            self.__prompt_menu_display(msg, bars_size) 
            user_option = int(input("Enter Choice: "))

            if (user_option == 1): 
                self.__compression_prompt()
            elif (user_option != 4): 
                UtilityEngine.clear_terminal()
                print("invalid choice!!! please chooose again") 

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
        
# MARK: - Terminal View

class TerminalView():
    def __init__(self): 
        pass 

    def init_prompt(self):
        pass 

    def _prompt_menu_display(self, msg="", bars_size=30): 
        UtilityEngine.clear_terminal() 

        menu_options = (
            "=" * bars_size + "\n" + 
            f"{msg}" + 
            "=" * bars_size + "\n" 
        )

        print(menu_options)



# MARK: - Main Terminal View

class MainTerminalView(TerminalView):
    def __init__(self):
        pass 

    def init_prompt(self):
        user_option = -1 

        msg = (
            "[1]: Compression\n"
            "[4]: Exit\n"
        )

        engine_view_options = {
            1: CompressionEngineTerminalUIView
        }

        while (user_option != 4):
            self._prompt_menu_display(msg) 
            user_option = int(input("Enter Choice: "))

            if (user_option == 1): 
                engine_view = engine_view_options.get(1)()
                engine_view.init_prompt() 
            elif (user_option != 4): 
                input("invalid choice press enter to continue")



# MARK: - File Processing Program: 

class FileProcessingProgram(): 
    def __init__(self): 
        pass 

    def run_program(self) -> None:
        MainTerminalView().init_prompt()

                
if __name__ == "__main__": 
    FileProcessingProgram().run_program() 
    
