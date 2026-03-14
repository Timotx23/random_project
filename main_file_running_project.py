import csv
import os
from pathlib import Path
import pandas as pd #IF it was commercial i would need to check license if i want to use it

class Config:
    """This will be something of an interface class where it is responsable for the inputs"""
    def __init__(self, dictionary_of_inputs):
        self.dictionary_of_inputs=dictionary_of_inputs
        try:
            self.path_to_read = self.dictionary_of_inputs["reading_path"]
            self.path_to_write = self.dictionary_of_inputs["writing_path"]
            self.path_to_reference = self.dictionary_of_inputs["reference_point"] #change this to a list or similar
            self.expected_columns = self.dictionary_of_inputs["expected_columns"]
            self.type_of_opp = self.dictionary_of_inputs["type_of_opp"]
            self.access_to_db = None
            
        except:
            raise ValueError( "Invalid input was given " )

class ApplyUserTask:
    """This class is to apply the tasks that the user wants to do."""
    def __init__(self, config):
        self.config = config
        self.task = config.type_of_opp
        
        self.autoconvert = CoordinateConversions(config)
    def apply_task(self):
        """This function decides what task will need to be run in the ApplyConversions class"""
        if self.task == "Average":
            return self.autoconvert.average()
        else:
            raise ValueError ("There was not given an correct type_of_opp")




class CoordinateConversions:
    """
    This class will coordinate the needed conversions to the file.
    """
    def __init__(self, config):
        self.config = config
    
    def average(self):
        """For average the label to change
        It first checks that no columns must be changed.
        if columns must be changed it does so automatically such that the final average opperation is passed throough successfully
           """
        detecting_columns_to_convert = DetectingColumnsToConvert(self.config)
        converting_columns = ConvertingColumns(self.config, detecting_columns_to_convert.identify_what_to_convert())
        converting_columns.converting_column()
        return self.config.access_to_db.groupby(self.config.path_to_reference[0])[self.config.path_to_reference[1]].mean()

    def listing_items(self):
        """This function will be used if the user simply decides to get items listed""" 
    
        
class DetectingColumnsToConvert:
    def __init__(self, config):
        self.config = config
        self.needs_conversion = {x:[i] for i,x in enumerate(self.config.path_to_reference)}
    def identify_what_to_convert(self):
        """
        This is gpt enhanced version of my code so that it is a bit more functional programming style
        """
        def analyze_column(values):
            values = list(values)

            types = {type(v) for v in values}
            all_have_digits = all(any(ch.isdigit() for ch in str(v)) for v in values)

            if len(types) == 1:
                only_type = next(iter(types))
                if all_have_digits:
                    if only_type in (int, float):
                        return [True, float]
                    return [False, float]
            return [True, str]

        headers = self.config.path_to_reference
        db = self.config.access_to_db

        self.needs_conversion = {header: analyze_column(db[header]) for header in headers}
        return self.needs_conversion


class ConvertingColumns:
    def __init__(self, config, dict):
        self.config = config
        self.needs_conversion = dict
    def converting_column(self) -> bool:
        """This function is in charge of ensuring that columns that have been identified to be in the wrong format be converted into the correct format"""
        for header in self.config.path_to_reference:
            if self.needs_conversion[header][0] == False :
                if self.needs_conversion[header][1] == float:
                    if self.convert_to_float(header) == True:
                        self.needs_conversion[header][0] = True
                    else: raise ValueError("Failed to do some conversion on",self.needs_conversion[header] )
            else:
                self.needs_conversion[header][0] = True
        return True
    def convert_to_float(self, converting) -> bool:
        """This function will be used to convert columns if needed in order for later opperations
        This function can also run independently from the rest of the class if needed 
        """
        thing_to_convert:str =converting

        self.config.access_to_db[thing_to_convert] = (
                self.config.access_to_db[thing_to_convert]
                .astype(str)
                .str.replace(",", "")   #this is too hardcoded replace with ascii or similar   
                .str.replace("$", "")   #This is too hardcoded replace with ascii or similar
                .astype(float)
                )    
        return True
    
    def convert_to_int(self):
        """FOR FUTURE. IGNORE FOR Now"""
        ...

    def collect_items(self):
        """
        This function will be used when the user wants to simply collect items from the db(FUTURE)
        """
    
    

class DataManager:
    """This class is used as a prep stage. It will ensure there are sufficent paths provided as well as ensure the following:
    - Path exsists
    - CSV has the correct headers
    - Has correct type
    - CSV to write has correct format
    """
    def __init__(self,dictionary_of_inputs):
        self.inputs_from_user:Config = Config(dictionary_of_inputs)
        self.read_csv_path()
                
    def read_csv_path(self):
        """This function will read the provided file path and ensure the expected csv file already exists and is in correct format
        if not in the correct format it will either convert it if requested or will void the opperation
        """
        if not os.path.exists(self.inputs_from_user.path_to_read) or not os.path.exists(self.inputs_from_user.path_to_write) :
            raise ValueError("Paths don't exist", self.inputs_from_user.path_to_read, self.inputs_from_user.path_to_write)
        
        self.inputs_from_user.access_to_db = pd.read_csv(self.inputs_from_user.path_to_read)
        return True
    
    def validate_columns(self):  
        actual_columns=list(self.inputs_from_user.access_to_db.columns)
        if actual_columns!= self.inputs_from_user.expected_columns:
            raise ValueError("CSV Structure Mismatch")
        return True
   
    def validate(self):
        """this validates that all the prerequisite tasks have been completed and allows system to continoue with the process"""
        if self.validate_columns() == True and self.read_csv_path() == True:
            return True
        return False
    
    def return_config(self):
        return self.inputs_from_user
        
    
                   

class ProcessCSV:
    """Controlling class that controls the data flow
    1. DataManager is called to verify the data
    2. If needed the data is converted by DoConversions
    """
    def __init__(self, csv_call_dictionary):
        """This initializes the config which is then passed to the data manager which does all the needed opperations"""
        self.user_data_configurator=DataManager(csv_call_dictionary)
        if self.user_data_configurator.validate() == False:
            raise ValueError("Failed to prepare the data")
        self.config_data = self.user_data_configurator.return_config()

    
    def UserDecidedAction(self):
        apply_user_task = ApplyUserTask(self.config_data)
        return apply_user_task.apply_task()
      
    def csv_writers(self) -> csv:
        """This function will write to a csv file. But only the selected values and nothing more """
        return self.UserDecidedAction().to_frame(self.config_data.type_of_opp).to_csv(f"{self.config_data.path_to_write}/{self.config_data.type_of_opp}_output.csv" )
   
       

#Declarers to make it more flexible
def process_csv():
    """
    This way of calling the class Process_csv is used if only one dictionary is provided.
    All inputs are still the same just cleaner to read and better structuring 
    """
    reading_path:str=Path("data/data_read/Chocolate Sales (2).csv")
    writing_path: str= Path("data/data_write/")
    reference_point:list =["Sales Person","Amount"] #Order  matters
    expected_columns:list=["Sales Person","Country","Product","Date","Amount","Boxes Shipped"]
    type_of_opp: str= "Average"
    message = "Find average sale per sales person" #-> future idea where user simply enters this and system detects it and executes the task specified
    
    input_dict={"reading_path":reading_path, 
                "writing_path":writing_path,
                "reference_point":reference_point, 
                "expected_columns":expected_columns,
                "type_of_opp": type_of_opp }
    
    prep_work: ProcessCSV=ProcessCSV(input_dict)  
    if prep_work.csv_writers():
        return True
    
if process_csv():
    print("All actions have been completed sucessfullly")


#learn more about interfaces
#SOLID -> LEARN