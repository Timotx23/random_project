from interfaces import BaseDataManager
from pathlib import Path

import pandas as pd #IF it was commercial i would need to check license if i want to use it
import os

class InputConfiguration:
    """This will be something of an interface class where it is responsable for the inputs"""
    def __init__(self, dictionary_of_inputs):
        try:
            self.dictionary_of_inputs: dict = dictionary_of_inputs
            self.path_to_read: Path = self.dictionary_of_inputs["reading_path"]
            self.path_to_write: Path = self.dictionary_of_inputs["writing_path"]
            self.path_to_reference:list = self.dictionary_of_inputs["reference_point"]
            self.expected_columns: list = self.dictionary_of_inputs["expected_columns"]
            self.type_of_opp: str = self.dictionary_of_inputs["type_of_opp"]
            self.access_to_db: str = None

        except:
            raise ValueError( "Invalid input was given " )
    
              

class DataManager(BaseDataManager):
    """This class is used as a prep stage. It will ensure there are sufficent paths provided as well as ensure the following:
    - Path exsists
    - CSV has the correct headers
    - Has correct type
    - CSV to write has correct format
    """
    def __init__(self,dictionary_of_inputs):
        self.dictionary_of_inputs = dictionary_of_inputs
        self.inputs_from_user:InputConfiguration = None

    def _input_config(self) -> InputConfiguration:
        self.inputs_from_user = InputConfiguration(self.dictionary_of_inputs)
        
                
    def _read_csv_path(self) -> bool:
        """This function will read the provided file path and ensure the expected csv file already exists and is in correct format
        if not in the correct format it will either convert it if requested or will void the opperation
        """
        if not os.path.exists(self.inputs_from_user.path_to_read) or not os.path.exists(self.inputs_from_user.path_to_write) :
            raise ValueError("Paths don't exist", self.inputs_from_user.path_to_read, self.inputs_from_user.path_to_write)
        
        self.inputs_from_user.access_to_db = pd.read_csv(self.inputs_from_user.path_to_read)
        return True
    
    def _validate_columns(self) -> bool:  
        actual_columns = list(self.inputs_from_user.access_to_db.columns)
        if actual_columns != self.inputs_from_user.expected_columns:
            raise ValueError("CSV Structure Mismatch")
        return True
   
    def validate(self) -> bool:
        """this validates that all the prerequisite tasks have been completed and allows system to continoue with the process"""
        #enhance this system so it detects what exactly failed instead of just a summary -> this will improve debugging and error handling
        try:
            self._input_config()
            self._read_csv_path()
            self._validate_columns()
        except:
            return False
        return True
    
    def return_config(self) -> InputConfiguration:
        try:
            self.validate()
        except:
            raise ValueError("Failed to validate some input")
        return self.inputs_from_user