'''
Created on 19.4.2010

@author: Michal Kovacik
'''
from lib.Exceptions import *
import random
from __init__ import *
from lxml.etree import tostring
from lxml.builder import ElementMaker
from AppearanceGenerator import AppearanceGenerator

addonPath = "share/addons/"

class Callable:
    def __init__(self, anycallable):
        self.__call__ = anycallable

OBJ_IDENTITY = "object_name"
PROP_IDENTITY = "properties"
NMS_METAMODEL = "http://umlfri.kst.fri.uniza.sk/xmlschema/metamodel.xsd"
XML_HEAD = "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n"
ENUM_VALUES = "values"
ENUM_VALUE = "value"
ENUM_IDENTITY = "enum_name"
DOMAIN_IDENTITY = "domain_name"

class RelationshipVisualGenerator(object):
       
    def GenerateRelationship(projectname,visual_identity,treemodel,domainname,zipfile=None):
        
        A = ElementMaker(namespace=NMS_METAMODEL,
                          nsmap={None : NMS_METAMODEL})
        object = A.ConnectionType()
            
        object.set("id",visual_identity)
        
        icon = A.Icon()
        icon.set("path","icons/"+visual_identity+".png")
        object.append(icon)
        
        domain = A.Domain()
        domain.set("id",domainname)
        domain.set("identity",DOMAIN_IDENTITY)
        object.append(domain)
        
        a = AppearanceGenerator()
        a.SetTreeView(treemodel)
        
        object.append(AppearanceGenerator().GenerateRelationshipXML(fileOutput=True))
        
        if (zipfile is not None):
            zipfile.writestr("metamodel/connections/"+visual_identity+".xml", tostring(object,encoding=None,method="xml",pretty_print=True))
            return
               
        #print(tostring(object,encoding=None,method="xml",pretty_print=True))
        f = open(addonPath+projectname+"/metamodel/connections/"+visual_identity+".xml","w");
        f.write(XML_HEAD)
        f.writelines(tostring(object,encoding=None,method="xml",pretty_print=True))
        f.close()
     
    #staticka metoda    
    GenerateRelationship = Callable(GenerateRelationship)    
    
    