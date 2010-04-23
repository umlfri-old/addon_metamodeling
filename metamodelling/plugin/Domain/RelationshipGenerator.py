'''
Created on 23.3.2010

@author: Michal Kovacik
'''
from lib.Exceptions import *
from __init__ import *
from lxml.etree import tostring
from lxml.builder import ElementMaker

addonPath = "share/addons/"

class Callable:
    def __init__(self, anycallable):
        self.__call__ = anycallable

REL_IDENTITY = "relationship_name"
PROP_IDENTITY = "properties"
NMS_METAMODEL = "http://umlfri.kst.fri.uniza.sk/xmlschema/metamodel.xsd"
XML_HEAD = "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n"

class RelationshipGenerator(object):
       
    def GenerateRelationship(projectname,obj,zipfile=None):
        
        A = ElementMaker(namespace=NMS_METAMODEL,
                          nsmap={None : NMS_METAMODEL})
        object = A.Domain()
            
        identity = obj.GetObject().GetValue(REL_IDENTITY)
        object.set("id",identity)
        
        prop_dict = eval(obj.GetObject().GetValue(PROP_IDENTITY))
        for els in prop_dict:
            print els
            type = els.get("type")
            name = els.get("name")
            newatt = A.Attribute()
            newatt.set("type",type)
            newatt.set("name",name)
            object.append(newatt)
        
        if (zipfile is not None):
            zipfile.writestr("metamodel/domains/"+identity+".xml", tostring(object,encoding=None,method="xml",pretty_print=True))
            return
        
        print(tostring(object,encoding=None,method="xml",pretty_print=True))
        f = open(addonPath+projectname+"/metamodel/domains/"+identity+".xml","w");
        f.write(XML_HEAD)
        f.writelines(tostring(object,encoding=None,method="xml",pretty_print=True))
        f.close()
     
    #staticka metoda    
    GenerateRelationship = Callable(GenerateRelationship)    
           
        