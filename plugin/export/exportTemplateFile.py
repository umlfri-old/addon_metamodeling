from lxml import etree
import constants
import os.path

class ExportTemplateFile:
    def __init__(self, interface, uri, version, rootDir, rootObject, nodes):
        self.i = interface
        self.metamodelUri = uri
        self.metamodelVersion = version
        self.objectsObjectId = '0'
        self.rootDir = rootDir
        self.rootObject = rootObject
        self.nodes = nodes
            
    def export(self):
        root = etree.Element("umlproject")
        root.attrib['xmlns']='http://umlfri.kst.fri.uniza.sk/xmlschema/umlproject.xsd'
        root.attrib['saveversion']='1.1.0'
        
        metamodel = etree.Element('metamodel')
        uri = etree.Element('uri')
        uri.text = self.metamodelUri
        metamodel.append(uri)
        version = etree.Element('version')
        version.text = self.metamodelVersion
        metamodel.append(version)
        root.append(metamodel)
        
        objects = etree.Element('objects')
        obj = etree.Element('object')
        type = self.rootObject
        print self.rootObject
        if type == 'Package_default':
            type = 'Package_default_empty'
        obj.attrib['type'] = type
        obj.attrib['id'] = self.objectsObjectId
        dic = etree.Element('dict')
        text = etree.Element('text')
        text.attrib['name'] = 'name'
        text.text = 'Project'
        dic.append(text)
        obj.append(dic)
        objects.append(obj)
        root.append(objects)
        
        connections = etree.Element('connections')
        root.append(connections)
        
        diagrams = []
        for element in self.nodes:
            if element.type.domain.name == constants.DIAGRAM_DOMAIN_NAME:
                diagrams.append(element)
        if len(diagrams) == 0:
            return False, 'No diagram found in project. Create at least one diagram before export.'
        else:
            diagramsEle = etree.Element('diagrams')
            diagramId = 1
            projectTreeDiagrams = etree.Element('diagrams')
            for dia in diagrams:
                diagram = etree.Element('diagram')
                diagram.attrib['id'] = str(diagramId)
                diagram.attrib['type'] = dia.name
                dic = etree.Element('dict')
                text = etree.Element('text')
                text.attrib['name'] = 'Name'
                text.text = dia.name
                dic.append(text)
                diagram.append(dic)
                diagramsEle.append(diagram)
                if dia.values['template'] == 'True':
                    projectTreeDiagram = etree.Element('diagram')
                    projectTreeDiagram.attrib['id'] = str(diagramId)
                    projectTreeDiagram.attrib['default'] = 'true'
                    projectTreeDiagrams.append(projectTreeDiagram)
                diagramId+=1
            root.append(diagramsEle)
            
            projectTree = etree.Element('projecttree')
            node = etree.Element('node')
            node.attrib['id'] = '0'
            node.append(projectTreeDiagrams)
            projectTree.append(node)
            root.append(projectTree)
        
        counters = etree.Element('counters')
        root.append(counters)
        
        template = open(os.path.join(self.rootDir,'templates','empty.fritx'), 'w')
        template.write(etree.tostring(root, pretty_print=True, xml_declaration=True, encoding="utf-8"))
        template.close()
        return (True,)
