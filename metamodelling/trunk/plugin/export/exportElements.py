from lxml import etree
import constants
import os.path
import shutil
import collections

class ExportElements:
    def __init__(self, interface, rootDir, nodes):
        self.i = interface
        self.rootDir = rootDir
        self.nodes = nodes
            
    def export(self):
        for node in self.nodes:
            if node.type.name == constants.DIAGRAM_OBJECT_NAME:
                self.createDiagram(node)

    def createElement(self, element, type, name):
        iconPath = os.path.split(os.path.realpath(__file__))[0]
        iconPath = iconPath.replace(os.path.join('plugin','export'), os.path.join('metamodel'))

        root = etree.Element(name)
        root.attrib['id'] = element.name
        root.attrib['xmlns'] = 'http://umlfri.kst.fri.uniza.sk/xmlschema/metamodel.xsd'
        icon = etree.Element('Icon')
        icon.attrib['path'] = 'icons/'+element.values['icon'].split('/')[1]
        root.append(icon)
        src = os.path.join(iconPath,element.values['icon'])
        dst = os.path.join(self.rootDir,'metamodel','icons',element.values['icon'].split('/')[1])
        shutil.copy(src,dst)

        domain = etree.Element('Domain')
        domain.attrib['id'] = element.name + '_domain'
        identify = element.values['identify']
        if identify != '':
            domain.attrib['identity'] = identify
        root.append(domain)
        self.createDomain(element)

        if type == 'elements':
            connectionsElement = etree.Element('Connections')
            for conn in element.connections:
                if conn.type.name == constants.LINK_NAME:
                    item = etree.Element('Item')
                    if conn.source == element:
                        item.attrib['value'] = conn.destination.name
                        connEle = conn.destination
                    else:
                        item.attrib['value'] = conn.source.name
                        connEle = conn.source
                    withElements = self.detectOtherConnections(connEle, element)
                    withString = ''
                    if withElements:
                        withString = ','.join(str(ele.name) for ele in withElements)
                    if conn.values['withMe'] == 'True':
                        if withString == '':
                            withString = element.name
                        else:
                            withString = withString + ',' + element.name
                    if withString != '':
                        item.attrib['with'] = unicode(withString)
                        if conn.values['allowRecursive'] == 'True':
                            item.attrib['allowrecursive'] = '1'
                        else:
                            item.attrib['allowrecursive'] = '0'
                        connectionsElement.append(item)
            root.append(connectionsElement)

        #Appearance
        try:
            app = etree.fromstring(element.values['appearance'],etree.XMLParser(remove_blank_text=True))
            for ele in app.iter('Icon'):
                filename = ele.attrib['filename']
                shutil.copy(filename, os.path.join(self.rootDir,'metamodel','icons'))
                iconName = os.path.split(filename)[-1]
                ele.attrib['filename'] = 'icons/' + iconName
        except Exception:       #in case when rootelement is not connected with diagram, can have empty app
            print 'som ex',element.name
            app = etree.Element('Appearance')
        if len(app) == 0:
            app.append(etree.Element('HBox'))
        root.append(app)

        #Options
        if type == 'elements':
            layer = element.values['layer']
            if layer != 'Middle':
                options = etree.Element('Options')
                layerEle = etree.Element('Layer')
                if layer == 'Bottom':
                    layerEle.text = '-1'
                elif layer == 'Top':
                    layerEle.text = '1'
                options.append(layerEle)
                root.append(options)

        template = open(os.path.join(self.rootDir,'metamodel',type,element.name+'.xml'), 'w')
        template.write(etree.tostring(root, pretty_print=True, xml_declaration=True, encoding="utf-8"))
        template.close()

    def detectOtherConnections(self, connEle, element):
        otherEle = []
        for con in connEle.connections:
            if con.type.name == constants.LINK_NAME:
                if con.source == element or con.destination == element:
                    pass
                else:
                    if con.values['withMe'] == 'True':
                        if con.source == connEle:
                            otherEle.append(con.destination)
                        else:
                            otherEle.append(con.source)
                    else:
                        if con.source == connEle:
                            otherEle.append(con.destination)
                    #else:
                    #    otherEle.append(con.source)
        return otherEle

    def createEnum(self, enum):
        values = eval(enum.values['attributes'])
        attribute = etree.Element('Attribute')
        attribute.attrib['id'] = enum.name.replace(' ','')
        attribute.attrib['name'] = enum.name
        string = etree.Element('Str')
        if enum.values['default'] != '':
            string.attrib['default'] = enum.values['default']
        enumPart = etree.Element('Enum')
        for d in values:
            value = etree.Element('Value')
            value.text = d['value']
            enumPart.append(value)
        string.append(enumPart)
        attribute.append(string)
        return attribute

    def createList(self, element):
        attribute = etree.Element('Attribute')
        attribute.attrib['id'] = element.name
        attribute.attrib['name'] = element.name
        listEle = etree.Element('List')
        #if element.values['separator'] != '':
        #    parse = etree.Element('Parse')
        #    parse.attrib['separator'] = element.values['separator']
        #    listEle.append(parse)
        domainEle = etree.Element('Domain')
        for d in eval(element.values['attributes']):
            domainAttr = etree.Element('Attribute')
            domainAttr.attrib['id'] = d['attName'].replace(' ','')
            domainAttr.attrib['name'] = d['attName']
            if d['visible'] == 'True':
                domainAttr.attrib['hidden'] = d['visible'].lower()
            attType = etree.Element(d['attType'])
            if d['default'] != '':
                attType.attrib['default'] = d['default']
            domainAttr.append(attType)
            domainEle.append(domainAttr)
        if element.values['joiner'] != '':
            joiner = etree.Element('Join')
            joiner.attrib['joiner'] = element.values['joiner']
            domainEle.append(joiner)
        for conn in element.connections:
            if conn.source.type.name == constants.ENUM_OBJECT_NAME:
                domainEle.append(self.createEnum(conn.source))
        for conn in element.connections:
            if conn.source.type.name == constants.ELEMENT_OBJECT_NAME:
                if conn.type.name == constants.ASSEMBLE_NAME:
                    if conn.destination == element:
                        domainEle.append(self.createList(conn.source))
        listEle.append(domainEle)
        attribute.append(listEle)
        return attribute

    def createDomain(self, element):
        root = etree.Element('Domain')
        root.attrib['xmlns'] = 'http://umlfri.kst.fri.uniza.sk/xmlschema/metamodel.xsd'
        root.attrib['id'] = element.name + '_domain'

        if element.type.name == constants.DIAGRAM_OBJECT_NAME:
            attribute = etree.Element('Attribute')
            attribute.attrib['id'] = 'Name'
            attribute.attrib['name'] = 'Name'
            attType = etree.Element('Str')
            attribute.append(attType)
            root.append(attribute)

        for d in eval(element.values['attributes']):
            attribute = etree.Element('Attribute')
            attribute.attrib['id'] = d['attName'].replace(' ','')
            attribute.attrib['name'] = d['attName']
            attType = etree.Element(d['attType'])
            if d['default'] != '':
                attType.attrib['default'] = d['default']
            if d['visible'] == 'True':
                attribute.attrib['hidden'] = d['visible'].lower()
            attribute.append(attType)
            root.append(attribute)

        for conn in element.connections:
            if conn.source.type.name == constants.ENUM_OBJECT_NAME:
                root.append(self.createEnum(conn.source))

        for conn in element.connections:
            if conn.source.type.name == constants.ELEMENT_OBJECT_NAME:
                if conn.type.name == constants.ASSEMBLE_NAME:
                    if conn.source != element:
                        root.append(self.createList(conn.source))

        template = open(os.path.join(self.rootDir,'metamodel','domains',element.name+'_domain.xml'), 'w')
        template.write(etree.tostring(root, pretty_print=True, xml_declaration=True, encoding="utf-8"))
        template.close()

    def createDiagram(self, diagram):
        iconPath = os.path.split(os.path.realpath(__file__))[0]
        iconPath = iconPath.replace(os.path.join('plugin','export'), os.path.join('metamodel'))

        root = etree.Element('DiagramType')
        root.attrib['id'] = diagram.name
        root.attrib['xmlns'] = 'http://umlfri.kst.fri.uniza.sk/xmlschema/metamodel.xsd'
        icon = etree.Element('Icon')
        icon.attrib['path'] = 'icons/'+diagram.values['icon'].split('/')[1]
        root.append(icon)
        src = os.path.join(iconPath,diagram.values['icon'])
        dst = os.path.join(self.rootDir,'metamodel','icons',diagram.values['icon'].split('/')[1])
        shutil.copy(src,dst)

        domain = etree.Element('Domain')
        domain.attrib['id'] = diagram.name + '_domain'
        domain.attrib['identity'] = 'Name'
        root.append(domain)
        self.createDomain(diagram)

        special = etree.Element('Special')
        special.attrib['swimlines'] = '0'
        special.attrib['lifelines'] = '0'
        root.append(special)

        connections = []
        elements = etree.Element('Elements')
        for conn in diagram.connections:
            if conn.source.type.name == constants.ELEMENT_OBJECT_NAME:
                if conn.type.name == constants.SET_NAME:
                    item = etree.Element('Item')
                    item.attrib['value'] = conn.source.name
                    elements.append(item)
                    for c in conn.source.connections:
                        if c.type.name == constants.LINK_NAME:
                            if c.source.name == conn.source.name:
                                if c.destination not in connections:
                                    connections.append(c.destination)
                            else:
                                if c.source not in connections:
                                    connections.append(c.source)
                    self.createElement(conn.source, 'elements', 'ElementType')
        root.append(elements)

        connectionsElement = etree.Element('Connections')
        names = []
        for conn in connections:
            item = etree.Element('Item')
            item.attrib['value'] = conn.name
            if conn.name not in names:
                connectionsElement.append(item)
                self.createElement(conn, 'connections', 'ConnectionType')
                names.append(conn.name)
        root.append(connectionsElement)

        template = open(os.path.join(self.rootDir,'metamodel','diagrams',diagram.name+'.xml'), 'w')
        template.write(etree.tostring(root, pretty_print=True, xml_declaration=True, encoding="utf-8"))
        template.close()
            
