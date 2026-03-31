from abc import ABC, abstractmethod
class BaseAverage(ABC):
    @abstractmethod
    def get_average(self):
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

class Operation(ABC):
    def __init__(self, config, key):
        self.config = config
        self.key = key

    @abstractmethod
    def execute(self):
        pass

