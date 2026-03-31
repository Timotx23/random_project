from conversion import DetectingColumnsToConvert
from interfaces import Operation, BaseAverage


class Operation: #this should be an interface
    def __init__(self, config, key):
        self.config = config
        self.key = key
    
    def decision(self):
        if self.column_conversion() == True:
            if self.key == "Average":
                average = Average(self.config)
                return average.get_average()
        else:
            raise ValueError("Failed to verfiy input") #Make this error more specific in the future
        
    def column_conversion(self):
        return DetectingColumnsToConvert(self.config).conversion_process()
       
class Average(BaseAverage):
    def __init__(self, config):
        self.config = config       
    def get_average(self):
        return self.config.access_to_db.groupby(self.config.path_to_reference[0])[self.config.path_to_reference[1]].mean()
        
