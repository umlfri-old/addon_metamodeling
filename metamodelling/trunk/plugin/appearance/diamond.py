import gtk
import os
from lxml import etree
from simpleContent import SimpleContent
from dragSourceEventBox import DragSourceEventBox
from expand import Expand
from colorChooserButton import ColorChooserButton
from pythonValue import PythonValue
from elementValue import ElementValue
from shadow import Shadow
from align import Align
from valueValidator import ValueValidator
import constants
from baseElement import BaseElement

class Diamond(BaseElement):
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
        self.fillColorButton = ColorChooserButton(self, 'Select fill color')
        self.borderColorButton = ColorChooserButton(self, 'Select border color')
        self.shadow = Shadow(self)

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

        hbox = gtk.HBox()
        label = gtk.Label('Fill color')
        label.set_alignment(0.01, 0.5)
        hbox.pack_start(label,False)
        hbox.pack_end(PythonValue(self,'Fill color'),False)
        hbox.pack_end(ElementValue(self,'Fill color'),False)
        box.pack_start(hbox,False)
        box.pack_start(self.fillColorButton, False)

        box.pack_start(gtk.Label(' '),False)

        hbox = gtk.HBox()
        label = gtk.Label('Border color')
        label.set_alignment(0.01, 0.5)
        hbox.pack_start(label,False)
        hbox.pack_end(PythonValue(self,'Border color'),False)
        hbox.pack_end(ElementValue(self,'Border color'),False)
        box.pack_start(hbox,False)
        box.pack_start(self.borderColorButton, False)

        box.pack_start(gtk.Label(' '),False)
        box.pack_start(self.shadow, False)
        box.pack_start(gtk.Label(' '),False)
        if self.expand:
            box.pack_start(self.expand, False)
            box.pack_start(gtk.Label(' '),False)
        box.show_all()

    def setElementValue(self, attrib, value):
        if attrib == 'Fill color':
            self.fillColorButton.color = value
            if value:
                self.fillColorButton.set_label(self.fillColorButton.color)
            else: self.fillColorButton.set_label('')
        elif attrib == 'Border color':
            self.borderColorButton.color = value
            if value:
                self.borderColorButton.set_label(self.borderColorButton.color)
            else:
                self.borderColorButton.set_label('')

    def colorChanged(self, newColor, attrib):
        pass

    def getApp(self):
        if self.containerName == 'Diamond':
            app = etree.Element('Diamond')
        else:
            app = etree.Element('Ellipse')
        if self.fillColorButton.color:
            app.attrib['fill'] = self.fillColorButton.getColor()
        if self.borderColorButton.color:
            app.attrib['border'] = self.borderColorButton.getColor()
        if self.childObjects[0].content != None:
            app.append(self.childObjects[0].content.getApp())
        if self.shadow.padding > 0 or self.shadow.buttonColor.color:
            shadow = self.shadow.getXMLFormat()
            shadow.append(app)
            return shadow
        return app

    @staticmethod
    def validate(element, dataElement):
        fill = element.get('fill')
        if fill:
            if not ValueValidator.validate(fill, dataElement):
                return False, 'Unknown element attribute for fill color: ' + fill
        border = element.get('border')
        if border:
            if not ValueValidator.validate(border, dataElement):
                return False, 'Unknown element attribute for border color: ' + border
        return True, None