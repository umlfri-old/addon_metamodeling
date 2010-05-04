'''
Created on 12.4.2010

@author: Michal Kovacik
'''

from PathFactory import *
import os

class FakeMetamodel(object):
    '''
    Fake Metamodel with minimal required functionality, used to support a visual part of Element construction
    '''
    def __init__(self):
        pass
    
    def GetPathFactory(self):
        '''
        Path factory created from metamodelling paths.xml file
        '''
        return PathFactory(os.getcwd()+'/share/addons/metamodelling/metamodel/paths.xml')
        