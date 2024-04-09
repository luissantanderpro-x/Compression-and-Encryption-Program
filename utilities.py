# MARK: - Dependencies
from dependencies import os
from dependencies import platform

CLEAR_COMMAND = "cls"

if (platform.system() != "Windows"):
    CLEAR_COMMAND = "clear" 

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