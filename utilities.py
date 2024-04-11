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
    def process_path(file_path): 
        file_path = file_path.strip('"')
        return file_path
    
    @staticmethod
    def transform_to_utf_8_bytes_string(s: str) -> bytes:
        return s.encode('utf-8') 
    
    @staticmethod
    def compress_string(uncompressed_string: bytes) -> bytes:
        compressed_string = zlib.compress(uncompressed_string, 9)  
        return compressed_string
    
        


