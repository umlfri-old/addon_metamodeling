'''
Created on 21.3.2010

@author: Michal Kovacik
'''
import os
from __init__ import * 

class Singleton(type):
    def __init__(cls, name, bases, dict):
        super(Singleton, cls).__init__(name, bases, dict)
        cls.instance = None
 
    def __call__(cls, *args, **kw):
        if cls.instance is None:
            cls.instance = super(Singleton, cls).__call__(*args, **kw)
 
        return cls.instance

class MetamodelManager(object):
    __metaclass__ = Singleton
    def __init__(self):
        self.metamodels = dict()
        
    def ShowEditWindow(self,selected,project):
        #if (selected is not None):
            #tu potom pridat ze ak uz pre takuto vizualnu reprezentaciu mame v 
            #self.metamodels 
        EditWindow(selected,project)
    
    def GenerateMetamodels(self):
        pass
    
    def __GetSelectedElement(self,project):
        if (project is not None):
            return 
    
        
if __name__ == '__main__':
    a=MetamodelManager()