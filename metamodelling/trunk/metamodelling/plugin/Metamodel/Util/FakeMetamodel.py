'''
Created on 12.4.2010

@author: Michal Kovacik
'''

from PathFactory import *
import os

class FakeMetamodel(object):
    
    def __init__(self):
        pass
    
    def GetPathFactory(self):
        return PathFactory(os.getcwd()+'/share/addons/metamodelling/metamodel/paths.xml')
        