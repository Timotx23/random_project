import csv



#imports of classes
from interfaces import  BaseDataPipelineManager
from opperations import Operation
from CSV_management import DataManager, InputConfiguration


class DataPipelineManager(BaseDataPipelineManager):
    """Controlling class that controls the data flow
    1. DataManager is called to verify the data
    2. If needed the data is converted by DoConversions
    """
    def __init__(self, csv_call_dictionary: dict):
        
        self.csv_call_dictionary:dict = csv_call_dictionary
        self.config_data: InputConfiguration = None
        self._configure_datamanager() #Must be called in the init to ensure that the system is prepared
    
    def _configure_datamanager(self):
            """Configures the data and verifies that the data is in the correct format in order to ensure correct later processes"""
            self.user_data_configurator:DataManager = DataManager(self.csv_call_dictionary)   
            self.config_data: InputConfiguration = self.user_data_configurator.return_config()
            if self.config_data is not None:
                return True
            
    def user_decided_action(self):
        """This function applies the task which the user has set out """
        apply_user_task = CoordinateUserTask(self.config_data)
        return apply_user_task.run_task()
      
    def csv_writers(self) -> csv:
        """This function will write to a csv file. But only the selected values and nothing more """
        return self.user_decided_action().to_frame(self.config_data.type_of_opp).to_csv(f"{self.config_data.path_to_write}/{self.config_data.type_of_opp}_output.csv" )
    

class CoordinateUserTask:
    def __init__(self, config):
        self.type_of_opperation: str = config.type_of_opp
        self.config: dict = config
    
    def run_task(self):
        self.operation = Operation(self.config, self.type_of_opperation)
        return self.operation.decision()









   
       
