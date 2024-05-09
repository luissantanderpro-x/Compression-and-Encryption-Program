# MARK: - Dependencies and Imports 
from utilities import UtilityEngine
from utilities import StringUtilities
from utilities import FilePathProcessingUtilities

from engines import CompressionEngine
from engines import EncryptionEngine
from engines import DecryptionEngine

from dependencies import keyboard
from dependencies import time 

from terminal_view_templates import templates

# MARK: - Terminal View

class TerminalView():
    def __init__(self): 
        pass 

    def init_prompt(self):
        pass 

    def _proceed(self, callback, *args):
        return callback(*args) 

    def _exit(self, exit_value: int, exit_msg=""): 
        print(exit_msg)
        return exit_value

    def _prompt_user(self, msg: list, bars_size=50) -> str: 
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
    
    def _get_file_path_from_directories_file_tree(self, file_path: str, subtemplate: dict) -> str: 
        chosen_file_path = '' 
        menu_options = [] 

        parent_directory_name = FilePathProcessingUtilities.get_file_name_out_of_path(file_path)
        folder_space_away_from_parent = 3

        specific_engine_select_template = subtemplate

        child_files = FilePathProcessingUtilities.get_file_path_directory_child_directories(file_path)

        menu_options.append(f'[X] - {parent_directory_name}\n')

        functions = {}

        functions[0] = lambda: file_path

        key = 1 

        for child_file in child_files: 
            child_file_option = '[ ]' + (' ' * folder_space_away_from_parent) + f' | - {child_file[0]}\n'
            menu_options.append(child_file_option)
            child_file_path = child_file[1]
            functions[key] = lambda path = child_file_path: path
            key += 1

        menu_options.append('[ ] return to main menu')

        specific_engine_select_template['menu_choices'] = menu_options

        functions[key] = lambda: self._exit(len(functions) - 1, 'returning to previous menu') 

        chosen_file_path = self._prompt_menu_options(specific_engine_select_template, functions) 

        return chosen_file_path
        
    
    def on_arrow_key(self, event, header_template_array_list, currently_selected_option: list, menu_options_template, footer_template, limit=4):
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
            
            prompt_msg = self.merge_multiple_string_arrays_into_msg(header_template_array_list, menu_options_template, footer_template) 

            '''Refreshes the screen everytime user moves the cursor'''
            self._prompt_user(prompt_msg, 50)

    # TODO: Place in String Utilities when Refactoring

    def merge_multiple_string_arrays_into_msg(self, *args) -> str: 
        msg = ""
        for template in args: 
            template_msg = "".join(template) 
            msg += template_msg
        return msg
                    
    def _prompt_selection(self, menu_options: dict, functions: dict, *args): 
        selected_user_option = [0]
        currently_selected = selected_user_option[0]
        exit_value = len(functions) - 1

        res = None

        while (currently_selected != exit_value):
            header_template_array_list = menu_options.get('header')[:]
            menu_choices_template_list = menu_options.get('menu_choices')[:]
            footer_template = menu_options.get("footer")[:]

            prompt_msg = self.merge_multiple_string_arrays_into_msg(header_template_array_list, menu_choices_template_list, footer_template)

            self._prompt_user(prompt_msg, 50)
            keyboard.on_press_key('up', lambda event: self.on_arrow_key(event, header_template_array_list, selected_user_option, menu_choices_template_list, footer_template, exit_value)) 
            keyboard.on_press_key('down', lambda event: self.on_arrow_key(event, header_template_array_list, selected_user_option, menu_choices_template_list, footer_template, exit_value))  

            input('') 

            keyboard.unhook_all() 

            currently_selected = selected_user_option[0]

            res = functions[currently_selected]()

            if (res == exit_value):
                currently_selected = res
            elif (currently_selected != exit_value): 
                selected_user_option = [0]
                currently_selected = selected_user_option[0]

    def _prompt_menu_options(self, menu_options: dict, functions: dict, selected_user_option=[0]): 
        exit_value = len(functions) - 1

        print('select:', selected_user_option)

        currently_selected = selected_user_option[0]

        header_template_array_list = menu_options.get('header')[:]
        menu_choices_template_list = menu_options.get('menu_choices')[:]
        footer_template = menu_options.get("footer")[:]

        prompt_msg = self.merge_multiple_string_arrays_into_msg(header_template_array_list, menu_choices_template_list, footer_template)

        self._prompt_user(prompt_msg, 50)
        keyboard.on_press_key('up', lambda event: self.on_arrow_key(event, header_template_array_list, selected_user_option, menu_choices_template_list, footer_template, exit_value)) 
        keyboard.on_press_key('down', lambda event: self.on_arrow_key(event, header_template_array_list, selected_user_option, menu_choices_template_list, footer_template, exit_value))  

        input('') 

        currently_selected = selected_user_option[0]

        keyboard.unhook_all() 

        return functions[currently_selected]()

    def _prompt_menu_options_loop(self, menu_options: dict, functions: dict):
        selected_user_option = [0]
        currently_selected = selected_user_option[0]
        exit_value = len(functions) - 1

        res = None

        while (currently_selected != exit_value): 
            res = self._prompt_menu_options(menu_options, functions, selected_user_option) 

            if (res != exit_value):
                selected_user_option = [0]
                currently_selected = selected_user_option
            elif (res == exit_value):
                currently_selected = exit_value

        return res

# MARK: - Compression Terminal View

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

    # MARK: - TESTING BREAKPOINT [1]

    '''for testing private function __compress_file_to_rar_prompt'''
    def test_compress_file_to_rar_localized_func(self, test_file_path: str): 
        return self._get_file_path_from_directories_file_tree(test_file_path, templates['compression_select_file'])
    
    def __compress_file_to_zip(self, file_path: str) -> int:
        '''
        Compresses file / directory using zip compression.
        '''
        res = -1 
        current_working_directory = self.engine.get_current_working_directory() 

        self.engine.create_compressed_files_directory(current_working_directory) 

        file_path = UtilityEngine.process_path(file_path) 

        result = self.engine.compress_directory_to_zip(file_path) 

        print(f'result: {result}')
        input('press enter to proceed forward\n:')

        if (result == 'file compressed successfully...'):
            res = 1 
        return res 
        
    def __get_selected_file_path_prompt(self) -> str: 
        UtilityEngine.clear_terminal()
        print('Enter file path or drop a file / directory.')

        file_path = input('file path: ') 
        file_path = FilePathProcessingUtilities.process_path(file_path)

        if (FilePathProcessingUtilities.is_the_file_path_a_directory(file_path)):
            file_path = self._get_file_path_from_directories_file_tree(file_path, templates['compression_select_file'])
        else:
            print('this is a file not directory') 

        return file_path 
    
    def __compress_file_to_rar_prompt(self) -> int: 
        print('rar prompt')

        file_path = self.__get_selected_file_path_prompt() 

        functions = {
            0: lambda: self.__compress_file_to_rar(file_path),
            1: lambda: self._exit(1, 'exiting out of the program') 
        }

        selected_choice = [0]
                
        compression_template = templates['compression_yes_or_no_options']
        self._prompt_menu_options(compression_template, functions, selected_choice)

        return 2
    
    def __compress_file_to_zip_prompt(self):
        print('zip prompt') 

        file_path = self.__get_selected_file_path_prompt() 

        functions = {
            0: lambda: self.__compress_file_to_zip(file_path),
            1: lambda: self._exit(2, 'exiting out of the program') 
        }

        compression_template = templates['compression_yes_or_no_options']

        selected_choice = [0]

        self._prompt_menu_options(compression_template, functions, selected_choice) 

        return 2 
        
    def __load_functions(self) -> dict: 
        return {
            0: self.__compress_file_to_rar_prompt,
            1: self.__compress_file_to_zip_prompt, 
            2: lambda: self._exit(2, "exiting compression engine....")
        }

    def init_prompt(self): 
        main_view_template = templates['compression_main']
        self._prompt_menu_options_loop(main_view_template, self.__load_functions())
        
# MARK: - Encryption Terminal View 

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
        file_path = FilePathProcessingUtilities.process_path(file_path)

        if (FilePathProcessingUtilities.is_the_file_path_a_directory(file_path)):
            file_path = self._get_file_path_from_directories_file_tree(file_path, templates['encryption_select_file'])
        else:
            print('this is file path is not a directory.') 

        UtilityEngine.clear_terminal()

        hashed_password_one = b'1'
        hashed_password_two = b'2' 

        while (hashed_password_one != hashed_password_two):
            hashed_password_one = self.encryption_engine.encrypt_password(input("Enter password to encrypt file with: "))
            hashed_password_two = self.encryption_engine.encrypt_password(input("Enter password to encrypt file one more time to double check: "))

            if (hashed_password_one != hashed_password_two):
                print("Error: Passwords don't match enter again")
            
        functions = {
            0: lambda: self.__encrypt_file(file_path, hashed_password_one),
            1: lambda: self._exit(1, 'going back to previous menu...')    
        }

        self._prompt_selection(templates['encryption_yes_or_no_options'], functions) 

        return 1

    def __load_functions(self) -> dict: 
        return {
            0: self.__encrypt_file_prompt,
            1: lambda: self._exit(1, 'exiting encryption engine') 
        }

    def init_prompt(self):
        encryption_main_view_template = templates['encryption_main']
        self._prompt_menu_options_loop(encryption_main_view_template, self.__load_functions())

# MARK: - Decryption Engine Terminal View

class DecryptionEngineTerminalUIView(TerminalView):
    def __init__(self):
        self.dec_engine = DecryptionEngine() 
        self.enc_engine = EncryptionEngine() 

    def __get_password_from_user(self) -> str: 
        UtilityEngine.clear_terminal()
        password = input('Please enter password in order to decrypt file: ') 
        hashed_password = self.enc_engine.encrypt_password(password)
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
        print('Enter file path of encrypted file you wish to decrypt.')
        encrypted_file_path = input('encrypted file path: ') 

        UtilityEngine.clear_terminal()

        encrypted_file_path = FilePathProcessingUtilities.process_path(encrypted_file_path) 

        if (FilePathProcessingUtilities.check_if_file_path_exists(encrypted_file_path)):
            hashed_password = self.__get_password_from_user() 


            # TODO: Check if Password is Valid before decrypting the file to prevent errors
            # before attempting to derypt entire file. 

            self.__decrypt_the_file(hashed_password, encrypted_file_path)
        else:
            print(f'File path: {encrypted_file_path} does not exists...')

        return 1

    def __load_functions(self) -> dict:
        return {
            0: self.__decryption_file_prompt,
            1: lambda: self._exit(1, 'exiting decryption engine') 
        }

    def init_prompt(self):
        decryption_main_view_template = templates['decryption_main']
        self._prompt_menu_options_loop(decryption_main_view_template, self.__load_functions())
        
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
            3: lambda: self._exit(3, 'Exiting main terminal view')
        }

    def init_prompt(self):
        view_prompt = templates['main']
        intro_template = templates['intro'].get('banner') 

        banner = self.merge_multiple_string_arrays_into_msg(intro_template)

        self._prompt_user(banner) 

        time.sleep(0.5)

        self._prompt_menu_options_loop(view_prompt, self.__load_functions())



