from abc import ABC, abstractmethod
class BaseAverage(ABC):
    @abstractmethod
    def get_value(self):
        pass

    @abstractmethod
    def get_average(self):
        pass

class BaseGatherValues(ABC):
    @abstractmethod
    def get_value(self):
        pass

class BaseDataPipelineManager(ABC):
    @abstractmethod
    def UserDecidedAction(self):
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

