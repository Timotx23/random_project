import pandas as pd
from pathlib import Path
class ApplyConversions:
    """This class will coordinate the needed conversions to the file.
    Average -> needs ints
    """
    def __init__(self, config, path):
        self.path = path
        self.config = config
        self.opperation_type = int #change this in future for now just testing.
        self.needs_conversion = {x:... for i,x in enumerate(self.config)}
    
    def identify_what_to_convert(self):
        """This system identifies weather something must be converted or not"""
        user_headers = self.config
        for header in user_headers:
            thing_checking = self.path[header]
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
                

path = Path("data/data_read/Chocolate Sales (2).csv")
dpath = pd.read_csv(path)
config = ["Sales Person", "Amount"]
applyconversion  = ApplyConversions(config, dpath)
print(applyconversion.identify_what_to_convert())