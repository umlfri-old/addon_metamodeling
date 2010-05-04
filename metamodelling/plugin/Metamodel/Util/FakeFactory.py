'''
Created on 12.4.2010

@author: Michal Kovacik
'''

from __init__ import *

class FakeFactory(object):
    '''
    Fake Factory with minimal required functionality, used to support a visual part of Element construction
    '''
    def __init__(self):
        pass
    
    def GetMetamodel(self):
        '''
        returns a new instance of FakeMetamodel
        '''
        return FakeMetamodel()
        