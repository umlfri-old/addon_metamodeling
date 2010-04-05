'''
Created on 22.3.2010

@author: Michal Kovacik
'''
from lib.Exceptions import *
import random
from __init__ import *
from lxml.etree import tostring
from lxml.builder import ElementMaker

addonPath = "share/addons/"

class Callable:
    def __init__(self, anycallable):
        self.__call__ = anycallable

OBJ_IDENTITY = "object_name"
PROP_IDENTITY = "properties"
NMS_METAMODEL = "http://umlfri.kst.fri.uniza.sk/xmlschema/metamodel.xsd"
XML_HEAD = "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n"

class AppearanceGenerator(object):
    
    #malo by jednoduchu elipsu nakreslit
    def DummyObject():
        A = ElementMaker(namespace=NMS_METAMODEL,
                          nsmap={None : NMS_METAMODEL})
        
        object = A.Appearance()
        ell = A.Ellipse()
        ell.set("fill","#cfg.Styles.Element.FillColor")
        ell.set("border","#cfg.Styles.Element.LineColor")
        object.append(ell)
        
        tbx = A.TextBox()
        tbx.set("color","black")
        tbx.set("text","texttext")
        tbx.set("font","Arial 10")
        #return object
        #return ell
        return tbx
    
    #staticka metoda    
    DummyObject = Callable(DummyObject) 
       
    def GenerateObject(projectname,obj):
        
        A = ElementMaker(namespace=NMS_METAMODEL,
                          nsmap={None : NMS_METAMODEL})
        object = A.Domain()
        
        #attrib = obj.GetObject().GetSaveInfo()
        #print attrib
        #attrkeys = attrib.keys()
        #print attrkeys
        #for i in attrkeys:
        #    atgen = A.Attribute()
        #    atgen.set(i,attrkeys.get(i))
        #    object.append(atgen)
            
        identity = obj.GetObject().GetValue(OBJ_IDENTITY)
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
        
        print(tostring(object,encoding=None,method="xml",pretty_print=True))
        f = open(addonPath+projectname+"/metamodel/domains/"+identity+".xml","w");
        f.write(XML_HEAD)
        f.writelines(tostring(object,encoding=None,method="xml",pretty_print=True))
        f.close()
     
    #staticka metoda    
    GenerateObject = Callable(GenerateObject)    
           
        