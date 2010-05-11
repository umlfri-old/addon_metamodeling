'''
Created on 21.3.2010

@author: Michal Kovacik
'''
from lib.Exceptions import *
#import random
from __init__ import *
import io
import os.path

addonPath = "share/addons/"
OBJ_IDENTITY = "object_name"

class DomainGenerator(object):
    '''
    class which manages domain process creation
    '''
    def __init__(self,pluginobj,project):
        self.project = project
        self.projectname = pluginobj.projectname
        
    def GenerateDomains(self,zipfile=None):
        '''
        for all Objects and Relationships generates the data background on the file system
        '''
        if (not self.ValidateDomains()):
            return
        if not zipfile: self.__GenerateDirectories(self.projectname)
        for diag in self.project.GetRoot().GetDiagrams(): 
            GraphGenerator.GenerateGraph(self.projectname,diag,zipfile)    
            for i in range(0,len(diag.GetElements())):
                if (diag.GetElements()[i].GetObject().GetType()=="Object"):
                    ObjectGenerator.GenerateObject(self.projectname,self.project,diag.GetElements()[i],zipfile)
            for i in range(0,len(diag.GetConnections())):
                if (diag.GetConnections()[i].GetObject().GetType()=="Relationship"):
                    ObjectGenerator.GenerateObject(self.projectname,self.project,diag.GetConnections()[i],zipfile)
                #RelationshipGenerator.GenerateRelationship(self.projectname,diag.GetConnections()[i],zipfile) 
          
    def ValidateDomains(self):
        '''
        defines domain validation 
        '''
        for diag in self.project.GetRoot().GetDiagrams():
            if (len(diag.GetElements())==0):
                #tu by mala byt hlaska o tom, ze nemame co generovat
                WarningDialog("Some diagram is empty. Each one requires at least one Object.")
                return False
            #validacia porovnanim, ci mame pre domenu iba jednu definiciu a ostatne pripadne rovnako nazvane elementy su iba zastupcovia
            for el in diag.GetElements():
                #print el.GetObject().GetType()=="Object"
                if (el.GetObject().GetType()=="Object"):
                    el.GetObject().GetValue(OBJ_IDENTITY)
                    #TU POKRACUJ
                
        return True 
    
    def __GenerateDirectories(self,projectname):
        '''
        when output is directly into filesystem, system of directories is this way created
        '''
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
        
        