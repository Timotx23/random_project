class DetectingColumnsToConvert:
    def __init__(self, config):
        self.config = config
        self.needs_conversion = {x:[i] for i,x in enumerate(self.config.path_to_reference)}
        self.column_conversion = ConvertingColumns(config)
    def identify_what_to_convert(self):
        """
        This is gpt enhanced version of my code so that it is a bit more functional programming style
        """
        def analyze_column(values):
            values = list(values)

            types = {type(v) for v in values}
            all_have_digits = all(any(ch.isdigit() for ch in str(v)) for v in values)

            if len(types) == 1:
                only_type = next(iter(types))
                if all_have_digits:
                    if only_type in (int, float):
                        return [True, float]
                    return [False, float]
            return [True, str]

        headers = self.config.path_to_reference
        db = self.config.access_to_db

        self.needs_conversion: dict[ {"some", int}] = {header: analyze_column(db[header]) for header in headers}
        return self.needs_conversion
    
    def detected_column_mismatch_conversion(self) -> bool:
        """This function is in charge of ensuring that columns that have been identified to be in the wrong format be converted into the correct format"""
        for header in self.config.path_to_reference:
            if self.needs_conversion[header][0] == False :
                if self.needs_conversion[header][1] == float:
                    if self.column_conversion.convert_to_float(header) == True:
                        self.needs_conversion[header][0] = True
                    else: raise ValueError("Failed to do some conversion on",self.needs_conversion[header] )
            else:
                self.needs_conversion[header][0] = True
        return True


class ConvertingColumns:
    def __init__(self, config):
        self.config = config
    
    def convert_to_float(self, converting) -> bool:
        """This function will be used to convert columns if needed in order for later opperations
        This function can also run independently from the rest of the class if needed 
        """
        thing_to_convert:str =converting

        self.config.access_to_db[thing_to_convert] = (
                self.config.access_to_db[thing_to_convert]
                .astype(str)
                .str.replace(",", "")   #this is too hardcoded replace with ascii or similar   
                .str.replace("$", "")   #This is too hardcoded replace with ascii or similar
                .astype(float)
                )    
        return True
    
    def convert_to_int(self):
        """FOR FUTURE. IGNORE FOR Now"""
        ...


    