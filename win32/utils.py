# -*- coding:utf-8 -*-

class PAGException(Exception):
    """
    Raise Exception here.
    """
    def __init__(self,reason):
        self.reason=str(reason)
        super().__init__(self,reason)
    
    def __str__(self):
        return self.reason

class FileNotFoundException(Exception):
    """
    File not found exception.
    """
    def __init__(self,reason):
        self.reason=str(reason)
        super().__init__(self,reason)
    
    def __str__(self):
        return self.reason
