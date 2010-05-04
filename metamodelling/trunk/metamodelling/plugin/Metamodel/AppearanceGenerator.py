'''
Created on 22.3.2010

@author: Michal Kovacik
'''
from lib.Exceptions import *
import random
from __init__ import *
from lxml.etree import tostring
from lxml.builder import ElementMaker
from lib.Drawing.Objects import ALL, ALL_CONNECTION, CContainer,CSimpleContainer
from lib.Connections.Type import CConnectionType
from lib.Drawing.Context import BuildParam

addonPath = "share/addons/"

class Callable:
    def __init__(self, anycallable):
        self.__call__ = anycallable

OBJ_IDENTITY = "object_name"
PROP_IDENTITY = "properties"
NMS_METAMODEL = "http://umlfri.kst.fri.uniza.sk/xmlschema/metamodel.xsd"
XML_HEAD = "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n"

class Singleton(type):
    '''
    Singleton is a type matching the Singleton design pattern
    '''
    def __init__(cls, name, bases, dict):
        super(Singleton, cls).__init__(name, bases, dict)
        cls.instance = None
 
    def __call__(cls, *args, **kw):
        if cls.instance is None:
            cls.instance = super(Singleton, cls).__call__(*args, **kw)
 
        return cls.instance

class AppearanceGenerator(object):
    '''
    AppearanceGenerator is a Singleton class.
    It is used to transform Tree stores into XML or generate XML layout for sample object.
    Also other transformations from Tree store data into XML is in this class competence.
    '''
    __metaclass__ = Singleton
    def __init__(self):
        self.model=None
        
    def SetTreeView(self,treestore):
        '''
        this method is important to be launched at least once
        
        @param treestore: treestore object which is set as model
        @type treestore: L{gtk.TreeStore<gtk.TreeStore>}
        '''
        self.model = treestore
    
    def GenerateSampleRounded(self):
        '''
        this method should create a simple ellipse with "sample" caption
        '''
        A = ElementMaker(namespace=NMS_METAMODEL,
                          nsmap={None : NMS_METAMODEL})
         
        object = A.Shadow()
        object.set("padding","3")
        object.set("color","#cfg.Styles.Element.ShadowColor")
        
        
        ell = A.Ellipse()
        ell.set("fill","#cfg.Styles.Element.FillColor")
        ell.set("border","#cfg.Styles.Element.LineColor")
        object.append(ell)
        
        pdi = A.Padding()
        pdi.set("padding","8")
        ell.append(pdi)
        
        tbx = A.TextBox()
        tbx.set("color","black")
        tbx.set("text","sample")
        tbx.set("font","Arial 10")
        pdi.append(tbx)
        return object
        
    
    def GetXMLElement(self,iterroot,A,fileOutput=False):
        '''
        this method gets subelement of iterroot
        it has two variants (one is preview mode(fileOutput=False) and one is mode used for file output(fileOutput=True))
        
        @return: xml from iter
        @rtype: string
        '''
        rootobj = self.model.get_value(iterroot,1)
        root = A(rootobj.Identity())
        attr = rootobj.GetAttributes().items()
        for it in attr:
            key, val = it
            if (val!=""):
                val = str(val)
                valSplit = val.split("|")
                if fileOutput: root.set(key,valSplit[0])
                elif ((not fileOutput)and(val[:5]=="#self")): 
                    if (len(valSplit)>1):
                        root.set(key,valSplit[1])
                    else: root.set(key,val[1:])  
                elif (not fileOutput): 
                    if (len(valSplit)>1):
                        root.set(key,valSplit[1])
                    else: root.set(key,val)     
        
        if self.model.iter_children(iterroot) is not None:
            first = self.model.iter_children(iterroot)
            #object = self.model.get_value(first,1)
            while first is not None:
                root.append(self.GetXMLElement(first,A,fileOutput))
                first=self.model.iter_next(first)

        return root
    
    def GenerateRelationshipXML(self,fileOutput=False):
        '''
        Generates whole XML visual definition for relationship by the model currently set
        it supports multiple trees (forest)
        '''
        A = ElementMaker(namespace=NMS_METAMODEL,
                         nsmap={None : NMS_METAMODEL}) 
       
        iterroot = self.model.get_iter_root()
        if iterroot is None: return
        if self.model.iter_next(iterroot) is not None:
            root = A.Appearance()
            while iterroot is not None:
                root.append(self.GetXMLElement(iterroot, A,fileOutput))
                iterroot=self.model.iter_next(iterroot)

            return root 
        else:
            root = A.Appearance()
            root.append(self.GetXMLElement(iterroot,A,fileOutput))
            return root
           
       
    def GenerateXML(self,fileOutput=False):
        '''
        Generates whole XML visual definition for object by the model currently set
        it requires only a tree representation
        '''
        A = ElementMaker(namespace=NMS_METAMODEL,
                          nsmap={None : NMS_METAMODEL})
          
        
        iterroot = self.model.get_iter_root()
        if iterroot is None: return
        rootobj = self.model.get_value(iterroot,1)
        root = A(rootobj.Identity())
        attr = rootobj.GetAttributes().items()
        for it in attr:
            key, val = it
            if (val!=""):
                val = str(val)
                valSplit = val.split("|")
                if fileOutput: root.set(key,valSplit[0])
                elif ((not fileOutput)and(val[:5]=="#self")): 
                    if (len(valSplit)>1):
                        root.set(key,valSplit[1])
                    else: root.set(key,val[1:])  
                elif (not fileOutput): 
                    if (len(valSplit)>1):
                        root.set(key,valSplit[1])
                    else: root.set(key,val)              
        
        if self.model.iter_children(iterroot) is not None:
            first = self.model.iter_children(iterroot)
            #object = self.model.get_value(first,1)
            while first is not None:
                root.append(self.GetXMLElement(first,A,fileOutput))
                first=self.model.iter_next(first)
        
        return root
    
    def DummyRelationshipAppearance(self,root):
        '''
        This is like __LoadAppearance of CConnection base class.
        it processes XML and generates visual object representing the Relationship tree
        '''
        tagName = root.tag.split("}")[1]
        
        if tagName not in ALL_CONNECTION:
            raise FactoryError("XMLError", root.tag)
        
        cls = ALL_CONNECTION[tagName]
        
        params = {}
        for attr in root.attrib.items():
            params[attr[0]] = BuildParam(attr[1], cls.types.get(attr[0], None))
        ret = obj = cls(**params)
        
        if hasattr(obj, "LoadXml"):
            obj.LoadXml(root)
        else:
            if len(root) > 1 and isinstance(obj, CSimpleContainer):
                tmp = CContainer()
                obj.SetChild(tmp)
                obj = tmp
            for child in root:
                obj.AppendChild(self.DummyRelationshipAppearance(child))
        return ret 
    
    def DummyObjectAppearance(self,root):
        '''
        this is like __LoadAppearance of Element
        it processes XML and generates visual object representing the Object tree
        '''
        if root.tag.split("}")[1] not in ALL:
            raise FactoryError("XMLError", root.tag)
        cls = ALL[root.tag.split("}")[1]]
        params = {}
        for attr in root.attrib.items():    #return e.g. attr == ('id', '1') => attr[0] == 'id', attr[1] == '1'
            params[attr[0]] = BuildParam(attr[1], cls.types.get(attr[0], None))
        obj = cls(**params)
        if hasattr(obj, "LoadXml"):
            obj.LoadXml(root)
        else:
            for child in root:
                obj.AppendChild(self.DummyObjectAppearance(child))
        return obj
    
    def DummyRelationshipProcesser(self,root,domain,a):
        '''
        this method encapsulates DummyRelationshipAppearance method and DummyLabelAppearance
        to generate Appearance part and Label parts
        '''
        visualObj = CContainer()
        labels=[]
        for child in root:
            if child.tag == METAMODEL_NAMESPACE+'Label':
                labels.append((child.get('position'), self.DummyLabelAppearance(child[0])))
            else:
                visualObj.AppendChild(self.DummyRelationshipAppearance(child))
        tmp = CConnectionType(a, 'Connection', visualObj,domain=domain)
        for pos, lbl in labels:
            tmp.AddLabel(pos, lbl) 
        return tmp 
    
    def DummyLabelAppearance(self,root):
        '''
        Labels in relationship are a bit autonomous part at the moment, so they are generated separately
        '''
        if root.tag.split("}")[1] not in ALL:
            raise FactoryError("XMLError", root.tag)
        
        cls = ALL[root.tag.split("}")[1]]
        params = {}
        for attr in root.attrib.items():
            params[attr[0]] = BuildParam(attr[1], cls.types.get(attr[0], None))
        obj = cls(**params)
        if hasattr(obj, "LoadXml"):
            obj.LoadXml(root)
        else:
            for child in root:
                obj.AppendChild(self.DummyLabelAppearance(child))
        return obj