from abc import ABC, abstractmethod
from pathlib import Path



class BaseAverage(ABC):
    def __init__(self, config):
        self.config = config 
    @abstractmethod
    def get_average(self, access_to_db: str, path_to_reference:Path ):
        pass
    

class BaseGatherValues(ABC):
    @abstractmethod
    def get_value(self):
        pass

class BaseDataPipelineManager(ABC):
    @abstractmethod
    def user_decided_action(self):
        pass
    
    @abstractmethod
    def csv_writers(self):
        pass


class BaseDataManager(ABC):
    @abstractmethod
    def validate(self):
        pass

    @abstractmethod
    def return_config(self):
        pass

class BaseOperation(ABC):
    def __init__(self, config, key):
        self.config = config
        self.key = key

    @abstractmethod
    def decision(self):
        pass

    @abstractmethod
    def column_conversion(self):
        pass

