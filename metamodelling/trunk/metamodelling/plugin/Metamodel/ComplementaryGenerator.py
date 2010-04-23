'''
Created on 19.4.2010

@author: Michal Kovacik
'''
from lib.Exceptions import *
from __init__ import *
from lxml.etree import tostring
from lxml.builder import ElementMaker
from AppearanceGenerator import AppearanceGenerator
import shutil, os

addonPath = "share/addons/"

class Callable:
    def __init__(self, anycallable):
        self.__call__ = anycallable

OBJ_IDENTITY = "object_name"
PROP_IDENTITY = "properties"
NMS_METAMODEL = "http://umlfri.kst.fri.uniza.sk/xmlschema/metamodel.xsd"
NMS_ADDON = "http://umlfri.org/xmlschema/addon.xsd"
NMS_UMLPROJECT = "http://umlfri.kst.fri.uniza.sk/xmlschema/umlproject.xsd"

XML_HEAD = "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n"
ENUM_VALUES = "values"
ENUM_VALUE = "value"
ENUM_IDENTITY = "enum_name"
DOMAIN_IDENTITY = "domain_name"
MY_PLUGIN_NAME="metamodelling"
SAMPLE_DOMAIN_ID="SimpleDiagram"

class ComplementaryGenerator(object):
       
    def GenerateMetamodelFile(projectname,diagrams,zipfile=None):
        
        A = ElementMaker(namespace=NMS_METAMODEL,
                          nsmap={None : NMS_METAMODEL})
        object = A.Metamodel()
        
        diags = A.Diagrams()
        for diagname in diagrams:
            newItem = A.Item()
            newItem.set("value",diagname)
            diags.append(newItem)
        object.append(diags)
               
        if (zipfile is not None):
            zipfile.writestr("metamodel/metamodel.xml", tostring(object,encoding=None,method="xml",pretty_print=True))
            return
               
        #print(tostring(object,encoding=None,method="xml",pretty_print=True))
        f = open(addonPath+projectname+"/metamodel/metamodel.xml","w");
        f.write(XML_HEAD)
        f.writelines(tostring(object,encoding=None,method="xml",pretty_print=True))
        f.close()
     
    #staticka metoda    
    GenerateMetamodelFile = Callable(GenerateMetamodelFile)    
    
    def CopyPaths(projectname,zipfile=None):
        if (zipfile is not None):
            zipfile.write(addonPath+"/"+MY_PLUGIN_NAME+"/metamodel/paths.xml", "metamodel/paths.xml")
            return
        
        shutil.copy(addonPath+"/"+MY_PLUGIN_NAME+"/metamodel/paths.xml", addonPath+"/"+projectname+"/metamodel/paths.xml")
    
    CopyPaths = Callable(CopyPaths)
    
    def CopySampleDomain(projectname,zipfile=None):
        if (zipfile is not None):
            zipfile.write(addonPath+"/"+MY_PLUGIN_NAME+"/metamodel/domains/"+SAMPLE_DOMAIN_ID+".xml", "metamodel/domains/"+SAMPLE_DOMAIN_ID+".xml")
            return
        
        shutil.copy(addonPath+"/"+MY_PLUGIN_NAME+"/metamodel/domains/"+SAMPLE_DOMAIN_ID+".xml", addonPath+"/"+projectname+"/metamodel/domains/"+SAMPLE_DOMAIN_ID+".xml")
    
    CopySampleDomain = Callable(CopySampleDomain)
    
    def CopyDummyGraphIcon(projectname,graphs,zipfile=None):
        for gr in graphs:
            if (zipfile is not None):
                zipfile.write(addonPath+"/"+MY_PLUGIN_NAME+"/icons/sampleGraph.png","metamodel/icons/"+gr+".png")
                return
            
            shutil.copy(addonPath+"/"+MY_PLUGIN_NAME+"/icons/sampleGraph.png",addonPath+"/"+projectname+"/metamodel/icons/"+gr+".png")
    
    CopyDummyGraphIcon = Callable(CopyDummyGraphIcon)
    
    def CopyDummyObjectIcon(projectname,el,zipfile=None):
        if (zipfile is not None):
            zipfile.write(addonPath+"/"+MY_PLUGIN_NAME+"/icons/sampleDomain.png","metamodel/icons/"+el+".png")
            return
        
        shutil.copy(addonPath+"/"+MY_PLUGIN_NAME+"/icons/sampleDomain.png", addonPath+"/"+projectname+"/metamodel/icons/"+el+".png")
        
    CopyDummyObjectIcon = Callable(CopyDummyObjectIcon)  
    
    def CopyDummyRelationshipIcon(projectname,el,zipfile=None):
        if (zipfile is not None):
            zipfile.write(addonPath+"/"+MY_PLUGIN_NAME+"/icons/sampleRelationship.png","metamodel/icons/"+el+".png")
            return
        
        shutil.copy(addonPath+"/"+MY_PLUGIN_NAME+"/icons/sampleRelationship.png", addonPath+"/"+projectname+"/metamodel/icons/"+el+".png")
        
    CopyDummyRelationshipIcon = Callable(CopyDummyRelationshipIcon)  
    
    def CopyDummyProjectIcon(projectname,zipfile=None):
        if (zipfile is not None):
            zipfile.write(addonPath+"/"+MY_PLUGIN_NAME+"/icons/sampleIcon.png","icons/"+projectname+".png")
            return
        
        shutil.copy(addonPath+"/"+MY_PLUGIN_NAME+"/icons/sampleIcon.png", addonPath+"/"+projectname+"/icons/"+projectname+".png")
        
    CopyDummyProjectIcon = Callable(CopyDummyProjectIcon)
    
    def CopyPackageItems(projectname,zipfile=None):
        if (zipfile is not None):
            zipfile.write(addonPath+"/"+MY_PLUGIN_NAME+"/metamodel/icons/Package.png","metamodel/icons/Package.png")
            zipfile.write(addonPath+"/"+MY_PLUGIN_NAME+"/metamodel/domains/Package.xml","metamodel/domains/Package.xml")
            zipfile.write(addonPath+"/"+MY_PLUGIN_NAME+"/metamodel/elements/Package.xml","metamodel/elements/Package.xml")
            return
        
        shutil.copy(addonPath+"/"+MY_PLUGIN_NAME+"/metamodel/icons/Package.png",addonPath+"/"+projectname+"/metamodel/icons/Package.png")
        shutil.copy(addonPath+"/"+MY_PLUGIN_NAME+"/metamodel/domains/Package.xml",addonPath+"/"+projectname+"/metamodel/domains/Package.xml")
        shutil.copy(addonPath+"/"+MY_PLUGIN_NAME+"/metamodel/elements/Package.xml",addonPath+"/"+projectname+"/metamodel/elements/Package.xml")
    
    CopyPackageItems = Callable(CopyPackageItems)
    
    def GenerateTemplate(projectname,zipfile=None):
        A = ElementMaker(namespace=NMS_UMLPROJECT,
                          nsmap={None : NMS_UMLPROJECT})
        
        object = A.umlproject()
        object.set("saveversion","1.0.1")
        
        metamodel = A.metamodel()
        uri = A.uri()
        uri.text = "urn:umlfri.org:metamodel:"+projectname
        version = A.version()
        version.text = "0.1"
        metamodel.append(uri)
        metamodel.append(version)
        object.append(metamodel)
        
        #basic_package
        objects = A.objects()
        obj = A.object()
        obj.set("type","Package")
        obj.set("id","0")
        dictio = A.dict()
        conttext = A.text()
        conttext.set("name","note")
        scopetext = A.text()
        scopetext.set("name","scope")
        scopetext.text="Private"
        abstracttext = A.text()
        abstracttext.set("name","abstract")
        abstracttext.text="False"
        nametext = A.text()
        nametext.set("name","name")
        nametext.text="Project"
        stereotext = A.text()
        stereotext.set("name","stereotype")
        
        dictio.append(conttext)
        dictio.append(scopetext)
        dictio.append(abstracttext)
        dictio.append(nametext)
        dictio.append(stereotext)
        obj.append(dictio)
        objects.append(obj)
        object.append(objects)
        
        conns = A.connections()
        object.append(conns)
        
        projtree = A.projecttree()
        prnode = A.node()
        prnode.set("id","0")
        prdiagrams = A.diagrams()
        prnode.append(prdiagrams)
        projtree.append(prnode)
        object.append(projtree)
        
        counters = A.counters()
        countobj = A.count()
        countobj.set("id","Package")
        countobj.set("value","0")
        counters.append(countobj)
        object.append(counters)
        
        if (zipfile is not None):
            zipfile.writestr("templates/empty.fritx", tostring(object,encoding=None,method="xml",pretty_print=True))
            return
        
        f = open(addonPath+projectname+"/templates/empty.fritx","w");
        f.write(XML_HEAD)
        f.writelines(tostring(object,encoding=None,method="xml",pretty_print=True))
        f.close()
    
    GenerateTemplate = Callable(GenerateTemplate)
    
    def GenerateAddon(projectname,zipfile=None):
        A = ElementMaker(namespace=NMS_ADDON,
                          nsmap={None : NMS_ADDON})
        
        object = A.AddOn()
        identity = A.Identity()
        identity.set("uri","urn:umlfri.org:metamodel:"+projectname)
        #old identity is for backward compatibility
        identityOld = A.Identity()
        identityOld.set("uri","http://umlfri.kst.fri.uniza.sk/metamodel/"+projectname+".frim")
        
        object.append(identity)
        object.append(identityOld)
        
        friendlyname = A.FriendlyName()
        friendlyname.set("name",projectname)
        friendlyname.set("version","1.0.0")
        object.append(friendlyname)
        
        author = A.Author()
        authorname = A.Name()
        authorname.set("name","Metamodelling engine(add your name here)")
        
        homepage = A.Homepage()
        homepage.set("url","http://umlfri.org")
        
        commonlic = A.CommonLicense()
        commonlic.set("name","GPL-2")
        
        author.append(authorname)
        author.append(homepage)
        author.append(commonlic)
        
        object.append(author)
        
        icon = A.Icon()
        icon.set("path","icons/"+projectname+".png")
        
        object.append(icon)
        
        description = A.Description()
        description.text = "This module was automatically generated using Metamodelling plugin"
        object.append(description)
        
        metamodel = A.Metamodel()
        path = A.Path()
        path.set("path","metamodel")
        metamodel.append(path)
        object.append(metamodel)
        
        template=A.Template()
        template.set("path","templates/empty.fritx")
        template.set("name","Empty diagram")
        
        metamodel.append(template)
        
        if (zipfile is not None):
            zipfile.writestr("addon.xml", tostring(object,encoding=None,method="xml",pretty_print=True))
            return
        
        f = open(addonPath+projectname+"/addon.xml","w");
        f.write(XML_HEAD)
        f.writelines(tostring(object,encoding=None,method="xml",pretty_print=True))
        f.close()
    
    GenerateAddon = Callable(GenerateAddon)
    
    
    