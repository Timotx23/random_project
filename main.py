import csv
import os
from pathlib import Path


#imports of classes
from interfaces import BaseAverage, BaseDataPipelineManager
from opperations import Average
from CSV_management import DataManager




class ApplyUserTask:
    """This class is to apply the tasks that the user wants to do."""
    def __init__(self, config, ):
        self.config = config
        self.task = config.type_of_opp
       
    def apply_task(self):
        """This function decides what task will need to be run in the ApplyConversions class"""
        if self.task == "Average":
            average = Average(self.config)
            self.autoconvert = CoordinateUserTask(self.config, type_of_opperation = self.task, I_of_opperation = average )
              
        else:
            raise ValueError ("There was not given an correct type_of_opp")
        return self.autoconvert.run_task()


class CoordinateUserTask:
    def __init__(self, config, type_of_opperation: str, I_of_opperation: BaseAverage):
        self.type_of_opperation: str = type_of_opperation
        self.config = config
        self.I_of_opperation = I_of_opperation
        self.task = None
    
    def run_task(self):
        # Removed the stray Average(self.config) — use the injected I_of_opperation only
        if self.type_of_opperation == "Average":
            self.task = self.I_of_opperation.get_average()
        if self.type_of_opperation == "Gather":
            ...
        return self.task
    
        

class DataPipelineManager(BaseDataPipelineManager):
    """Controlling class that controls the data flow
    1. DataManager is called to verify the data
    2. If needed the data is converted by DoConversions
    """
    def __init__(self, csv_call_dictionary):
        """This initializes the config which is then passed to the data manager which does all the needed opperations"""
        self.user_data_configurator:DataManager = DataManager(csv_call_dictionary)
        if self.user_data_configurator.validate() == False :
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
    
    prep_work: DataPipelineManager=DataPipelineManager(input_dict)  
    if prep_work.csv_writers():     
        return True
    
if process_csv() == True:
    print("All actions have been completed sucessfullly")


#learn more about interfaces
#SOLID -> LEARN