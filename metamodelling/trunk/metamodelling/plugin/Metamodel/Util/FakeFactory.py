'''
Created on 12.4.2010

@author: Michal Kovacik
'''

from __init__ import *

class FakeFactory(object):
    
    def __init__(self):
        pass
    
    def GetMetamodel(self):
        return FakeMetamodel()
        