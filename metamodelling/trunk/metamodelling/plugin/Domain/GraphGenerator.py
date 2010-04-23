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

IDENTITY = "name"
PROP_IDENTITY = "properties"
NMS_METAMODEL = "http://umlfri.kst.fri.uniza.sk/xmlschema/metamodel.xsd"
XML_HEAD = "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n"
ICON_PATH = "icons/"
META_IDENTITY = "visual_identity"

class GraphGenerator(object):
       
    def GenerateGraph(projectname,obj,zipfile=None):
        
        A = ElementMaker(namespace=NMS_METAMODEL,
                          nsmap={None : NMS_METAMODEL})
        object = A.DiagramType()
          
        identity = obj.GetValue(IDENTITY)
        object.set("id",identity)
        
        icon = A.Icon()
        icon.set("path",ICON_PATH+identity+".png")
        object.append(icon)
        
        domain = A.Domain()
        #tu treba dat domenu 
        domain.set("id","SimpleDiagram") 
        domain.set("identity","name")
        object.append(domain)
        
        special = A.Special()
        special.set("swimlines","0")
        special.set("lifelines","0")
        object.append(special)
        
        elements = A.Elements()
        for el in GraphGenerator.__GetUniqueObjectsFromDiagram(obj):
            newEl = A.Item()
            newEl.set("value",el.GetValue(META_IDENTITY))
            elements.append(newEl)
        
        object.append(elements)
        
        connections = A.Connections()
        for el in GraphGenerator.__GetUniqueRelationshipsFromDiagram(obj):
            newC = A.Item()
            newC.set("value",el.GetValue(META_IDENTITY))
            connections.append(newC)
            
        object.append(connections)    
        
        if (zipfile is not None):
            zipfile.writestr("metamodel/diagrams/"+identity+".xml", tostring(object,encoding=None,method="xml",pretty_print=True))
            return
            
        print(tostring(object,encoding=None,method="xml",pretty_print=True))
        f = open(addonPath+projectname+"/metamodel/diagrams/"+identity+".xml","w");
        f.write(XML_HEAD)
        f.writelines(tostring(object,encoding=None,method="xml",pretty_print=True))
        f.close()
     
    #staticka metoda    
    GenerateGraph = Callable(GenerateGraph)    
    
    def __GetUniqueObjectsFromDiagram(diag):
        #v buducnosti z toho moze byt aj filter, pripadne validator, minimalne ak pridam ine elementy
        mydict = dict()
        for it in diag.GetElements():
            if (it.GetObject().GetType()=="Object"):
                if (mydict.has_key(it.GetObject().GetValue(META_IDENTITY))==False):
                    mydict[it.GetObject().GetValue(META_IDENTITY)]=it.GetObject()
                #mydict.items().append(eval('{\"it.GetObject().GetValue(META_IDENTITY)\":it.GetObject()}'))        
        return mydict.values() 
    
    __GetUniqueObjectsFromDiagram = Callable(__GetUniqueObjectsFromDiagram)
    
    def __GetUniqueRelationshipsFromDiagram(diag):     
        #v buducnosti z toho moze byt aj filter, pripadne validator, minimalne ak pridam ine spojenia
        mydict = dict()
        for it in diag.GetConnections():
            if (mydict.has_key(it.GetObject().GetValue(META_IDENTITY))==False):
                mydict[it.GetObject().GetValue(META_IDENTITY)]=it.GetObject()
                #mydict.items().append(eval('{\"it.GetObject().GetValue(META_IDENTITY)\":it.GetObject()}'))        
        return mydict.values()
    
    __GetUniqueRelationshipsFromDiagram = Callable(__GetUniqueRelationshipsFromDiagram)