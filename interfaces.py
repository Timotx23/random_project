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
        ...
class BaseDataPipelineManager(ABC):
    ...

class BaseDataManager(ABC):
    ...

