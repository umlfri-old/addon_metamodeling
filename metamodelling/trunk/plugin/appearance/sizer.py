import gtk
import os
from simpleContent import SimpleContent
from dragSourceEventBox import DragSourceEventBox
from align import Align
from expand import Expand

class Sizer(gtk.EventBox):
    def __init__(self, name, box, manager, parent):
        gtk.EventBox.__init__(self)
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
        if spin == self.minHeightSpin or spin == self.minWidthSpin:
            self.widthSpin.set_value(0)
            self.heightSpin.set_value(0)
        else:
            self.minWidthSpin.set_value(0)
            self.minHeightSpin.set_value(0)

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

    def deleteChild(self, child):
        for c in self.box.children():
            if c.content == child:
                self.box.remove(c)
                self.childObjects.remove(c)
        self.add_New_Simple_Content()

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

    def add_New_Simple_Content(self):
        if len(self.childObjects) == 0:
            sc = SimpleContent(self,self.manager)
            self.box.pack_start(sc)
            self.childObjects.append(sc)
            self.show_all()

    def motion_cb(self, wid, context, x, y, time):
        context.drag_status(gtk.gdk.ACTION_COPY, time)
        return True

    def drop_cb(self, wid, context, x, y, time):
        tempX = None
        source = context.get_source_widget().getParent()
        for child in self.parentContainer.childObjects:
            if child.content == source:
                for x in self.parentContainer.childObjects:
                    if x.content == self:
                        tempX = x
        if tempX:
            newPosition = self.parentContainer.childObjects.index(tempX)
            self.parentContainer.reorder(newPosition, source)
        return True

    def getApp(self):
        app = '<Sizer '
        if self.minWidthSpin.get_value() > 0:
            app += 'minwidth="' + str(int(self.minWidthSpin.get_value())) + '" '
        if self.minHeightSpin.get_value() > 0:
            app += 'minheight="' + str(int(self.minHeightSpin.get_value())) + '" '
        if self.widthSpin.get_value() > 0:
            app += 'width="' + str(int(self.widthSpin.get_value())) + '" '
        if self.heightSpin.get_value() > 0:
            app += 'height="' + str(int(self.heightSpin.get_value())) + '" '
        if self.maxWidthSpin.get_value() > 0:
            app += 'maxwidth="' + str(int(self.maxWidthSpin.get_value())) + '" '
        if self.maxHeightSpin.get_value() > 0:
            app += 'maxheight="' + str(int(self.maxHeightSpin.get_value())) + '" '
        app += '>'
        for child in self.childObjects:
            if child.content:
                app += child.content.getApp()
        return app+' </Sizer>'