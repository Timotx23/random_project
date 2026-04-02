from conversion import ColumnTypeDetector
from interfaces import BaseOperation, BaseAverage
from pathlib import Path

class Operation(BaseOperation): #this should be an interface    
    def decision(self):
        if self.column_conversion() == True:
            if self.key == "Average":
                average = Average(self.config)
                return average.get_average(self.config.access_to_db, self.config.path_to_reference)
        else:
            raise ValueError("Failed to verfiy input") #Make this error more specific in the future
        
    def column_conversion(self):
        return ColumnTypeDetector(self.config).conversion_process()
       
class Average(BaseAverage):     
    def get_average(self, access_to_db: str, path_to_reference: Path):
        return access_to_db.groupby(path_to_reference[0])[path_to_reference[1]].mean()
        
