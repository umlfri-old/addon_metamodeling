import gtk
import os
from lxml import etree
from simpleContent import SimpleContent
from dragSourceEventBox import DragSourceEventBox
from align import Align
from expand import Expand
from baseElement import BaseElement

class Padding(BaseElement):
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
        self.paddingSpin = gtk.SpinButton(gtk.Adjustment(0,-10000,10000,1,10,0),0.0,0)
        self.leftSpin = gtk.SpinButton(gtk.Adjustment(0,-10000,10000,1,10,0),0.0,0)
        self.rightSpin = gtk.SpinButton(gtk.Adjustment(0,-10000,10000,1,10,0),0.0,0)
        self.topSpin = gtk.SpinButton(gtk.Adjustment(0,-10000,10000,1,10,0),0.0,0)
        self.bottomSpin = gtk.SpinButton(gtk.Adjustment(0,-10000,10000,1,10,0),0.0,0)

        self.paddingSpin.connect('value-changed', self.changePadding)
        self.leftSpin.connect('value-changed', self.changePadding)
        self.rightSpin.connect('value-changed', self.changePadding)
        self.topSpin.connect('value-changed', self.changePadding)
        self.bottomSpin.connect('value-changed', self.changePadding)

        self.paddingSpin.set_editable(False)
        self.leftSpin.set_editable(False)
        self.rightSpin.set_editable(False)
        self.topSpin.set_editable(False)
        self.bottomSpin.set_editable(False)

        self.innerEB = gtk.EventBox()

        newVbox = gtk.VBox()
        self.innerEB.set_border_width(0)
        self.innerEB.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("black"))

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
        self.borders = gtk.Alignment()
        self.borders.set(1.0,1.0,1.0,1.0)
        self.innerEB.add(eB)
        self.borders.add(self.innerEB)
        self.add(self.borders)

    def changePadding(self, spin):
        if spin == self.paddingSpin:
            self.leftSpin.set_value(0)
            self.rightSpin.set_value(0)
            self.topSpin.set_value(0)
            self.bottomSpin.set_value(0)
            v = int(spin.get_value())
            if v > -1:
                self.borders.set_padding(v,v,v,v)
        else:
            self.paddingSpin.set_value(0)
            top = int(self.topSpin.get_value())
            bot = int(self.bottomSpin.get_value())
            left = int(self.leftSpin.get_value())
            right = int(self.rightSpin.get_value())
            if top < 0:
                top = 0
            if bot < 0:
                bot = 0
            if left < 0:
                left = 0
            if right < 0:
                right = 0
            self.borders.set_padding(top,bot,left,right)

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
        self.manager.lastHighligted = self.innerEB
        self.innerEB.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("green"))
        box = self.manager.wTree.get_widget('vbox_properties')
        for w in box.children():
            box.remove(w)
        label = gtk.Label('Padding')
        label.set_alignment(0.01, 0.5)
        box.pack_start(label, False)
        box.pack_start(self.paddingSpin, False)
        box.pack_start(gtk.Label(' '),False)
        label = gtk.Label('Left')
        label.set_alignment(0.01, 0.5)
        box.pack_start(label, False)
        box.pack_start(self.leftSpin, False)
        box.pack_start(gtk.Label(' '),False)
        label = gtk.Label('Right')
        label.set_alignment(0.01, 0.5)
        box.pack_start(label, False)
        box.pack_start(self.rightSpin, False)
        box.pack_start(gtk.Label(' '),False)
        label = gtk.Label('Top')
        label.set_alignment(0.01, 0.5)
        box.pack_start(label, False)
        box.pack_start(self.topSpin, False)
        box.pack_start(gtk.Label(' '),False)
        label = gtk.Label('Bottom')
        label.set_alignment(0.01, 0.5)
        box.pack_start(label, False)
        box.pack_start(self.bottomSpin, False)
        box.pack_start(gtk.Label(' '),False)
        if self.expand:
            box.pack_start(self.expand, False)
            box.pack_start(gtk.Label(' '),False)
        box.show_all()

    def getApp(self):
        app = etree.Element('Padding')
        if 0 == self.paddingSpin.get_value() == self.leftSpin.get_value() == self.rightSpin.get_value() == self.topSpin.get_value() == self.bottomSpin.get_value():
            app.attrib['padding'] = '0'
        if self.paddingSpin.get_value() != 0:
            app.attrib['padding'] = str(int(self.paddingSpin.get_value()))
        else:
            if self.leftSpin.get_value() != 0:
                app.attrib['left'] = str(int(self.leftSpin.get_value()))
            if self.rightSpin.get_value() != 0:
                app.attrib['right'] = str(int(self.rightSpin.get_value()))
            if self.topSpin.get_value() != 0:
                app.attrib['top'] = str(int(self.topSpin.get_value()))
            if self.bottomSpin.get_value() != 0:
                app.attrib['bottom'] = str(int(self.bottomSpin.get_value()))
        if self.childObjects[0].content != None:
            app.append(self.childObjects[0].content.getApp())
        return app

    @staticmethod
    def validate(element, dataElement):
        padding = element.get('padding')
        if padding == '0':
            return False, 'Padding values not set. Set some or delete padding.'
        if element.getchildren() == []:
            return False, 'Missing content for padding. Add some or delete padding.'
        return True, None