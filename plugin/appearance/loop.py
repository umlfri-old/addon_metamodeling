import gtk
import os
from lxml import etree
from simpleContent import SimpleContent
from dragSourceEventBox import DragSourceEventBox
from expand import Expand
import constants
from baseElement import BaseElement

class Loop(BaseElement):
    def __init__(self, name, box, manager, parent):
        BaseElement.__init__(self)
        self.manager = manager
        self.containerName = name
        self.box = box
        self.parentContainer = parent
        self.childObjects = []
        self.expand = None
        if type(self.parentContainer).__name__ == 'Container':
            self.expand = Expand(self)
        self.loopCombo = gtk.combo_box_new_text()
        self.selectedLoop = None

        newVbox = gtk.VBox()
        self.set_border_width(0)
        self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("black"))

        newHbox = gtk.HBox()
        eB = gtk.EventBox()
        eB.set_border_width(2)
        eB.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("lightgray"))

        labelEvent = DragSourceEventBox(self)
        newHbox.connect('button-press-event', self.showProperties)
        labelEvent.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("lightgray"))
        label = gtk.Label('  '+name)
        label.set_alignment(0.0, 0.5)

        if type(self.parentContainer).__name__ == 'Container':
            labelEvent.drag_source_set(gtk.gdk.BUTTON1_MASK,[],0)
            self.drag_dest_set(0,[],0)
            self.connect('drag_motion', self.motion_cb)
            self.connect('drag_drop', self.drop_cb)

        labelEvent.add(label)
        newHbox.pack_start(labelEvent,True,True,2)
        iconEvent = gtk.EventBox()
        iconEvent.set_border_width(2)
        iconEvent.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("lightgray"))
        iconEvent.connect('button-release-event', self.deleteClicked)
        icon = gtk.Image()
        icon.set_from_file(os.path.split(os.path.realpath(__file__))[0]+'/delete.png')
        iconEvent.add(icon)
        newHbox.pack_end(iconEvent,False,True,2)

        newVbox.pack_start(newHbox,False)

        sc = SimpleContent(self,manager)
        self.box.pack_start(sc)
        self.childObjects.append(sc)

        newVbox.pack_start(self.box)
        eB.add(newVbox)
        self.add(eB)

    def deleteClicked(self, widget, w):
        dialog = gtk.MessageDialog(None,0,gtk.MESSAGE_QUESTION,gtk.BUTTONS_YES_NO,'Delete '+self.containerName+' with whole content?')
        response = dialog.run()
        if response == gtk.RESPONSE_YES:
            if self.parentContainer == None:
                self.manager.clearAll()
            else:
                self.parentContainer.deleteChild(self)
                self.manager.clearProperties()
        dialog.destroy()

    def showProperties(self, widget, w):
        if self.manager.lastHighligted:
            self.manager.lastHighligted.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("black"))
        self.manager.lastHighligted = self
        self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("green"))
        box = self.manager.wTree.get_widget('vbox_properties')
        for w in box.children():
            box.remove(w)
        label = gtk.Label('Loop')
        label.set_alignment(0.01, 0.5)
        self.loopCombo = gtk.combo_box_new_text()
        self.loopCombo.connect('changed', self.comboChanged)
        actualLoopLayer = self.getActualLoopLayer()
        if actualLoopLayer:
            self.searchElements(actualLoopLayer)
        if self.selectedLoop == None:
            self.loopCombo.set_active(0)
        i = 0
        for x in self.loopCombo.get_model():
            if x[0] == self.selectedLoop:
                self.loopCombo.set_active(i)
            i += 1
        box.pack_start(label, False)
        box.pack_start(self.loopCombo, False)
        box.pack_start(gtk.Label(' '),False)
        if self.expand:
            box.pack_start(self.expand, False)
            box.pack_start(gtk.Label(' '),False)
        box.show_all()

    def comboChanged(self, widget):
        self.selectedLoop = self.loopCombo.get_active_text()

    def getActualLoopLayer(self):
        widget = self.parent
        elementName = ''
        while widget:
            if type(widget).__name__ == 'Loop':
                if str(widget.selectedLoop).startswith('#self.'):
                    elementName = widget.selectedLoop[6:]
                elif str(widget.selectedLoop).startswith('#'):
                    elementName = widget.selectedLoop[1:]
                for ele in widget.loopCombo.get_model():
                    self.loopCombo.append_text(ele[0])
                return self.findElementByName(self.manager.selected.object, elementName)
            else:
                widget = widget.parent
        return self.manager.selected.object

    def searchElements(self, element):
        for con in element.connections:
            if con.type.name == constants.ASSEMBLE_NAME:
                if con.destination == element and con.source.type.name == constants.ELEMENT_OBJECT_NAME:
                    if con.destination == self.manager.selected.object:
                        self.loopCombo.append_text('#self.'+con.source.name)
                    else:
                        self.loopCombo.append_text('#'+con.source.name)

    def findElementByName(self, root, name):
        self.element = None
        self.getNodes(root, name)
        return self.element

    def getNodes(self, root, name):
        for con in root.connections:
            if con.type.name == constants.ASSEMBLE_NAME:
                if con.destination == root and con.source.type.name == constants.ELEMENT_OBJECT_NAME:
                    if con.source.name == name:
                        self.element = con.source
                    self.getNodes(con.source, name)

    def getApp(self):
        app = etree.Element('Loop')
        collection = self.loopCombo.get_active_text()
        if not collection:
            collection = ''
        app.attrib['collection'] = collection
        if self.childObjects[0].content != None:
            app.append(self.childObjects[0].content.getApp())
        return app

    @staticmethod
    def validate(element, dataElement):
        value = element.get('collection')
        if value == '' or not value.strip():
            return False, 'Missing value in loop.'
        if element.getchildren() == []:
            return False, 'Missing content for loop. Add some or delete loop.'
        return True, None