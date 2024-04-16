# MARK: - Dependencies and Imports 
from utilities import UtilityEngine
from utilities import StringUtilities
from utilities import FilePathProcessingUtilities

from engines import CompressionEngine
from engines import EncryptionEngine
from engines import DecryptionEngine

from dependencies import keyboard

from terminal_view_templates import templates

# MARK: - Terminal View

class TerminalView():
    def __init__(self): 
        pass 

    def init_prompt(self):
        pass 

    def _proceed(self, callback, *args):
        return callback(*args) 

    def _exit(self, exit_msg=""): 
        print(exit_msg)
        return 

    def _prompt_user(self, msg: list, bars_size=30) -> str: 
        UtilityEngine.clear_terminal() 

        msg = "".join(msg) 

        prompt_display = (
            "=" * bars_size + "\n" + 
            f"{msg}\n" + 
            "=" * bars_size + "\n" 
        )

        print(prompt_display)
        

    def _get_user_input(self, input_msg: str, type="str"): 
        user_input = None
        
        if (type == 'int'):
            user_input = int(input(input_msg))
        else: 
            user_input = input(input_msg) 

        return user_input
    
    def on_arrow_key(self, event, header_template_array_list, currently_selected_option, menu_options_template, footer_template, limit=4):
        if (event.event_type == keyboard.KEY_DOWN):
            if event.name == 'up':
                if (currently_selected_option[0] != 0):
                    menu_options_template[currently_selected_option[0]] = StringUtilities.replace_char_at_index(menu_options_template[currently_selected_option[0]], 1, " ") 

                    currently_selected_option[0] -= 1

                    menu_options_template[currently_selected_option[0]] = StringUtilities.replace_char_at_index(menu_options_template[currently_selected_option[0]], 1, "X") 
        
            elif (event.name == 'down'):
                if (currently_selected_option[0] != limit):
                    menu_options_template[currently_selected_option[0]] = StringUtilities.replace_char_at_index(menu_options_template[currently_selected_option[0]], 1, " ") 

                    currently_selected_option[0] += 1

                    menu_options_template[currently_selected_option[0]] = StringUtilities.replace_char_at_index(menu_options_template[currently_selected_option[0]], 1, "X") 
            
            prompt_msg = self.merge_multiplpe_string_arrays_into_msg(header_template_array_list, menu_options_template, footer_template) 

            self._prompt_user(prompt_msg, 40)

    # TODO: Place in String Utilities when Refactoring

    def merge_multiplpe_string_arrays_into_msg(self, *args) -> str: 
        msg = ""

        for template in args: 
            template_msg = "".join(template) 
            msg += template_msg

        return msg
                    
    def _prompt_selection(self, menu_choices: dict, functions: dict, *args): 
        selected_user_option = [0]
        currently_selected = selected_user_option[0]

        exit_value = len(functions) - 1

        while (currently_selected != exit_value):
            header_template_array_list = menu_choices.get('header')[:]
            menu_choices_template_list = menu_choices.get('menu_choices')[:]
            footer_template = menu_choices.get("footer")[:]

            prompt_msg = self.merge_multiplpe_string_arrays_into_msg(header_template_array_list, menu_choices_template_list, footer_template)

            self._prompt_user(prompt_msg, 40)
            keyboard.on_press_key('up', lambda event: self.on_arrow_key(event, header_template_array_list, selected_user_option, menu_choices_template_list, footer_template, exit_value)) 
            keyboard.on_press_key('down', lambda event: self.on_arrow_key(event, header_template_array_list, selected_user_option, menu_choices_template_list, footer_template, exit_value))  

            input('') 

            keyboard.unhook_all() 

            currently_selected = selected_user_option[0]

            res = functions[currently_selected]()

            if (currently_selected != exit_value): 
                selected_user_option = [0]
                currently_selected = selected_user_option[0]

# MARK: - Compression Engine Terminal UI Prompts

class CompressionEngineTerminalUIView(TerminalView):
    def __init__(self): 
        self.engine = CompressionEngine()

    def __compress_file_to_rar(self, file_path) -> int: 
        print(f"compressing file {file_path}")

        current_working_directory = self.engine.get_current_working_directory() 

        self.engine.create_compressed_files_directory(current_working_directory)

        file_path = UtilityEngine.process_path(file_path) 

        result = self.engine.compress_directory_to_rar(file_path)

        print(f"result: {result}")
        input("press enter to proceed forward\n:") 

        return 1

    def __compress_file_to_rar_prompt(self): 
        print("Enter file path of file or directory you with to compress")

        file_path = input('file path: ') 

        print(f"[1] file path: {file_path}")

        functions = {
            0: lambda: self._proceed(self.__compress_file_to_rar, file_path), 
            1: lambda: self._exit('going back to previous menu...') 
        }

        compression_template = templates['compression_yes_or_no_options']
        self._prompt_selection(compression_template, functions)

    def __load_functions(self) -> dict: 
        return {
            0: self.__compress_file_to_rar_prompt, 
            1: lambda: self._exit("exiting compression engine....")
        }

    def init_prompt(self): 
        main_view_template = templates['compression_main']
        self._prompt_selection(main_view_template, self.__load_functions())

# MARK: - Encryption Engine Terminal UI Prompts 

class EncryptionEngineTerminalUIView(TerminalView):
    def __init__(self) -> None:
        self.encryption_engine = EncryptionEngine() 

    def __encrypt_file(self, file_path: str, hashed_password) -> int:
        '''Encryption engine logic goes here'''
        
        self.encryption_engine.encrypt_file(hashed_password, file_path)

        file_name = FilePathProcessingUtilities.get_file_name_out_of_path(file_path)
        
        print(f'File {file_name} has been encrypted successfully...')
        input('press enter to return to main menu\n:')

        return 1

    def __encrypt_file_prompt(self): 
        print("Enter a file path or drag file onto terminal if you wish to encrypt\n") 

        file_path = input('compressed file path: ') 

        UtilityEngine.clear_terminal()

        hashed_password_one = b'1'
        hashed_password_two = b'2' 

        while (hashed_password_one != hashed_password_two):
            hashed_password_one = self.encryption_engine.encrypt_password(input("Enter password to encrypt file with: "))
            hashed_password_two = self.encryption_engine.encrypt_password(input("Enter password to encrypt file one more time to double check: "))

            if (hashed_password_one != hashed_password_two):
                print("Error: Passwords don't match enter again")
            
        functions = {
            0: lambda: self._proceed(self.__encrypt_file, file_path, hashed_password_one), 
            1: lambda: self._exit('going back to previous menu...')    
        }

        self._prompt_selection(templates['encryption_yes_or_no_options'], functions) 

        return 1

    def __load_functions(self) -> dict: 
        return {
            0: self.__encrypt_file_prompt,
            1: lambda: self._exit('exiting encryption engine') 
        }

    def init_prompt(self):
        encryption_main_view_template = templates['encryption_main']
        self._prompt_selection(encryption_main_view_template, self.__load_functions())

# MARK: - Decryption Engine Terminal UI Prompts

class DecryptionEngineTerminalUIView(TerminalView):
    def __init__(self):
        self.dec_engine = DecryptionEngine() 
        self.enc_engine = EncryptionEngine() 

    def __get_password_from_user(self) -> str: 
        UtilityEngine.clear_terminal()
        password = input('Please enter file password in order to decrypt: ') 

        hashed_password = self.enc_engine.encrypt_password(password)

        print(f'hashed password: {hashed_password}')

        input(':') 

        return hashed_password

    def __decrypt_the_file(self, hashed_password: bytes, encrypted_file_path: str) -> int:
        '''Decryption Engine logic runs here...'''
        file_name = FilePathProcessingUtilities.get_file_name_out_of_path(encrypted_file_path)
        file_name = self.dec_engine.decrypt_file_name(file_name) 

        self.dec_engine.decrypt_file(hashed_password, encrypted_file_path) 

        UtilityEngine.clear_terminal()

        print(f'File {file_name} has been decrypted successfully...')
        print(f'Resides in path: {self.dec_engine.get_decrypted_file_directory()}')

        input('press [ enter ] to return....\n:')

        return 1

    def __decryption_file_prompt(self):
        print('Enter a encrypted file you wish to decrypt!')

        encrypted_file_path = input('encrypted file path: ') 

        UtilityEngine.clear_terminal()

        encrypted_file_path = FilePathProcessingUtilities.process_path(encrypted_file_path) 

        if (FilePathProcessingUtilities.check_if_file_path_exists(encrypted_file_path)):
            hashed_password = self.__get_password_from_user() 
            self.__decrypt_the_file(hashed_password, encrypted_file_path)
        else:
            print(f'File path: {encrypted_file_path} does not exists...')

        return 1

    def __load_functions(self) -> dict:
        return {
            0: self.__decryption_file_prompt,
            1: lambda: self._exit('exiting decryption engine') 
        }

    def init_prompt(self):
        decryption_main_view_template = templates['decryption_main']
        self._prompt_selection(decryption_main_view_template, self.__load_functions())
        
# MARK: - Main Terminal View

class MainTerminalView(TerminalView):
    def __init__(self):
        pass 

    def __get_compression_view(self):
        CompressionEngineTerminalUIView().init_prompt() 

    def __get_encryption_view(self):
        EncryptionEngineTerminalUIView().init_prompt()

    def __get_decryption_view(self): 
        DecryptionEngineTerminalUIView().init_prompt()
        
    def __load_functions(self) -> dict: 
        return {
            0: self.__get_compression_view,
            1: self.__get_encryption_view,
            2: self.__get_decryption_view, 
            3: lambda: self._exit('Exiting main terminal view')
        }

    def init_prompt(self):
        view_prompt = templates['main']
        self._prompt_selection(view_prompt, self.__load_functions())



