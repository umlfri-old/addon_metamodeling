import gtk
import os
from lxml import etree
from simpleContent import SimpleContent
from dragSourceEventBox import DragSourceEventBox
from align import Align
from expand import Expand
from baseElement import BaseElement

class Sizer(BaseElement):
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
        self.minWidthSpin = gtk.SpinButton(gtk.Adjustment(0,0,10000,1,10,0),0.0,0)
        self.minHeightSpin = gtk.SpinButton(gtk.Adjustment(0,0,10000,1,10,0),0.0,0)
        self.widthSpin = gtk.SpinButton(gtk.Adjustment(0,0,10000,1,10,0),0.0,0)
        self.heightSpin = gtk.SpinButton(gtk.Adjustment(0,0,10000,1,10,0),0.0,0)
        self.maxWidthSpin = gtk.SpinButton(gtk.Adjustment(0,0,10000,1,10,0),0.0,0)
        self.maxHeightSpin = gtk.SpinButton(gtk.Adjustment(0,0,10000,1,10,0),0.0,0)
        self.minWidthSpin.set_editable(False)
        self.minHeightSpin.set_editable(False)
        self.widthSpin.set_editable(False)
        self.heightSpin.set_editable(False)
        self.maxHeightSpin.set_editable(False)
        self.maxWidthSpin.set_editable(False)
        self.minWidthSpin.connect('value-changed', self.changeValue)
        self.minHeightSpin.connect('value-changed', self.changeValue)
        self.widthSpin.connect('value-changed', self.changeValue)
        self.heightSpin.connect('value-changed', self.changeValue)
        self.maxHeightSpin.connect('value-changed', self.changeValue)
        self.maxWidthSpin.connect('value-changed', self.changeValue)


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

    def changeValue(self, spin):
        if spin == self.minHeightSpin or spin == self.minWidthSpin or spin == self.maxHeightSpin or spin == self.maxWidthSpin:
            self.widthSpin.set_value(0)
            self.heightSpin.set_value(0)
        else:
            self.minWidthSpin.set_value(0)
            self.minHeightSpin.set_value(0)
            self.maxWidthSpin.set_value(0)
            self.maxHeightSpin.set_value(0)

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
        label = gtk.Label('Min width')
        label.set_alignment(0.01, 0.5)
        box.pack_start(label, False)
        box.pack_start(self.minWidthSpin, False)
        box.pack_start(gtk.Label(' '),False)
        label = gtk.Label('Min height')
        label.set_alignment(0.01, 0.5)
        box.pack_start(label, False)
        box.pack_start(self.minHeightSpin, False)
        box.pack_start(gtk.Label(' '),False)
        label = gtk.Label('Width')
        label.set_alignment(0.01, 0.5)
        box.pack_start(label, False)
        box.pack_start(self.widthSpin, False)
        box.pack_start(gtk.Label(' '),False)
        label = gtk.Label('Height')
        label.set_alignment(0.01, 0.5)
        box.pack_start(label, False)
        box.pack_start(self.heightSpin, False)
        box.pack_start(gtk.Label(' '),False)

        label = gtk.Label('Max height')
        label.set_alignment(0.01, 0.5)
        box.pack_start(label, False)
        box.pack_start(self.maxHeightSpin, False)
        box.pack_start(gtk.Label(' '),False)

        label = gtk.Label('Max width')
        label.set_alignment(0.01, 0.5)
        box.pack_start(label, False)
        box.pack_start(self.maxWidthSpin, False)
        box.pack_start(gtk.Label(' '),False)

        if self.expand:
            box.pack_start(self.expand, False)
            box.pack_start(gtk.Label(' '),False)
        box.show_all()

    def getApp(self):
        app = etree.Element('Sizer')
        if self.minWidthSpin.get_value() > 0:
            app.attrib['minwidth'] = str(int(self.minWidthSpin.get_value()))
        if self.minHeightSpin.get_value() > 0:
            app.attrib['minheight'] = str(int(self.minHeightSpin.get_value()))
        if self.widthSpin.get_value() > 0:
            app.attrib['width'] = str(int(self.widthSpin.get_value()))
        if self.heightSpin.get_value() > 0:
            app.attrib['height'] = str(int(self.heightSpin.get_value()))
        if self.maxWidthSpin.get_value() > 0:
            app.attrib['maxwidth'] = str(int(self.maxWidthSpin.get_value()))
        if self.maxHeightSpin.get_value() > 0:
            app.attrib['maxheight'] = str(int(self.maxHeightSpin.get_value()))
        for child in self.childObjects:
            if child.content:
                app.append(child.content.getApp())
        return app

    @staticmethod
    def validate(element, dataElement):
        minwidth = element.get('minwidth')
        minheight = element.get('minheight')
        width = element.get('width')
        height = element.get('height')
        maxwidth = element.get('maxwidth')
        maxheight = element.get('maxheight')
        if minwidth == minheight == width == height == maxwidth == maxheight == None:
            return False, 'Sizer values not set. Set some or delete sizer.'
        if element.getchildren() == []:
            return False, 'Missing content for sizer. Add some or delete sizer.'
        return True, None

    def setValues(self, minwidth, minheight, maxwidth, maxheight, width, height):
        if minwidth:
            self.minWidthSpin.set_value(int(minwidth))
        if minheight:
            self.minHeightSpin.set_value(int(minheight))
        if maxwidth:
            self.maxWidthSpin.set_value(int(maxwidth))
        if maxheight:
            self.maxHeightSpin.set_value(int(maxheight))
        if width:
            self.widthSpin.set_value(int(width))
        if height:
            self.heightSpin.set_value(int(height))