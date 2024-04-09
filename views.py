# MARK: - Dependencies and Imports 
from utilities import UtilityEngine
from engines import CompressionEngine

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