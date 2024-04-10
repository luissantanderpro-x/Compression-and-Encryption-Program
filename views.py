# MARK: - Dependencies and Imports 
from utilities import UtilityEngine
from engines import CompressionEngine
from engines import EncryptionEngine

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
            f"{msg}\n" + 
            "=" * bars_size + "\n" 
        )

        print(menu_options)

    def _user_selection(self, msg, functions, *args): 
        user_option = -1 
        exit_value = len(functions) 

        while(user_option != exit_value):
            self._prompt_menu_display(msg) 
            user_option = int(input("Enter choice: ")) 

            if (user_option >= 0 and user_option < exit_value):
                functions[user_option](*args)
                user_option = exit_value
            elif (user_option != exit_value):
                UtilityEngine.clear_terminal()
                print("Invalid choice!!! pleae choose again") 

        functions[exit_value]()


# MARK: - Compression Engine Terminal UI Prompts

class CompressionEngineTerminalUIView(TerminalView):
    def __init__(self): 
        self.engine = CompressionEngine()

    def __compress_file(self, file_name, file_path): 
        msg = (
            f"compressing file: {file_name}"
        )

        self._prompt_menu_display(msg) 

        res = self.engine.compress_directory_to_rar(file_path)

        print(res) 

        input("Press enter to return to main menu") 


    def __exit(self): 
        print("exiting compression program") 

    def __compression_prompt(self): 
        msg = "Please Enter a file path or drag file \n"
        self._prompt_menu_display(msg) 
        file_path = input("File Path: ")

        file_path = self.engine.load_file(file_path) 


        if (UtilityEngine.check_if_path_exists(file_path)): 
            file_name = UtilityEngine.get_file_name_out_of_path(file_path)

            msg = (
                f"Would you like to proceed in compressing the file: {file_name}\n" 
                "[1]: Yes\n"
                "[2]: No\n"
            )

            functions = {
                1: self.__compress_file,
                2: self.__exit
            }

            self._user_selection(msg, functions, file_name, file_path)


        else:
            print("file does not exist") 
            input("Press Enter to return to main menu: ")



    def init_prompt(self): 
        msg = (
            "[1]: Compress Directory to RAR\n"
            "[2]: Exit"
        )

        functions = {
            1: self.__compression_prompt,
            2: self.__exit
        }

        self._user_selection(msg, functions) 


# MARK: - Encryption Terminal UI Prompts 

class EncryptionTerminalView(TerminalView): 
    def __init__(self): 
        self.engine = EncryptionEngine()

    def exit(self): 
        print("Exiting Encryption Terminal View") 

    def init_prompt(self):
        print("Encryption Terminal Init Prompot") 

        msg = (
            "[1]: Encrypt Directory"
            "[2]: Exit"
        )

        functions = {
            1: self.engine.encrypt_data,
            2: self.exit
        }

        self._user_selection(msg, functions) 

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