from main import DataPipelineManager
from pathlib import Path
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