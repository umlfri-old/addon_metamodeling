'''
Created on 21.3.2010

@author: Michal Kovacik
'''
#from lib.Addons.Plugin.Interface import IDiagram
from lib.Exceptions import *
import random
from __init__ import *
import io
import os.path

addonPath = "share/addons/"
OBJ_IDENTITY = "object_name"

class DomainGenerator(object):
    def __init__(self,pluginobj,project):
        self.project = project
        self.projectname = pluginobj.projectname
        
    def GenerateDomains(self):
        if (not self.ValidateDomains()):
            return
        self.GenerateDirectories(self.projectname)
        for diag in self.project.GetRoot().GetDiagrams(): 
            GraphGenerator.GenerateGraph(self.projectname,diag)    
            for i in range(0,len(diag.GetElements())):
                ObjectGenerator.GenerateObject(self.projectname,diag.GetElements()[i])
            for i in range(0,len(diag.GetConnections())):
                RelationshipGenerator.GenerateRelationship(self.projectname,diag.GetConnections()[i]) 
          
    def ValidateDomains(self):
        for diag in self.project.GetRoot().GetDiagrams():
            if (len(diag.GetElements())==0):
                #tu by mala byt hlaska o tom, ze nemame co generovat
                WarningDialog("Niektory z diagramov je prazdny, upravte ho prosim.")
                return False
            print len(diag.GetElements())
            #validacia porovnanim, ci mame pre domenu iba jednu definiciu a ostatne pripadne rovnako nazvane elementy su iba zastupcovia
            for el in diag.GetElements():
                el.GetObject().GetValue(OBJ_IDENTITY)
                #TU POKRACUJ
                
        return True 
    
    def GenerateDirectories(self,projectname):
        try:
            basicPath = addonPath+projectname
            metaPath = basicPath+"/metamodel"
            print "test Generate directories"

            if (not os.path.isdir(basicPath)):
                io.os.mkdir(basicPath)
            if (not os.path.isdir(basicPath+"/icons")):    
                io.os.mkdir(basicPath+"/icons")
            if (not os.path.isdir(metaPath)):    
                io.os.mkdir(metaPath)
            if (not os.path.isdir(basicPath+"/templates")):    
                io.os.mkdir(basicPath+"/templates")
            if (not os.path.isdir(metaPath+"/connections")):    
                io.os.mkdir(metaPath+"/connections")
            if (not os.path.isdir(metaPath+"/diagrams")):    
                io.os.mkdir(metaPath+"/diagrams")
            if (not os.path.isdir(metaPath+"/domains")):    
                io.os.mkdir(metaPath+"/domains")
            if (not os.path.isdir(metaPath+"/elements")):    
                io.os.mkdir(metaPath+"/elements")
            if (not os.path.isdir(metaPath+"/icons")):    
                io.os.mkdir(metaPath+"/icons")
        except Exception:
            print "Directories were not generated"
            return    
        print "Directories were generated successfully"
        
    def isElementEmpty(self,element):
        pass    
        