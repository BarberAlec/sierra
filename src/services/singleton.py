import logging


class Singleton:
    """Base class for implementing the singletons."""
    _instances = {}
    
    def __new__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super(Singleton, cls).__new__(cls)
            instance.logger = logging.getLogger(cls.__module__)
            instance.initialized = False
            cls._instances[cls] = instance
        return cls._instances[cls]
    
    def __init__(self):
        if not self.initialized:
            self._initialize()
            self.initialized = True
    
    def _initialize(self):
        pass
        
    @classmethod
    def _reset(cls):
        """Reset - should only be used in tests."""
        if cls in cls._instances:
            del cls._instances[cls]
