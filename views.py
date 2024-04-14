# MARK: - Dependencies and Imports 
from utilities import UtilityEngine
from utilities import StringUtilities
from engines import CompressionEngine
from engines import EncryptionEngine

from dependencies import keyboard


def capture_input():
    input_string = ""
    print("Enter your input (press Enter to submit):")
    
    # Listen for key presses
    while True:
        event = keyboard.read_event(suppress=True)
        
        if event.event_type == keyboard.KEY_DOWN:
            if event.name == 'enter':
                # Terminate input loop when Enter is pressed
                break
            elif event.name == 'backspace':
                # Remove the last character from the input_string
                input_string = input_string[:-1]
            elif len(event.name) == 1:
                # Append the pressed character to the input_string
                input_string += event.name

        print(input_string) 
    
    keyboard.unhook_all() 
    
    return input_string




# MARK: - Terminal View

class TerminalView():
    def __init__(self): 
        pass 

    def init_prompt(self):
        pass 

    def _exit(self, exit_msg=""): 
        print(exit_msg)
        return 

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
    
    def on_arrow_key(self, event, header_template_array_list, currently_selected_option, menu_options_template, limit=4):
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
            
            prompt_msg = self.merge_multiplpe_string_arrays_into_msg(header_template_array_list, menu_options_template) 

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

        exit_value = len(functions) - 1

        header_template_array_list = menu_choices.get('header')[:]
        menu_choices_template_list = menu_choices.get('menu_choices')[:]

        currently_selected = selected_user_option[0]

        prompt_msg = self.merge_multiplpe_string_arrays_into_msg(header_template_array_list, menu_choices_template_list)

        while (currently_selected != exit_value):
            self._prompt_user(prompt_msg, 40)
            keyboard.on_press_key('up', lambda event: self.on_arrow_key(event, header_template_array_list, selected_user_option, menu_choices_template_list, exit_value)) 
            keyboard.on_press_key('down', lambda event: self.on_arrow_key(event, header_template_array_list, selected_user_option, menu_choices_template_list, exit_value))
            keyboard.wait('esc') 
            keyboard.unhook_all() 
            currently_selected = selected_user_option[0]
            functions[currently_selected]()

# MARK: - Terminal View Templates 

terminal_view_templates = {
    'main': {
        'header': [
            "Please enter one of the following options\n"
        ], 
        'menu_choices': [
            "[X] Compression\n",
            "[ ] Encryption\n",
            "[ ] Decryption\n",
            "[ ] Exit"
        ]
    }, 
    'compression_main': {
        'header': [
            "Welcome to the compression engine...\n Please choose one of the following compression options\n"
        ],
        'menu_choices': [
            "[X] Compress to RAR Format\n",
            "[ ] Return back to Main Menu"
        ]
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

    # def __compression_prompt(self): 
    #     msg = "Please Enter a file path or drag file \n"
    #     self._prompt_menu_display(msg) 
    #     file_path = input("File Path: ")

    #     file_path = self.engine.load_file(file_path) 


    #     if (UtilityEngine.check_if_path_exists(file_path)): 
    #         file_name = UtilityEngine.get_file_name_out_of_path(file_path)

    #         msg = (
    #             f"Would you like to proceed in compressing the file: {file_name}\n" 
    #             "[1]: Yes\n"
    #             "[2]: No\n"
    #         )

    #         functions = {
    #             1: self.__compress_file,
    #             2: self.__exit
    #         }

    #         self._user_selection(msg, functions, file_name, file_path)


    #     else:
    #         print("file does not exist") 
    #         input("Press Enter to return to main menu: ")

    def __compression_prompt(self): 
        print('compressoin prompot') 
        
        user_input = input("enter something......") 

        print(user_input)

    def __load_functions(self) -> dict: 
        return {
            0: self.__compression_prompt,
            1: lambda: self._exit("Exiting main compression menu...") 
        }

    def init_prompt(self): 
        main_view_template = terminal_view_templates['compression_main']
        self._prompt_selection(main_view_template, self.__load_functions())

# MARK: - Main Terminal View

class MainTerminalView(TerminalView):
    def __init__(self):
        pass 

    def __get_compression_view(self):
        print("compression view...") 
        CompressionEngineTerminalUIView().init_prompt() 

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


