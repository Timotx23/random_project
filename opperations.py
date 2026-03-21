from conversion import DetectingColumnsToConvert
from interfaces import BaseAverage, BaseGatherValues


class Average(BaseAverage):
    def __init__(self, config):
        super().__init__()
        self.config = config
        
    def get_value(self):
        
        detecting_columns_to_convert = DetectingColumnsToConvert(self.config)
        detecting_columns_to_convert.identify_what_to_convert()
        detecting_columns_to_convert.detected_column_mismatch_conversion()
        if detecting_columns_to_convert:
            return True
        return False
        
    def get_average(self):
        if self.get_value() == True:
            return self.config.access_to_db.groupby(self.config.path_to_reference[0])[self.config.path_to_reference[1]].mean()
        else:
            raise ValueError("Failed to verfiy input")
