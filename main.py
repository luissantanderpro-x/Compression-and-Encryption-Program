# MARK: - Imports 

# TODO: Change this imports to specfiic imports

from views import *

# MARK: - File Processing Program: 

class FileProcessingProgram(): 
    def __init__(self): 
        pass 

    def run_program(self) -> None:
        CompressionEngineTerminalUIView().init_prompt() 
        # EncryptionTerminalView().init_prompt() 


# MARK: - Program Main 

if __name__ == "__main__": 
    FileProcessingProgram().run_program() 
    
