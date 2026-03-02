import csv
import os
from pathlib import Path
import pandas as pd

class check_format:
    """This class will be used to check the input format of for the Process_csv class in order for it to sucessfully opperate"""
    def __init__(self, *args):

        ...
    def decide(self):
        ...
class auto_convert:
    """This class will auto convert the rows if needed in order for the user not to need to enter this step manually"""
    def __init__(self, **kwargs):
        ... 

class Prep_csv:
    """This class is used as a prep stage. It will ensure there are sufficent paths provided as well as ensure the following:
    - Path exsists
    - CSV has the correct headers
    - Has correct type
    - CSV to write has correct format
    """
    def __init__(self,paths: list[str, str],lables: list[str,str], action: list[int,bool], expected_columns):
        self.action=action
        self.paths=paths
        self.lables=lables
        self.expected_columns=expected_columns
        self.access_to_db=None
    
    def read_csv_path(self):
        """This function will read the provided file path and ensure the expected csv file already exists and is in correct format
        if not in the correct format it will either convert it if requested or will void the opperation
        """
        if not os.path.exists(self.paths[1]) or not os.path.exists(self.paths[0]) :
            return False
        self.access_to_db = pd.read_csv(self.paths[0])
        
        actual_columns=list(self.access_to_db.columns)
        if actual_columns!= self.expected_columns or self.lables[1] not in actual_columns or self.lables[0] not in actual_columns:
            raise ValueError("CSV Structure Mismatch")
        return True
        
    def do_conversions(self,):
        """This function will be used to convert columns if needed in order for later opperations
        This function can also run independently from the rest of the class if needed (FUTURE)
        """
        thing_to_convert=self.lables[self.action[0]]
        if self.action[1]== int: #This is still somewhat hard coded and could still be improved
            self.access_to_db[thing_to_convert] = (
                self.access_to_db[thing_to_convert]
                .astype(str)
                .str.replace(",", "")       
                .str.replace("$", "")      
                .astype(float)
                )    
        elif self.action[1] == str:
            self.access_to_db[thing_to_convert]=str(self.access_to_db[thing_to_convert])
        return True
    def is_working(self):
        if Prep_csv.read_csv_path(self)== True and Prep_csv.do_conversions(self) == True:
            return True
    def File_reader(self):
        return self.access_to_db
               
class Process_csv:
    def __init__(self,paths: list[str, str],lables: list[str,str], action: list[int,bool], expected_columns,type_of_opp):
        
        self.check_if_valid=Prep_csv(paths,lables, action, expected_columns)# This verifies that the csv exsists and is working as expected
        if self.check_if_valid.is_working() == True:
            self.paths=paths
            self.lables=lables
            self.action=action
            self.type_of_opp=type_of_opp
            self.dicti={}
        else:
            raise ValueError("Faild to verify CSV flie")
        
    def decision(self):
        access_to_db=self.check_if_valid.File_reader()
        if self.type_of_opp == "Average":
            return access_to_db.groupby(self.lables[1])[self.lables[0]].mean() 
        if self.type_of_opp == "list":
            return access_to_db.groupby(self.lables[1])[self.lables[0]]
            
    def csv_writers(self) -> bool:
        """This function will write to a csv file. But only the selected values and nothing more """
        
        return Process_csv.decision(self).to_frame(name=self.type_of_opp).to_csv("output.csv")
       

#Declarers to make it more flexible
def call_csv_class():
    """This function will be called and contains all the most important things that will needed to be given as input for the Process_csv class.
    This is done sothat only this function needs to be modified if needed
    The inputs needed:
    paths=[path for csv, path to write]
    labels=[what is being measured, who  is being measured ]
    action=[index of the labels that needs to be adjusted, to what it needs to be converted to]
    expected_columns = [Represents the expected columns that are expected in the csv]
    type_of_opp= str: is the opperation that is being done to the labels[0]
    prep_work: Actually calls the Process_csv  class
    Pros:
    - System is more modular and u dont have things stored in one dict
    -system is more modular by itself
    Cons:
    - Order matters a lot
    - A bit more hard coded classes
    """
    paths:list=[Path("data/data_read/Chocolate Sales (2).csv"),Path("data/data_write/")]
    labels:list=["Amount","Sales Person" ]
    action:list=[0,int]
    expected_columns:list=["Sales Person","Country","Product","Date","Amount","Boxes Shipped"]
    type_of_opp: str="Average"
    prep_work=Process_csv(paths,labels,action,expected_columns,type_of_opp )  
    if prep_work.csv_writers():
        return True


if call_csv_class() == True:
    print("All actions have been completed sucessfullly")

def improved_call_csv_class():
    """
    This way of calling the class Process_csv is used if only one dictionary is provided.
    All inputs are still the same just cleaner to read and better structuring 
    """
    reading_path:str=Path("data/data_read/Chocolate Sales (2).csv")
    writing_path: str= Path("data/data_write/")
    reference_point:str="Sales Person" 
    thing_to_change: str="Amount"
    action:list=[0,int] # -> this shouldnt need to be given

    expected_columns:list=["Sales Person","Country","Product","Date","Amount","Boxes Shipped"]
    type_of_opp: str="Average"
    
    input_dict={"reading path":reading_path, 
                "writing path":writing_path,
                "reference_point":reference_point, 
                "label to change": thing_to_change,
                "action":action,
                "expected_columns":expected_columns,
                "type_of_opp": type_of_opp }
    
    #prep_work=Process_csv(dictionary_to_call=input_dict)  
    #if prep_work.csv_writers():
        #return True
    