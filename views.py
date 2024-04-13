# MARK: - Dependencies and Imports 
from utilities import UtilityEngine
from utilities import StringUtilities
from engines import CompressionEngine
from engines import EncryptionEngine

from dependencies import keyboard

# MARK: - Terminal View

class TerminalView():
    def __init__(self): 
        pass 

    def init_prompt(self):
        pass 

    def _exit(self, exit_msg=""): 
        print(exit_msg)

    def _prompt_user(self, msg: list, bars_size=30) -> None: 
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
    
    def on_arrow_key(self, event, currently_selected_option, prompt, limit=4):

        if (event.event_type == keyboard.KEY_DOWN):
            if event.name == 'up':
                print("Up arrow pressed")
                if (currently_selected_option[0] != 0):
                    prompt[currently_selected_option[0]] = StringUtilities.replace_char_at_index(prompt[currently_selected_option[0]], 1, " ") 

                    currently_selected_option[0] -= 1

                    prompt[currently_selected_option[0]] = StringUtilities.replace_char_at_index(prompt[currently_selected_option[0]], 1, "*") 
        
            elif (event.name == 'down'):
                print("Down arrow pressed")

                if (currently_selected_option[0] != limit):
                    prompt[currently_selected_option[0]] = StringUtilities.replace_char_at_index(prompt[currently_selected_option[0]], 1, " ") 

                    currently_selected_option[0] += 1

                    prompt[currently_selected_option[0]] = StringUtilities.replace_char_at_index(prompt[currently_selected_option[0]], 1, "*") 

            self._prompt_user(prompt)
                    

    def _prompt_selection(self, view_prompt: dict, functions: dict, *args): 
        selected_user_option = [0]

        exit_value = len(functions) - 1

        prompt = view_prompt.get(1)[:]

        keyboard.on_press_key('up', lambda event: self.on_arrow_key(event, selected_user_option, prompt, exit_value)) 
        keyboard.on_press_key('down', lambda event: self.on_arrow_key(event, selected_user_option, prompt, exit_value))

        currently_selected = selected_user_option[0]

        self._prompt_user(prompt) 

        while (currently_selected != exit_value): 
            keyboard.wait('return') 

            # TODO: Write code here for triggering functions 

            currently_selected = selected_user_option[0]

            functions[currently_selected]()


        print(selected_user_option)

        # while(user_option != exit_value):
        #     self._prompt_user(view_prompt.get(1))

        #     user_option = self._get_user_input(view_prompt.get(2), 'int') 
            
        #     if (user_option >= 0 and user_option < exit_value):
        #         functions[user_option](*args)
        #         user_option = exit_value
        #     elif (user_option != exit_value):
        #         UtilityEngine.clear_terminal()
        #         print("Invalid choice!!! pleae choose again") 

        # functions[exit_value](view_prompt.get(3))


# MARK: - Terminal View Templates 

terminal_view_templates = {
    'main': {
        1: [
            "[*] Compression\n",
            "[ ] Encryption\n",
            "[ ] Decryption\n",
            "[ ] Exit"
        ], 
        2: "Enter choice: ",
        3: 'Exiting main...'
    }, 
    'compression_init': {
        1: ["Welcome to compression program...\n"
            
        ],
        2: "Enter choice: ",
        3: 'Exiting compression view...'
    }
}


# MARK: - Compression Engine Terminal UI Prompts

class CompressionEngineTerminalUIView(TerminalView):
    def __init__(self): 
        self.engine = CompressionEngine()

    # def __compress_file(self, file_name, file_path): 
    #     msg = (
    #         f"compressing file: {file_name}"
    #     )

    #     self._prompt_menu_display(msg) 

    #     res = self.engine.compress_directory_to_rar(file_path)

    #     print(res) 

    #     input("Press enter to return to main menu") 

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
        pass 

# MARK: - Main Terminal View

class MainTerminalView(TerminalView):
    def __init__(self):
        pass 

    def __get_compression_view(self):
        print("compression view...") 

    def __get_encryption_view(self):
        print("encryption view....")

    def __get_decryption_view(self): 
        print("decryption view....")  

    def __load_functions(self) -> dict: 
        return {
            0: self.__get_compression_view,
            1: self.__get_encryption_view,
            2: self.__get_decryption_view, 
            3: lambda: self._exit("Exiting main terminal view")
        }

    def init_prompt(self):
        view_prompt = terminal_view_templates['main']
        self._prompt_selection(view_prompt, self.__load_functions())

