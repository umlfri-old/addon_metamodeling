import gtk
import gtk.glade
from exportAddonFile import ExportAddonFile
from exportTemplateFile import ExportTemplateFile
from exportMetamodelFolder import ExportMetamodelFolder
from exportElements import ExportElements
from appValidator import AppValidator
import os
import constants

class Export:
    def __init__(self, interface):
        self.i = interface
        self.dic = { "on_button_cancel_clicked" : self.close, "on_button_export_clicked" : self.export_metamodel,
                     "on_buttonIconChoose_clicked" : self.chooseIcon, "on_buttonFolderChoose_clicked" : self.chooseFolder }
        self.gladefile = os.path.join(os.path.split(os.path.realpath(__file__))[0],'export_metamodel.glade')
        self.closed = True
        self.wTree = gtk.glade.XML(self.gladefile) 
        self.window = self.wTree.get_widget("MainWindow")
        self.wTree.signal_autoconnect(self.dic)
        self.window.connect("destroy", self.close)
        self.window.connect("delete_event", self.close2)
        self.rootDir = ''
        self.nodes = []
        self.visited = []
        self.saveNodes = []
    
    def setRootDir(self, directory):
        self.rootDir = directory    	    
    
    def close(self, widget):
        self.closed = True
        self.window.hide()
        return gtk.TRUE
        
    def close2(self, widget, widget2):
        self.closed = True
        self.window.hide()
        return gtk.TRUE
        
    def chooseFolder(self, widget):
        chooser = gtk.FileChooserDialog(title='Choose folder for export',action=gtk.FILE_CHOOSER_ACTION_OPEN,buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK))
        chooser.set_action(gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER)
        response = chooser.run()
        if response == gtk.RESPONSE_OK:
            self.wTree.get_widget('entryFolder').set_text(chooser.get_filename())
            self.rootDir = chooser.get_filename()
        elif response == gtk.RESPONSE_CANCEL:
            pass
        chooser.destroy()
    
    def chooseIcon(self, widget):
        chooser = gtk.FileChooserDialog(title='Choose icon',action=gtk.FILE_CHOOSER_ACTION_OPEN,buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK))
        pngFilter = gtk.FileFilter()
        pngFilter.set_name("png files")
        pngFilter.add_pattern("*.png")
        chooser.add_filter(pngFilter)
        response = chooser.run()
        if response == gtk.RESPONSE_OK:
            self.wTree.get_widget('entryIcon').set_text(chooser.get_filename())
        elif response == gtk.RESPONSE_CANCEL:
            pass
        chooser.destroy()
    
    def getAllNodes(self, root):
        for node in root.children:
            if node.type.name != constants.DEFAULT_ROOT_OBJECT_NAME:
                self.nodes.append(node)
            self.getAllNodes(node)

    def show(self):
        if self.i.project:      #show export window only if metamodeling project is opened
            if self.i.project.metamodel.uri == 'urn:umlfri.org:metamodel:metamodeling':
                self.nodes = []
                self.getAllNodes(self.i.project.root)

                if not self.checkModelConstraints():
                    return

                self.loadPackageInfo()

                if self.closed:
                    self.window.show()
                    self.closed = False
                else:
                    self.close(self.window)
                    self.show()
    
    def showError(self, message, title = None):
        md = gtk.MessageDialog(None, gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_ERROR, gtk.BUTTONS_CLOSE, message)
        if title:
            md.set_title(title)
        md.run()
        md.destroy()
    
    def validateForm(self):
        if self.wTree.get_widget('entryName').get_text() == '':
            self.showError('It is good to have a name.')
            return False
        
        tag = self.wTree.get_widget('entryUriTag').get_text()
        tag = tag.replace(' ','')         
        if not tag:
            self.showError('Uri tag is required.')
            return False
        
        root = self.wTree.get_widget('entryRoot').get_text()
        if root != constants.DEFAULT_ROOT_OBJECT_NAME:
            exists = False
            for element in self.nodes:
                if element.name == root:
                    exists = True
            if not exists:
                self.showError('Element with name "'+root+'" not found. Use "'+constants.DEFAULT_ROOT_OBJECT_NAME+'" for default.')
                return False

        icon = self.wTree.get_widget('entryIcon').get_text()
        if not os.path.isfile(icon) or not icon.endswith('.png'):
            self.showError('You have to choose png icon.') 
            return False 
        
        if not os.path.exists(self.rootDir) or not os.listdir(self.rootDir) == []:
            self.showError('Choose empty folder for export.')    
            return False
        return True

    def loadPackageInfo(self):
        self.wTree.get_widget('entryName').set_text(self.i.project.root.values['name'])
        self.wTree.get_widget('entryUriTag').set_text(self.i.project.root.values['uriTag'])
        self.wTree.get_widget('entryVersion').set_text(self.i.project.root.values['version'])
        self.wTree.get_widget('entryAuthor').set_text(self.i.project.root.values['author'])
        self.wTree.get_widget('entryHomepage').set_text(self.i.project.root.values['homepage'])
        self.wTree.get_widget('entryRoot').set_text(self.i.project.root.values['root'])
        self.wTree.get_widget('entryIcon').set_text(self.i.project.root.values['icon'])
        self.wTree.get_widget('entryFolder').set_text(self.i.project.root.values['folder'])
        buffer = gtk.TextBuffer()
        buffer.set_text(self.i.project.root.values['note'])
        self.wTree.get_widget('textviewDescription').set_buffer(buffer)

    def checkModelConstraints(self):
        diagrams = []
        for element in self.nodes:
            if element.type.domain.name == constants.DIAGRAM_DOMAIN_NAME:
                diagrams.append(element)
        if len(diagrams) == 0:
            self.showError('No diagram found in project. Create at least one diagram before export.')
            return False

        for child in self.nodes:
            if child.type.name == constants.DIAGRAM_OBJECT_NAME:
                for conn in child.connections:
                    if conn.destination.type.name != constants.DIAGRAM_OBJECT_NAME:
                        self.showError('Diagram "'+child.name+'" can not be connection source element with "'+conn.destination.name+'".')
                        return False

        for child in self.nodes:
            if child.type.name == constants.ENUM_OBJECT_NAME:
                for conn in child.connections:
                    if conn.destination.type.name == constants.ENUM_OBJECT_NAME:
                        self.showError('Enum "'+child.name+'" can not be connection destination element with '+conn.source.name+'".')
                        return False

        for child in self.nodes:
            if child.type.name == constants.CONNECTION_OBJECT_NAME:
                for conn in child.connections:
                    if conn.type.name == constants.ASSEMBLE_NAME:
                        if conn.source.type.name == constants.CONNECTION_OBJECT_NAME:
                            self.showError('"'+child.name+'" can not be connection source element with "'+conn.destination.name+'".')
                            return False

        #names = []
        #for child in self.nodes:
        #    if child.type.name == constants.ELEMENT_OBJECT_NAME:
        #        names.append(child.name)
        #for child in self.nodes:
        #    if child.type.name == constants.CONNECTION_OBJECT_NAME:
        #        for conn in child.connections:
        #            if conn.type.name == constants.LINK_NAME:
        #                if conn.values['connectWith'] != '':
        #                    connWith = conn.values['connectWith'].split(',')
        #                    for ele in connWith:
        #                        if ele not in names:
        #                            self.showError('Link "'+conn.source.name+'" - "'+conn.destination.name+'" has incorret atribute:'+ele)
        #                            return False

        if not self.checkUniqueNamesOfElements():
            return False

        if not self.checkEmptyEnums():
            return False

        #if not self.checkUniqueNamesOfConnections():
        #    return False

        for child in self.nodes:
            if not self.checkMultipleConnections(child):
                return False

        if not self.checkCycles():
            return False

        #if not self.checkRedundantElements():
        #    return False
        if not self.checkAppearance():
            return False

        return True

    def checkEmptyEnums(self):
        for child in self.nodes:
            if child.type.name == constants.ENUM_OBJECT_NAME:
                if len(eval(child.values['attributes'])) == 0:
                    self.showError('Enum "'+child.name+'" is empty. Add some values.')
                    return False
        return True

    def exploreElement(self, element, allNodes):
        if element in allNodes:
                allNodes.remove(element)
        if len(allNodes) > 0:
            for con in element.connections:
                if con.type.name == constants.ASSEMBLE_NAME:
                    if con.source != element:
                        self.exploreElement(con.source, allNodes)
                if con.type.name == constants.LINK_NAME:
                    if con.source == element:
                        self.exploreElement(con.destination, allNodes)
                    else:
                        self.exploreElement(con.source, allNodes)
        else:
            return

    def checkRedundantElements(self):
        allNodes = []
        for child in self.nodes:
            if child.type.name != constants.DIAGRAM_OBJECT_NAME:
                allNodes.append(child)

        for child in self.nodes:
            if child.type.name == constants.DIAGRAM_OBJECT_NAME:
                for con in child.connections:
                    self.exploreElement(con.source, allNodes)
        if len(allNodes) == 0:
            return True
        else:
            self.showError('Unused elements: '+(','.join(str(x.name) for x in allNodes)))
            return False

    def checkUniqueNamesOfConnections(self):
        for child in self.nodes:
            if child.type.name == constants.DIAGRAM_OBJECT_NAME:
                for con in child.connections:
                    if con.type.name == constants.SET_NAME:
                        uniq = set()
                        for c in con.source.connections:
                            if c.type.name == constants.LINK_NAME:
                                if c.source.type.name == constants.ELEMENT_OBJECT_NAME:
                                    if c.destination.name in uniq:
                                        self.showError('Unique names for connections with one elements are required. Found two same for element "'+c.source.name+'": '+c.destination.name)
                                        return False
                                    else:
                                        uniq.add(c.destination.name)
                                else:
                                    if c.source.name in uniq:
                                        self.showError('Unique names for connections with one elements are required. Found two same for element "'+c.destination.name+'": '+c.source.name)
                                        return False
                                    else:
                                        uniq.add(c.source.name)
        return True

    def checkUniqueNamesOfElements(self):
        uniq = set()
        for child in self.nodes:
            if child.type.name == constants.DIAGRAM_OBJECT_NAME:
                for con in child.connections:
                    if con.type.name == constants.SET_NAME:
                        if con.source.name in uniq:
                            self.showError('Unique names for all elements connected to a diagram are required. Found two same "'+con.source.name+'".')
                            return False
                        else:
                            uniq.add(con.source.name)
        return True

    def checkCycles(self):
        nodes = []
        #L = [] #Empty list that will contain the sorted elements
        starters = [] #Set of all nodes with no incoming edges
        for node in self.nodes:
            if node.type.name == constants.ELEMENT_OBJECT_NAME:
                nodes.append(node)
                hasIncoming = False
                for conn in node.connections:
                    if conn.type.name == constants.ASSEMBLE_NAME:
                        if conn.destination == node:
                            if conn.source.type.name == constants.ELEMENT_OBJECT_NAME:
                                hasIncoming = True
                if not hasIncoming:
                    starters.append(node)
        #print 'starters:', ','.join(str(x.name) for x in starters)


        while starters:
            upLayer = []
            upLayer.append(starters.pop())
            nodes.remove(upLayer[0])
            while True:
                currentLevel = []
                downLayer = []
                for node in upLayer:
                    for conn in node.connections:
                        if conn.type.name == constants.ASSEMBLE_NAME:
                            if conn.destination != node:
                                if conn.destination in nodes:
                                    if conn.destination not in downLayer:
                                        currentLevel.append(conn.destination)
                #print 'curr:',",".join(str(x.name) for x in currentLevel)
                #print 'up:',",".join(str(x.name) for x in upLayer)
                #print 'down:', ",".join(str(x.name) for x in downLayer)
                for node in currentLevel:
                    for conn in node.connections:
                        if conn.type.name == constants.ASSEMBLE_NAME:
                            if conn.destination in upLayer:
                                self.showError('Cycle found between elements: "'+conn.destination.name+'" and "'+node.name+'".')
                                return False
                            else:
                                downLayer.append(conn.destination)
                                #print 'nodes:', ",".join(str(x.name) for x in nodes)
                                #print 'idem mazat:', node.name
                                if node in nodes:
                                    nodes.remove(node)
                for node in currentLevel:
                    upLayer.append(node)
                if not downLayer:
                    break
        #print 'pocet:', 'down:', ",".join(str(x.name) for x in nodes)
        if nodes:
            self.showError('Cycle found:' + ",".join(str(x.name) for x in nodes))
            return False
        return True



        '''KAHN
        count = 0
        L = [] #Empty list that will contain the sorted elements
        starters = [] #Set of all nodes with no incoming edges
        edges = []
        for node in self.i.project.root.children:
            if node.type.name == constants.ELEMENT_OBJECT_NAME:
                count += 1
                hasIncoming = False
                for conn in node.connections:
                    if conn.type.name == constants.ASSEMBLE_NAME:
                        if conn.destination == node:
                            hasIncoming = True
                        if conn not in edges:
                            edges.append(conn)
                if not hasIncoming:
                    starters.append(node)
        print 'edges:', ",".join(str(x.source.name+'-'+x.destination.name) for x in edges)
        print 'starters:', ','.join(str(x.name) for x in starters)
        while starters:
            node = starters.pop()
            print 'pop:', node.name
            L.append(node)
            for conn in node.connections:
                if conn.type.name == constants.ASSEMBLE_NAME:
                    if conn.destination != node:
                        edges.remove(conn)
                        hasIncoming = False
                        for c in conn.destination.connections:
                            if c.type.name == constants.ASSEMBLE_NAME:
                                if c != conn:
                                    if c.destination == conn.destination:
                                        hasIncoming = True
                        if not hasIncoming:
                            starters.append(conn.destination)

        print ",".join(str(x.source.name+'-'+x.destination.name) for x in edges)
        print ",".join(str(x.name) for x in L)
        if edges:
            self.showError('cyklus')
            return False
        else:
            return True
        '''

        '''nodes = []
        for child in self.i.project.root.children:
            if child.type.name == constants.ELEMENT_OBJECT_NAME:
                nodes.append(child)
        upLayer = []
        downLayer = []

        while nodes:
            downLayer.append(nodes[0])
            while downLayer:
                for node in upLayer:
                    for conn in node.connections:
                        if conn.type.name == constants.ASSEMBLE_NAME:
                            if conn.destination != node:
                                if conn.destination in nodes:
                                    if conn.destination not in downLayer:
                                        downLayer.append(conn.destination)
                print 'up:',",".join(str(x.name) for x in upLayer)
                print 'down:', ",".join(str(x.name) for x in downLayer)
                for node in downLayer:
                    for conn in node.connections:
                        if conn.type.name == constants.ASSEMBLE_NAME:
                            if conn.destination in upLayer:
                                self.showError('cyklus')
                                return False
                    else:
                        nodes.remove(node)
                for node in downLayer:
                    upLayer.append(node)
                downLayer = []
        return True'''

        '''self.nodes = []

        for child in self.i.project.root.children:
            if child.type.name == constants.ELEMENT_OBJECT_NAME:
                self.nodes.append(child)
        discovered = []
        closed = []
        while self.nodes:
            S= [] #stack
            S.append(self.nodes[0])
            path = []
            print '-----'
            while S:
                node = S.pop()
                print node.name
                print 'disc:', (",".join(str(x.name) for x in discovered))
                if node in path:
                    if node not in closed:
                        self.showError('Cyclus found: '+",".join(str(x.name) for x in path)+','+node.name)
                        return False
                else:
                    path.append(node)
                if node not in discovered:
                    discovered.append(node)
                    self.nodes.remove(node)
                    count = 0
                    for conn in node.connections:
                        if conn.destination != node:
                            if conn.destination.type.name == constants.ELEMENT_OBJECT_NAME:
                                S.append(conn.destination)
                                count = 1
                    if count == 0:
                        print 'closed adde:',node.name
                        closed.append(node)
                #else:
                #    print 'closed adde:',node.name
                #    closed.append(node)


        return True'''

    def checkMultipleConnections(self, element):
        seen = set()
        for conn in element.connections:
            edge1 = (conn.source,conn.destination,conn.type.name)
            edge2 = (conn.destination,conn.source,conn.type.name)
            if edge1 in seen or edge2 in seen:
                self.showError('Only one '+conn.type.name+' connection is allowed between "'+conn.source.name+'" and "'+conn.destination.name+'".')
                return False
            else:
                seen.add(edge1)
                seen.add(edge2)
        return True

    def export_metamodel(self, widget):
        if not self.validateForm():
            return              
        
        self.createFolders()
        
        addonExport = ExportAddonFile(self.i, self.wTree, self.rootDir)
        result = addonExport.export()
        if not result[0]:
            self.showError(result[1])
            return  
        uri, version = result[2], result[3]     
        
        templateExport = ExportTemplateFile(self.i, uri, version, self.rootDir, self.wTree.get_widget('entryRoot').get_text(), self.nodes)
        result = templateExport.export()
        if not result[0]:
            self.close(widget)
            self.showError(result[1])            
            return
        
        metamodelFolder = ExportMetamodelFolder(self.i, self.rootDir, self.wTree.get_widget('entryRoot').get_text(), self.nodes)
        result = metamodelFolder.export()

        elements = ExportElements(self.i, self.rootDir, self.nodes)
        elements.export()

        self.close(widget)
        md = gtk.MessageDialog(None, gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO, gtk.BUTTONS_OK, 'Export done!')
        md.run()
        md.destroy()

        #self.i.project.root.values['name'] = self.wTree.get_widget('entryName').get_text()
        #self.i.project.root.values['uriTag'] = self.wTree.get_widget('entryUriTag').get_text()
        #self.i.project.root.values['version'] = self.wTree.get_widget('entryVersion').get_text()
        #self.i.project.root.values['author'] = self.wTree.get_widget('entryAuthor').get_text()
        #self.i.project.root.values['homepage'] = self.wTree.get_widget('entryHomepage').get_text()
        #self.i.project.root.values['root'] = self.wTree.get_widget('entryRoot').get_text()
        #self.i.project.root.values['icon'] = self.wTree.get_widget('entryIcon').get_text()
        #self.i.project.root.values['folder'] = self.wTree.get_widget('entryFolder').get_text()
        #startIter = self.wTree.get_widget('textviewDescription').get_buffer().get_start_iter()
        #endIter = self.wTree.get_widget('textviewDescription').get_buffer().get_end_iter()
        #self.i.project.root.values['note'] = self.wTree.get_widget('textviewDescription').get_buffer().get_text(startIter,endIter)


    def createFolders(self):
        self.createFolder('icons')
        self.createFolder('templates')
        self.createFolder('metamodel')
        self.createFolder(os.path.join('metamodel','connections'))
        self.createFolder(os.path.join('metamodel','diagrams'))
        self.createFolder(os.path.join('metamodel','domains'))
        self.createFolder(os.path.join('metamodel','elements'))
        self.createFolder(os.path.join('metamodel','icons'))
    
    def createFolder(self, folder):
        if not os.path.exists(os.path.join(self.rootDir,folder)):
                os.makedirs(os.path.join(self.rootDir,folder))

    def checkAppearance(self):
        checkedConnections = []
        for child in self.nodes:
            if child.type.name == constants.DIAGRAM_OBJECT_NAME:
                for con in child.connections:
                    if con.type.name == constants.SET_NAME:
                        result, msg = self.checkIdentifyAttribute(con.source)
                        if not result:
                            self.showError(msg, 'Attribute error')
                            return False
                        result, msg = AppValidator.validate(con.source)
                        if not result:
                            self.showError(msg, 'Appearance error')
                            return False
                        for con2 in con.source.connections:
                            if con2.type.name == constants.LINK_NAME:
                                if con2.source.type.name == constants.CONNECTION_OBJECT_NAME:
                                    if not con2.source in checkedConnections:
                                        result, msg = AppValidator.validate(con2.source)
                                        if not result:
                                            self.showError(msg, 'Appearance error')
                                            return False
                                        checkedConnections.append(con2.source)
                                else:
                                    if not con2.destination in checkedConnections:
                                        result, msg = AppValidator.validate(con2.destination)
                                        if not result:
                                            self.showError(msg, 'Appearance error')
                                            return False
        return True

    def checkIdentifyAttribute(self, element):
        identify = element.values['identify']
        if identify != '':
            for attrib in eval(element.values['attributes']):
                if attrib['attName'] == identify:
                    if attrib['attType'] == 'Str' or attrib['attType'] == 'Text':
                        return True, None
                    else:
                        return False, element.name + ': Identify attribute "' + identify + '" has to be Str or Text.'
            return False, element.name + ': Identify attribute "' + identify + '" does not exist.'
        return True, None