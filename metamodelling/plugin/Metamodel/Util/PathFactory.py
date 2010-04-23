'''
Created on 12.4.2010

@author: Michal Kovacik
'''

from lib.Depend.etree import etree, HAVE_LXML

from lib.Distconfig import SCHEMA_PATH
from lib.Math2D import Path
from lib.consts import METAMODEL_NAMESPACE

import os.path

#if lxml.etree is imported successfully, we use xml validation with xsd schema
if HAVE_LXML:
    xmlschema_doc = etree.parse(os.path.join(SCHEMA_PATH, "metamodel.xsd"))
    xmlschema = etree.XMLSchema(xmlschema_doc)

class PathFactory(object):
    def __init__(self, path):
        #self.storage = storage
        self.paths = {}
        self.content = etree.parse(path)
        
        root = self.content.getroot()

        #xml (version) file is validate with xsd schema (metamodel.xsd)
        if HAVE_LXML:
            if not xmlschema.validate(root):
                raise FactoryError("XMLError", xmlschema.error_log.last_error)
        
        for element in root:
            if element.tag == METAMODEL_NAMESPACE + 'Path':
                self.paths[element.get('id')] = Path(element.get('path'))
    
    #return path by id
    def GetPath(self, id):
        return self.paths[id]
    
    #return path items
    def GetPaths(self):
        return self.paths.items()
    
    def GetContent(self):
        return self.content
    
    
        