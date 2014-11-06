'''
Created on 21.3.2010

@author: Michal Kovacik
'''
from lib.Addons.Plugin.Client.Interface import CInterface
from lib.Exceptions import *
from __init__ import *
import random
import gtk
from zipfile import ZipFile,ZIP_DEFLATED


class Plugin(object):
    '''
    Entrance point into module
    @ivar projectname: defines name of project which we work on
    @ivar metamanager: Singleton of MetamodelManager() to manage metamodel data
    '''
    def __init__(self,interface):
        '''
        Create new instance of Metamodelling object
        @param interface: interface object sent from a plug-in core system 
        '''
        self.interface = interface
        self.interface.SetGtkMainloop()
        self.projectname = None
        #metamanager is only one, it is a singleton
        self.metamanager = MetamodelManager()
        try:
            mainmenu = self.interface.GetAdapter().GetGuiManager().GetMainMenu()
            mmenu = mainmenu.AddMenuItem('mitMetamodelling',None,len(mainmenu.GetItems())-1,'Metamodelling')
            mmenu.AddSubmenu()
            msubmenu=mmenu.GetSubmenu()
            msubmenu.AddMenuItem('mitDomain',self.GenerateDomain,0,'Generate domain')
            msubmenu.AddMenuItem('mitVisual',self.SetVisualIdentity,1,'Set visual identity')
            msubmenu.AddMenuItem('mitMeta',self.GenerateMetamodel,2,'Generate metamodel')
            msubmenu.AddMenuItem('mitMetaSaveAll',self.Generate,3,'Generate')
        except PluginInvalidParameter:
            pass
            
    def GenerateDomain(self,*args):
        '''
        Generates domain, so that is full data background of new metamodel
        but no visual representation is within this method created
        '''
        actProject = self.interface.GetAdapter().GetProject()
        if (actProject is not None):
            self.projectname = self.__GetProjectName()
        else:
            return    
        
        generator = DomainGenerator(self,actProject)
        generator.GenerateDomains()
    
    def GenerateMetamodel(self,*args):
        '''
        Generates visual representation of data background
        '''
        actProject = self.interface.GetAdapter().GetProject()
        if (actProject is not None):
            self.projectname = self.__GetProjectName()
        else:
            return
        
        self.metamanager.GenerateMetamodels(actProject,self.projectname)
    
    def Generate(self,*args):
        '''
        Saves entire project as FRI Addon
        that means zip packed file with .fria extension
        '''
        dialog = gtk.FileChooserDialog("Save..",
                                       None,
                                       gtk.FILE_CHOOSER_ACTION_SAVE,
                                       (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                       gtk.STOCK_SAVE, gtk.RESPONSE_OK))
        dialog.set_default_response(gtk.RESPONSE_OK)

        filter = gtk.FileFilter()
        filter.set_name("Fri addon")
        filter.add_pattern("*.fria")

        dialog.add_filter(filter)
        dialog.show()
        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            name = dialog.get_filename()
            if name != None:
                #file = open(name, 'w')
                fZip = ZipFile(name, 'w', ZIP_DEFLATED)
                actProject = self.interface.GetAdapter().GetProject()
                if (actProject is not None):
                    self.projectname = self.__GetProjectName()
                else:
                    return
                
                generator = DomainGenerator(self,actProject)
                generator.GenerateDomains(fZip)
                self.metamanager.GenerateMetamodels(actProject,self.projectname,fZip)
                fZip.close()
            
            dialog.destroy()
        elif response == gtk.RESPONSE_CANCEL:
            pass
        dialog.destroy()
    
    def Validate(self):
        '''
        Validation method for future restrictions
        '''
        return True
    
    def SetVisualIdentity(self,*args):
        '''
        Method for making a pair of data and visual representation of Object or Relationship type
        '''
        actProject = self.interface.GetAdapter().GetProject()
        if (actProject is not None):
            self.projectname = self.__GetProjectName()
        else:
            return
        selItem = self.__GetSelectedItem()
        if (selItem is not None): self.metamanager.ShowEditWindow(self.__GetSelectedItem(),actProject)
        
    def __GetProjectName(self):
        '''
        private method encapsulating the way how to get projectname
        @return: name of project under construction
        @rtype: str
        '''
        return self.interface.GetAdapter().GetProject().GetRoot().GetName()  
    
    #if there is more than one item selected, fail
    def __GetSelectedItem(self):  
        '''
        private method used to get selected item
        @return: selected item
        @rtype: various
        '''
        if (len(self.interface.GetAdapter().GetCurrentDiagram().GetSelected()) == 1):
            return self.interface.GetAdapter().GetCurrentDiagram().GetSelected()[0]
        else:
            WarningDialog("Choose ONE object or relationship")
            return None  
    
pluginMain = Plugin