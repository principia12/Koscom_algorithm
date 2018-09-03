from abc import *

class List(metaclass = ABCMeta):
    @abstractmethod
    def __init__(self):
        pass
        
    @abstractmethod
    def is_empty(self):
        pass
        
    @abstractmethod
    def prepend(self, item):
        pass
        
    @abstractmethod
    def append(self, item):
        pass
        
    @abstractmethod
    def head(self):
        pass
        
    @abstractmethod
    def tail(self):
        pass
        
    @abstractmethod
    def iter(self, option):
        pass