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

NMS_METAMODEL = "http://umlfri.kst.fri.uniza.sk/xmlschema/metamodel.xsd"
XML_HEAD = "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n"
DOMAIN_IDENTITY = "name"

class ObjectVisualGenerator(object):
       
    def GenerateObject(projectname,visual_identity,treemodel,domainname,relationships,zipfile=None):
        
        A = ElementMaker(namespace=NMS_METAMODEL,
                          nsmap={None : NMS_METAMODEL})
        object = A.ElementType()
            
        object.set("id",visual_identity)
        
        icon = A.Icon()
        icon.set("path","icons/"+visual_identity+".png")
        object.append(icon)
        
        domain = A.Domain()
        domain.set("id",domainname)
        domain.set("identity",DOMAIN_IDENTITY)
        object.append(domain)
        
        rel = A.Connections()
        for it in relationships:
            newrel = A.Item()
            newrel.set("value",it)
            rel.append(newrel)
        
        object.append(rel)
        
        a = AppearanceGenerator()
        a.SetTreeView(treemodel)
        appearance = A.Appearance()
        appearance.append(AppearanceGenerator().GenerateXML(fileOutput=True))
        object.append(appearance)
           
        if (zipfile is not None):
            zipfile.writestr("metamodel/elements/"+visual_identity+".xml", tostring(object,encoding=None,method="xml",pretty_print=True))
            return
                   
        #print(tostring(object,encoding=None,method="xml",pretty_print=True))
        f = open(addonPath+projectname+"/metamodel/elements/"+visual_identity+".xml","w");
        f.write(XML_HEAD)
        f.writelines(tostring(object,encoding=None,method="xml",pretty_print=True))
        f.close()
     
    #staticka metoda    
    GenerateObject = Callable(GenerateObject)    
    
    