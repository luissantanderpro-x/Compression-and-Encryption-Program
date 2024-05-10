from views import MainTerminalView

# MARK: - File Processing Program: 

class FileProcessingProgram(): 
    def __init__(self): 
        pass 

    def run_program(self) -> None:
        MainTerminalView().init_prompt() 
        print("Exiting program.........") 

# MARK: - Program Main 

if __name__ == "__main__": 
    FileProcessingProgram().run_program()