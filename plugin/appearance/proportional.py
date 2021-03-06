import gtk
import os
from lxml import etree
from simpleContent import SimpleContent
from dragSourceEventBox import DragSourceEventBox
from align import Align
from expand import Expand
from baseElement import BaseElement

class Proportional(BaseElement):
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
        self.align = Align(self)
        self.ratio = gtk.Entry()
        self.ratio.set_text('1:1')
        self.size = gtk.combo_box_entry_new_text()
        self.size.append_text('minimal')
        self.size.append_text('maximal')
        self.size.set_active(1)

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
        label = gtk.Label('Ratio')
        label.set_alignment(0.01, 0.5)
        box.pack_start(label, False)
        box.pack_start(self.ratio, False)
        box.pack_start(gtk.Label(' '),False)
        box.pack_start(self.align, False)
        box.pack_start(gtk.Label(' '),False)
        label = gtk.Label('Width')
        label.set_alignment(0.01, 0.5)
        box.pack_start(label, False)
        box.pack_start(self.size, False)
        box.pack_start(gtk.Label(' '),False)
        if self.expand:
            box.pack_start(self.expand, False)
            box.pack_start(gtk.Label(' '),False)
        box.show_all()

    def xChanged(self):
        pass

    def yChanged(self):
        pass

    def getApp(self):
        app = etree.Element('Proportional')
        app.attrib['ratio'] = self.ratio.get_text()
        if self.align.isAlignSet():
            align = self.align.getXMLFormat()
            app.attrib['align'] = align.get('align')
        app.attrib['size'] = self.size.get_active_text()
        if self.childObjects[0].content != None:
            app.append(self.childObjects[0].content.getApp())
        return app

    @staticmethod
    def validate(element, dataElement):
        ratio = element.get('ratio').split(':')
        if len(ratio) != 2:
            return False, 'Invalid ratio format. Example of correct ratio is: 1:2.'
        if not ratio[0].isdigit() or not ratio[1].isdigit():
            return False, 'Invalid ratio format. Example of correct ratio is: 1:2.'
        if element.getchildren() == []:
            return False, 'Missing content for proportional. Add some or delete proportional.'
        return True, None