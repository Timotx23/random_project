import csv
import os
from pathlib import Path
import pandas as pd #IF it was commercial i would need to check license if i want to use it

class AutoConvert:
    """This class will auto convert the rows if needed in order for the user not to need to enter this step manually
    It can either run independently from the DataManager class or run in sync with it
    """
    def __init__(self, types, label, access_to_db):
        self.type=types
        self.label=label
        self.access_to_db=access_to_db
    def do_conversions(self):
        """This function will be used to convert columns if needed in order for later opperations
        This function can also run independently from the rest of the class if needed (FUTURE)
        """
        thing_to_convert=self.label
        if self.type== int: #This is still somewhat hard coded and could still be improved
            self.access_to_db[thing_to_convert] = (
                self.access_to_db[thing_to_convert]
                .astype(str)
                .str.replace(",", "")   #this is too hardcoded    
                .str.replace("$", "")   #This is too hardcoded   
                .astype(float)
                )    
        elif self.action == str:
            self.access_to_db[thing_to_convert]=str(self.access_to_db[thing_to_convert])
        return True

class Config:
    """This will be something of an interface class where it is responsable for the inputs"""
    def __init__(self, dictionary_of_inputs):
        self.dictionary_of_inputs=dictionary_of_inputs
        try:
            self.path_to_read = self.dictionary_of_inputs["reading_path"]
            self.path_to_write = self.dictionary_of_inputs["writing_path"]
            self.path_to_reference = self.dictionary_of_inputs["reference_point"]
            self.label_to_change = self.dictionary_of_inputs["label_to_change"]
            self.action = self.dictionary_of_inputs["action"]
            self.expected_columns = self.dictionary_of_inputs["expected_columns"]
            self.type_of_opp = self.dictionary_of_inputs["type_of_opp"]
            self.access_to_db = None
            
        except:
            raise ValueError( "Invalid input was given " )
    


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
        
        actual_columns=list(self.inputs_from_user.access_to_db.columns)
        if actual_columns!= self.inputs_from_user.expected_columns or self.inputs_from_user.path_to_reference not in actual_columns or self.inputs_from_user.label_to_change not in actual_columns:
            raise ValueError("CSV Structure Mismatch")
        return True
    
    def ConvertingColumn(self):
        actual_conversion = AutoConvert(self.inputs_from_user.action, self.inputs_from_user.label_to_change, self.inputs_from_user.access_to_db)
        if actual_conversion.do_conversions() == True:
            return True
    def return_config(self):
        return self.inputs_from_user
        
    
                   

class ProcessCSV:
    """Controlling class that controls both the prep_csv and the prep_input_data
    """
    def __init__(self, csv_call_dictionary):
        """This initializes the config which is then passed to the data manager which does all the needed opperations"""
        self.user_data_configurator=DataManager(csv_call_dictionary)
        self.config_data = self.user_data_configurator.return_config()

    
    def UserDecidedAction(self):
        access_to_db=self.user_data_configurator.inputs_from_user.access_to_db
        
        if self.user_data_configurator.inputs_from_user.type_of_opp == "Average":
            if self.config_data.action == int:
                self.user_data_configurator.ConvertingColumn()
                return access_to_db.groupby(self.config_data.path_to_reference)[self.config_data.label_to_change].mean() 
        if self.user_data_configurator.inputs_from_user.type_of_opp == "list":
            return access_to_db.groupby(self.config_data.path_to_reference)[self.config_data.label_to_change]
        else:
            raise ValueError ("There was not given an correct type_of_opp")
            
    def csv_writers(self) -> bool:
        """This function will write to a csv file. But only the selected values and nothing more """
        return self.UserDecidedAction().to_frame(self.config_data.type_of_opp).to_csv(f"{self.config_data.type_of_opp}_output.csv")
   
       

#Declarers to make it more flexible
def improved_call_csv_class():
    """
    This way of calling the class Process_csv is used if only one dictionary is provided.
    All inputs are still the same just cleaner to read and better structuring 
    """
    reading_path:str=Path("data/data_read/Chocolate Sales (2).csv")
    writing_path: str= Path("data/data_write/")
    reference_point:str="Sales Person" 
    thing_to_change: str="Amount"
    action:type=int # -> this shouldnt need to be given but for now its a ok fix
    expected_columns:list=["Sales Person","Country","Product","Date","Amount","Boxes Shipped"]
    type_of_opp: str= "Average"
    
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
    



if improved_call_csv_class():
    print("All actions have been completed sucessfullly")


#learn more about interfaces
#SOLID -> LEARN