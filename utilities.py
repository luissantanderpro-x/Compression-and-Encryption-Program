# MARK: - Dependencies
from dependencies import os
from dependencies import platform

import zlib

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
    def get_file_name_from_path(file_path: str):
        return os.path.splitext(file_path)
    
    @staticmethod
    def clear_terminal():
        os.system(CLEAR_COMMAND)

    @staticmethod
    def process_path(file_path: str) -> str:  
        file_path = file_path.strip('"')
        file_path = file_path.strip('& ')
        file_path = file_path.strip("'")
        return file_path
    
    @staticmethod
    def transform_to_utf_8_bytes_string(s: str) -> bytes:
        return s.encode('utf-8') 
    
    @staticmethod
    def compress_string(uncompressed_string: bytes) -> bytes:
        compressed_string = zlib.compress(uncompressed_string, 9)  
        return compressed_string


# MARK: - File Path Processing Utilities 

class FilePathProcessingUtilities():
    def __init__(self) -> None:
        pass

    @staticmethod
    def process_path(file_path: str) -> str:
        file_path = file_path.strip('"')
        file_path = file_path.strip('& ')
        file_path = file_path.strip("'")
        return file_path
    
    @staticmethod
    def check_if_file_path_exists(file_path: str) -> bool:
       return os.path.exists(file_path)
    
    @staticmethod
    def get_file_name_out_of_path(file_path: str) -> str:
        return os.path.basename(file_path) 
    
    @staticmethod
    def is_the_file_path_a_directory(file_path: str) -> bool:
        return os.path.isdir(file_path)
    
    @staticmethod
    def get_file_path_directory_child_directories(directory_path: str) -> list:
        child_folders = []
        files = os.listdir(directory_path) 

        for file in files: 
            child_file_path = FilePathProcessingUtilities.process_path(os.path.join(directory_path, file))
            child_folders.append((file, child_file_path))

        return child_folders

# MARK: - String Utilities 
        
class StringUtilities():
    def __init__(self) -> None:
        pass

    @staticmethod
    def replace_char_at_index(string_data: str, index: int, replacement: str): 
        return string_data[:index] + replacement + string_data[index + 1:]
    
    @staticmethod
    def transform_to_utf_8_bytes_string(s: str) -> bytes:
        return s.encode('utf-8') 
    