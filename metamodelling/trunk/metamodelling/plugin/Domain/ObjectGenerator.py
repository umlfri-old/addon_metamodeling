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
REL_IDENTITY = "relationship_name"
PROP_IDENTITY = "properties"
NMS_METAMODEL = "http://umlfri.kst.fri.uniza.sk/xmlschema/metamodel.xsd"
XML_HEAD = "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n"
ENUM_VALUES = "values"
ENUM_VALUE = "value"
ENUM_IDENTITY = "enum_name"
DOMAIN_IDENTITY = "domain_name"

class ObjectGenerator(object):
       
    def GenerateObject(projectname,project,obj,zipfile=None):
        
        A = ElementMaker(namespace=NMS_METAMODEL,
                          nsmap={None : NMS_METAMODEL})
        object = A.Domain()
        
        if (obj.GetObject().GetType()=="Object"):    
            identity = obj.GetObject().GetValue(OBJ_IDENTITY)
        elif (obj.GetObject().GetType()=="Relationship"):
            identity = obj.GetObject().GetValue(REL_IDENTITY)    
        object.set("id",identity)
        
        domain_name = A.Attribute()
        domain_name.set("id","name")
        domain_name.set("name","Name")
        domain_name_str = A.Str()
        domain_name.append(domain_name_str)
        object.append(domain_name)
        
        prop_dict = eval(obj.GetObject().GetValue(PROP_IDENTITY))
        for els in prop_dict:
            type = els.get("type")
            role = els.get("role")
            name = els.get("name")
            default = els.get("default")
            if (type=="str"):
                if (default == ""):
                    object.append(ObjectGenerator.__GenerateStr(A,name))
                else: object.append(ObjectGenerator.__GenerateStr(A,name,default))
            elif (type=="text"):
                if (default == ""):
                    object.append(ObjectGenerator.__GenerateText(A,name))
                else: object.append(ObjectGenerator.__GenerateText(A,name,default))
            elif (type=="int"):
                if (default == ""):
                    object.append(ObjectGenerator.__GenerateInt(A,name))
                else: object.append(ObjectGenerator.__GenerateInt(A,name,default))        
            elif (type=="float"):
                if (default == ""):
                    object.append(ObjectGenerator.__GenerateFloat(A,name))
                else: object.append(ObjectGenerator.__GenerateFloat(A,name,default))
            elif (type=="bool"):
                if (default == ""):
                    object.append(ObjectGenerator.__GenerateBool(A,name))
                else: object.append(ObjectGenerator.__GenerateBool(A,name,default))
            elif (type=="enum"):
                if (ObjectGenerator.__GenerateEnum(A,name,role,project) is not None):
                    if (default == ""):
                        object.append(ObjectGenerator.__GenerateEnum(A,name,role,project))
                    else: object.append(ObjectGenerator.__GenerateEnum(A,name,role,project,default))    
            elif (type=="domain"):
                if (ObjectGenerator.__GenerateDomain(A,name,role,project) is not None):
                    if (default == ""):
                        object.append(ObjectGenerator.__GenerateDomain(A,name,role,project))
                    else: object.append(ObjectGenerator.__GenerateDomain(A,name,role,project,default))
        
        #for notes card purpose
        note = A.Attribute()
        note.set("id","note")
        note.set("name","Note")
        txtNote = A.Text()
        note.append(txtNote)
        object.append(note)
        
        if (zipfile is not None):
            zipfile.writestr("metamodel/domains/"+identity+".xml", tostring(object,encoding=None,method="xml",pretty_print=True))
            return
        
        #print(tostring(object,encoding=None,method="xml",pretty_print=True))
        f = open(addonPath+projectname+"/metamodel/domains/"+identity+".xml","w");
        f.write(XML_HEAD)
        f.writelines(tostring(object,encoding=None,method="xml",pretty_print=True))
        f.close()
     
    #staticka metoda    
    GenerateObject = Callable(GenerateObject)    
    
    def __GenerateStr(A,name,default=None):
        newatt = A.Attribute()
        newatt.set("id",name)
        newatt.set("name",name)
        typeTag = A.Str()
        if (default is not None): typeTag.set("default",default)
        newatt.append(typeTag)
        return newatt
    
    def __GenerateText(A,name,default=None):
        newatt = A.Attribute()
        newatt.set("id",name)
        newatt.set("name",name)
        typeTag = A.Text()
        if (default is not None): typeTag.set("default",default)
        newatt.append(typeTag)
        return newatt
    
    def __GenerateInt(A,name,default=None):
        newatt = A.Attribute()
        newatt.set("id",name)
        newatt.set("name",name)
        typeTag = A.Int()
        if (default is not None): typeTag.set("default",default)
        newatt.append(typeTag)
        return newatt
    
    def __GenerateFloat(A,name,default=None):
        newatt = A.Attribute()
        newatt.set("id",name)
        newatt.set("name",name)
        typeTag = A.Float()
        if (default is not None): typeTag.set("default",default)
        newatt.append(typeTag)
        return newatt
    
    def __GenerateBool(A,name,default=None):
        newatt = A.Attribute()
        newatt.set("id",name)
        newatt.set("name",name)
        typeTag = A.Bool()
        if (default is not None): typeTag.set("default",default)
        newatt.append(typeTag)
        return newatt
    
    def __GenerateEnum(A,name,role,project,default=None):
        newatt = A.Attribute()
        if (role != "") : 
            newatt.set("id",role)
            newatt.set("name",role)
        else: 
            newatt.set("id",name)
            newatt.set("name",name)
        typeTag = A.Enum()
        if (default is not None): typeTag.set("default",default)
        en = None
        for diag in project.GetRoot().GetDiagrams():     
            for i in range(0,len(diag.GetElements())):
                if ((diag.GetElements()[i].GetObject().GetType()=="Enum")and(diag.GetElements()[i].GetObject().GetValue(ENUM_IDENTITY)==name)):
                    en = diag.GetElements()[i].GetObject()
        
        if (en is None): return            
        prop_dict = eval(en.GetValue(ENUM_VALUES))
        for i in prop_dict:
            val = A.Value()
            print i
            val.text = i.get(ENUM_VALUE)
            typeTag.append(val)
        
        newatt.append(typeTag)
        return newatt    
    
    def __GenerateDomain(A,name,role,project,default=None):
        newatt = A.Attribute()  
        if (role != "") : 
            newatt.set("id",role)
            newatt.set("name",role)
        else: 
            newatt.set("id",name)
            newatt.set("name",name)
        newattList = A.List()
        typeTag = A.Domain()
        
        for diag in project.GetRoot().GetDiagrams():     
            for i in range(0,len(diag.GetElements())):
                if ((diag.GetElements()[i].GetObject().GetType()=="Domain")and(diag.GetElements()[i].GetObject().GetValue(DOMAIN_IDENTITY)==name)):
                    dom = diag.GetElements()[i].GetObject()
        
        #typeTag.append(ObjectGenerator.__GenerateSubDomain(A,name,project,dom,typetag))            
        ObjectGenerator.__GenerateSubDomain(A,name,role,project,dom,typeTag)
        newatt.append(newattList)
        newattList.append(typeTag)
        return newatt
        
    def __GenerateSubDomain(A,name,role,project,domain,object):
        prop_dict = eval(domain.GetValue(PROP_IDENTITY))
        for els in prop_dict:
            type = els.get("type")
            name = els.get("name")
            role = els.get("role")
            default = els.get("default")
            if (type=="str"):
                if (default == ""):
                    object.append(ObjectGenerator.__GenerateStr(A,name))
                else: object.append(ObjectGenerator.__GenerateStr(A,name,default))
            elif (type=="text"):
                if (default == ""):
                    object.append(ObjectGenerator.__GenerateText(A,name))
                else: object.append(ObjectGenerator.__GenerateText(A,name,default))
            elif (type=="int"):
                if (default == ""):
                    object.append(ObjectGenerator.__GenerateInt(A,name))
                else: object.append(ObjectGenerator.__GenerateInt(A,name,default))        
            elif (type=="float"):
                if (default == ""):
                    object.append(ObjectGenerator.__GenerateFloat(A,name))
                else: object.append(ObjectGenerator.__GenerateFloat(A,name,default))
            elif (type=="bool"):
                if (default == ""):
                    object.append(ObjectGenerator.__GenerateBool(A,name))
                else: object.append(ObjectGenerator.__GenerateBool(A,name,default))
            elif (type=="enum"):
                if (ObjectGenerator.__GenerateEnum(A,name,role,project) is not None):
                    if (default == ""):
                        object.append(ObjectGenerator.__GenerateEnum(A,name,role,project))
                    else: object.append(ObjectGenerator.__GenerateEnum(A,name,role,project,default))    
            elif (type=="domain"):
                if (ObjectGenerator.__GenerateDomain(A,name,role,project) is not None):
                    if (default == ""):
                        object.append(ObjectGenerator.__GenerateDomain(A,name,role,project))
                    else: object.append(ObjectGenerator.__GenerateDomain(A,name,role,project,default))
    
    __GenerateStr = Callable(__GenerateStr)       
    __GenerateText = Callable(__GenerateText)
    __GenerateInt = Callable(__GenerateInt) 
    __GenerateFloat = Callable(__GenerateFloat)
    __GenerateBool = Callable(__GenerateBool)
    __GenerateEnum = Callable(__GenerateEnum)   
    __GenerateDomain = Callable(__GenerateDomain)
    __GenerateSubDomain = Callable(__GenerateSubDomain)