from lxml import etree
import constants
import os.path
import shutil
from exportElements import ExportElements

class ExportMetamodelFolder:
    def __init__(self, interface, rootDir, rootObject, nodes):
        self.i = interface
        self.rootDir = rootDir
        self.rootObject = rootObject
        self.nodes = nodes
            
    def export(self):    
        #create metamodel.xml
        root = etree.Element("Metamodel")
        root.attrib['xmlns'] = 'http://umlfri.kst.fri.uniza.sk/xmlschema/metamodel.xsd'
        
        diagrams = etree.Element('Diagrams')
        for element in self.nodes:
            if element.type.domain.name == constants.DIAGRAM_DOMAIN_NAME:
                item = etree.Element('Item')
                item.attrib['value'] = element.name
                diagrams.append(item)
        root.append(diagrams)        
                
        template = open(os.path.join(self.rootDir,'metamodel','metamodel.xml'), 'w')
        template.write(etree.tostring(root, pretty_print=True, xml_declaration=True, encoding="utf-8"))
        template.close()

        #create paths.xml
        root = etree.Element('Paths')
        root.attrib['xmlns'] = 'http://umlfri.kst.fri.uniza.sk/xmlschema/metamodel.xsd'
        path = etree.Element('Path')
        path.attrib['id'] = 'diamond_arrow'
        path.attrib['path'] = "M -0.5,-1 L 0,0 L 0.5,-1 L 0,-2 z"
        root.append(path)
        path = etree.Element('Path')
        path.attrib['id'] = 'simple_arrow'
        path.attrib['path'] = "M -0.5,-1 L 0,0 L 0.5,-1"
        root.append(path)
        path = etree.Element('Path')
        path.attrib['id'] = 'connect_arrow'
        path.attrib['path'] = "M -0.5,-1 L 0,0 L 0.5,-1"
        root.append(path)
        path = etree.Element('Path')
        path.attrib['id'] = 'rounded_corner'
        path.attrib['path'] = "M 0,1 C 0,0.446 0.446,0 1,0"
        root.append(path)
        path = etree.Element('Path')
        path.attrib['id'] = 'note_corner'
        path.attrib['path'] = "M 0,1 L 1,1 L 1,0 L 0,1 z M 0,1 L 1,0"
        root.append(path)
        path = etree.Element('Path')
        path.attrib['id'] = 'rounded_side'
        path.attrib['path'] = "M 0,0 C -0.554,0 -1,-0.223 -1,-0.5 C -1,-0.777 -0.554,-1 0,-1"
        root.append(path)
        path = etree.Element('Path')
        path.attrib['id'] = 'crosscircle_arrow'
        path.attrib['path'] = "M -0.5,0 L 0.5,0 M 0,0.5 L 0,-0.5 M 1,0.5 C 1,0.776 0.776,1 0.5,1 C 0.224,1 0,0.776 0,0.5 C 0,0.224 0.224,0 0.5,0 C 0.776,0 1,0.224 1,0.5 z"
        root.append(path)
        path = etree.Element('Path')
        path.attrib['id'] = 'triangle_arrow'
        path.attrib['path'] = "M -0.5,-1 L 0,0 L 0.5,-1 z"
        root.append(path)
        path = etree.Element('Path')
        path.attrib['id'] = 'square_arrow'
        path.attrib['path'] = "M -0.5,-0.5 L 0,0 L 0.5,-0.5 L 0,-1 z"
        root.append(path)
        path = etree.Element('Path')
        path.attrib['id'] = 'sidelong_side'
        path.attrib['path'] = "M -1,0 L 0,-1"
        root.append(path)
        path = etree.Element('Path')
        path.attrib['id'] = 'beak_side'
        path.attrib['path'] = "M 0,-1 L -1,-0.5 L 0,0"
        root.append(path)
        
        template = open(os.path.join(self.rootDir,'metamodel','paths.xml'), 'w')
        template.write(etree.tostring(root, pretty_print=True, xml_declaration=True, encoding="utf-8"))
        template.close()        
        
        #copy package: element, domain, icon        
        exists = False
        for element in self.nodes:
            if self.rootObject == element.name:
                exists = True
                isConnectedWithDiagram = False
                for conn in element.connections:
                    if conn.type.name == constants.SET_NAME:
                        isConnectedWithDiagram = True
                if not isConnectedWithDiagram:
                    self.createRootElement(element)
        if not exists:
            path = os.path.split(os.path.realpath(__file__))[0]
            elementPath = path.replace(os.path.join('plugin','export'), os.path.join('metamodel','elements','package_default_empty.xml'))
            shutil.copy(elementPath, os.path.join(self.rootDir,'metamodel','elements'))
            domainPath = path.replace(os.path.join('plugin','export'), os.path.join('metamodel','domains','package_default_empty.xml'))
            shutil.copy(domainPath, os.path.join(self.rootDir,'metamodel','domains'))
            iconPath = path.replace(os.path.join('plugin','export'), os.path.join('metamodel','icons','package_default.png'))
            shutil.copy(iconPath, os.path.join(self.rootDir,'metamodel','icons'))

        return (True,)

    def createRootElement(self, element):
        exportEle = ExportElements(self.i, self.rootDir, self.nodes)
        exportEle.createElement(element, 'elements', 'ElementType')