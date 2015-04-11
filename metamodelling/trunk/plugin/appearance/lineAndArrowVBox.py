import gtk
import os
from simpleContent import SimpleContent
from dragSourceEventBox import DragSourceEventBox
from align import Align
from expand import Expand

class LineAndArrowVBox(gtk.EventBox):
    def __init__(self, box, manager, parent):
        gtk.EventBox.__init__(self)
        self.manager = manager
        self.box = box
        self.parentContainer = parent
        self.childObjects = []

        newVbox = gtk.VBox()
        self.set_border_width(0)
        sc = SimpleContent(self,manager)
        self.box.pack_start(sc)
        self.childObjects.append(sc)

        newVbox.pack_start(self.box)
        self.add(newVbox)

    def deleteChild(self, child):
        for c in self.box.children():
            if c.content == child:
                self.box.remove(c)
                self.childObjects.remove(c)

    def showProperties(self, widget, w):
        if self.manager.lastHighligted:
            self.manager.lastHighligted.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("black"))
        self.manager.lastHighligted = self
        box = self.manager.wTree.get_widget('vbox_properties')
        for w in box.children():
            box.remove(w)
        box.show_all()

    def add_New_Simple_Content(self):
        sc = SimpleContent(self,self.manager)
        self.box.pack_start(sc)
        self.childObjects.append(sc)
        self.show_all()

    def getApp(self):
        for child in self.childObjects:
            if child.content != None:
                yield child.content.getApp()