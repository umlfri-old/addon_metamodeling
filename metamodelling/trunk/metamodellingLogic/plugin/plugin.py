'''
Created on 21.3.2010

@author: Michal Kovacik
'''
from lib.Addons.Plugin.Client.Interface import CInterface
from lib.Exceptions import *
from __init__ import *
import random
import gtk

class Plugin(object):
    def __init__(self,interface):
        self.interface = interface
        self.projectname = None
        #metamanager is only one, it is a singleton
        self.metamanager = MetamodelManager()
        try:
            self.interface.AddMenu('MenuItem', 'mnuMenubar', 'metamodelling', None, text = 'Metamodelling')
            self.interface.AddMenu('submenu', 'mnuMenubar/metamodelling', None, None)
        except PluginInvalidParameter:
            pass
        self.interface.AddMenu('MenuItem', 'mnuMenubar/metamodelling', ''.join(chr(random.randint(97,125))for i in xrange(6)), self.GenerateDomain, text = 'Generate domain')
        self.interface.AddMenu('MenuItem', 'mnuMenubar/metamodelling', ''.join(chr(random.randint(97,125))for i in xrange(6)), self.SetProjectName, text = 'Set project name')
    
    def GenerateDomain(self,*args):
        actProject = self.interface.GetAdapter().GetProject()
        if (actProject is not None):
            self.projectname = self.__GetProjectName()
        else:
            return    
        
        generator = DomainGenerator(self,actProject)
        generator.GenerateDomains()
    
    def GenerateMetamodel(self,*args):
        pass
    
    def Generate(self,*args):
        if (self.Validate(self)):
            self.GenerateDomain(self,*args)
            self.GenerateMetamodel(self,*args)
    
    def Validate(self):
        return True
    
    def SetProjectName(self,*args):
        #print self.projectname
        #WarningDialog("Neimplementovane")
        actProject = self.interface.GetAdapter().GetProject()
        if (actProject is not None):
            self.projectname = self.__GetProjectName()
        else:
            return
        
        self.metamanager.ShowEditWindow(self.__GetSelectedItem(),actProject)
        
    def __GetProjectName(self):
        return self.interface.GetAdapter().GetProject().GetRoot().GetName()  
    
    #if there is more than one item selected, fail
    def __GetSelectedItem(self):
        
        if (self.interface.GetAdapter().GetCurrentDiagram().GetSelected().size == 1):
            return self.interface.GetAdapter().GetCurrentDiagram().GetSelected()[0]
        else:
            WarningDialog("Choose ONE object or relationship")
            return None  
    
pluginMain = Plugin