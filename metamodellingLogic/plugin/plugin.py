'''
Created on 21.3.2010

@author: Michal Kovacik
'''
from lib.Addons.Plugin.Client.Interface import CInterface
from lib.Exceptions import *
from __init__ import *
import random

class Plugin(object):
    def __init__(self,interface):
        self.interface = interface
        try:
            self.interface.AddMenu('MenuItem', 'mnuMenubar', 'metamodelling', None, text = 'Metamodelling')
            self.interface.AddMenu('submenu', 'mnuMenubar/metamodelling', None, None)
        except PluginInvalidParameter:
            pass
        self.interface.AddMenu('MenuItem', 'mnuMenubar/metamodelling', ''.join(chr(random.randint(97,125))for i in xrange(6)), self.GenerateDomain, text = 'Generate domain')
    
    def GenerateDomain(self,*args):
        print self
        print args
        actProject = self.interface.GetAdapter().GetProject()
        
        generator = DomainGenerator(actProject)
        generator.GenerateDomains()
    
    def GenerateMetamodel(self,*args):
        pass
    
    def Generate(self,*args):
        if (self.Validate(self)):
            self.GenerateDomain(self,*args)
            self.GenerateMetamodel(self,*args)
    
    def Validate(self):
        return True
    
pluginMain = Plugin