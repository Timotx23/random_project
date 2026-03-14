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
            self.label_to_change = self.dictionary_of_inputs["label_to_change"]
            self.action = self.dictionary_of_inputs["action"]
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
        
        self.autoconvert = ApplyConversions(config)
    def apply_task(self):
        if self.task == "Average":
            return self.autoconvert.average()
        else:
            raise ValueError ("There was not given an correct type_of_opp")



class ApplyConversions:
    """This class will coordinate the needed conversions to the file.
    Average -> needs ints
    """
    def __init__(self, config):
        self.config = config
        self.needs_conversion = {x:[i] for i,x in enumerate(self.config.path_to_reference)}
        self.opperation_type = int

    def identify_what_to_convert(self):
        user_headers = self.config.path_to_reference
        for header in user_headers:
            thing_checking = self.config.access_to_db[header]
            total_lines = 0
            total = 0
            current_type = []
            for line in thing_checking:
                contains_number = any(char.isdigit() for char in line)
                if contains_number:
                    total +=1
                total_lines +=1
                if type(line) not in current_type:
                    current_type.append(type(line))
            if len(current_type) == 1:     
                if total == total_lines:
                    if current_type[0] != float or current_type[0] != int:
                        self.needs_conversion[header]=[False, float]
                    else:
                        self.needs_conversion[header]=[True, float]
                else:
                    self.needs_conversion[header]=[True,str]
        return self.needs_conversion
    
    def converting_column(self):
        self.identify_what_to_convert()
        for header in self.config.path_to_reference:
            if self.needs_conversion[header][0] == False:
                if self.needs_conversion[header][1] == float:
                    if self.do_conversion_to_int(header) == True:
                        self.needs_conversion[header][0] = True
                    else: raise ValueError("Failed to do some conversion on",self.needs_conversion[header] )
            else:
                self.needs_conversion[header][0] = True
        print(self.needs_conversion)
        return True

    
    def do_conversion_to_int(self, converting):
        """This function will be used to convert columns if needed in order for later opperations
        This function can also run independently from the rest of the class if needed 
        """
        thing_to_convert=converting

        self.config.access_to_db[thing_to_convert] = (
                self.config.access_to_db[thing_to_convert]
                .astype(str)
                .str.replace(",", "")   #this is too hardcoded replace with ascii or similar   
                .str.replace("$", "")   #This is too hardcoded replace with ascii or similar
                .astype(float)
                )    
        return True
    
    def average(self):
        """For average the label to change """
        self.converting_column() 
        return self.config.access_to_db.groupby(self.config.path_to_reference[0])[self.config.path_to_reference[1]].mean() 




    


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
    reference_point:list =["Sales Person","Amount"] #Order doesn't matter
    thing_to_change: str="Amount"
    action:type=int # -> this shouldnt need to be given but for now its a ok fix
    expected_columns:list=["Sales Person","Country","Product","Date","Amount","Boxes Shipped"]
    type_of_opp: str= "Average"
    message = "Find average sale per sales person" #-> future idea where user simply enters this and system detects it and executes the task specified
    
    input_dict={"reading_path":reading_path, 
                "writing_path":writing_path,
                "reference_point":reference_point, 
                "label_to_change": thing_to_change,
                "action":action,
                "expected_columns":expected_columns,
                "type_of_opp": type_of_opp }
    
    prep_work: ProcessCSV=ProcessCSV(input_dict)  
    if prep_work.csv_writers():
        return True
    



if process_csv():
    print("All actions have been completed sucessfullly")


#learn more about interfaces
#SOLID -> LEARN