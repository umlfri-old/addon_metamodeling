import gtk
import os
from simpleContent import SimpleContent

class Container(gtk.EventBox):
    def __init__(self, name, box, manager, parent):
        gtk.EventBox.__init__(self)
        self.manager = manager
        self.containerName = name
        self.box = box
        self.parentContainer = parent
        self.childObjects = []

        newVbox = gtk.VBox()
        self.set_border_width(3)
        self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("black"))

        newHbox = gtk.HBox()
        eB = gtk.EventBox()
        eB.set_border_width(2)
        eB.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("lightgray"))

        labelEvent = gtk.EventBox()
        newHbox.connect('button-press-event', self.showProperties)
        labelEvent.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("lightgray"))
        label = gtk.Label(name)
        label.set_alignment(0.02, 0.5)

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
        iconEvent.connect('button-press-event', self.deleteClicked)
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
        self.delete_Container(widget)

    def showProperties(self, widget, w):
        if self.manager.lastHighligted:
            self.manager.lastHighligted.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("black"))
        self.manager.lastHighligted = self
        self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("green"))
        self.manager.wTree.get_widget("label_name").set_text(self.containerName)
        box = self.manager.wTree.get_widget('vbox_properties')
        for w in box.children():
            box.remove(w)
        #button = gtk.Button('Delete')
        #button.connect('clicked', self.delete_Container)
        #box.pack_start(button,False,True,1)
        #if type(self.parentContainer).__name__ == 'Container':
        #    box.pack_start(gtk.Label('Position'),False,True,1)
        #    combo = gtk.combo_box_new_text()
        #    position = 1
        #    current = 0
        #    for c in self.parentContainer.childObjects:
        #        if c.content != None:
        #            combo.append_text(str(position))
        #            if c.content == self:
        #                current = position-1
        #            position += 1
        #    combo.set_active(current)
        #    combo.connect('changed', self.parentContainer.reorder, self)
        #    box.pack_start(combo,False,True,1)
        box.show_all()

    def add_New_Simple_Content(self):
        sc = SimpleContent(self,self.manager)
        self.box.pack_start(sc)
        self.childObjects.append(sc)
        self.show_all()

    def reorder(self, newPosition, child):
        for c in self.childObjects:
            if c.content == child:
                self.childObjects.remove(c)
                self.childObjects.insert(newPosition, c)
        tempList = []
        tempChild = None
        for c in self.box.children():
            if c.content == child:
                tempChild = c
            else:
                tempList.append(c)
            self.box.remove(c)

        for i in range(0,len(tempList)):
            if i == newPosition:
                self.box.pack_start(tempChild)
            self.box.pack_start(tempList[i])

    def delete_Container(self, widget):
        dialog = gtk.MessageDialog(None,0,gtk.MESSAGE_QUESTION,gtk.BUTTONS_YES_NO,'Delete '+self.containerName+' with whole content?')
        dialog.show()
        response = dialog.run()
        if response == gtk.RESPONSE_YES:
            if self.parentContainer == None:
                self.manager.clearAll()
            else:
                for c in self.parentContainer.box.children():
                    if c.content == self:
                        self.parentContainer.box.remove(c)
                        self.parentContainer.childObjects.remove(c)
                self.manager.clearProperties()
        dialog.destroy()

    def motion_cb(self, wid, context, x, y, time):
        context.drag_status(gtk.gdk.ACTION_COPY, time)
        return True

    def drop_cb(self, wid, context, x, y, time):
        tempX = None
        source = context.get_source_widget().get_parent().get_parent().get_parent().get_parent()
        for child in self.parentContainer.childObjects:
            if child.content == source:
                for x in self.parentContainer.childObjects:
                    if x.content == self:
                        tempX = x
        if tempX:
            newPosition = self.parentContainer.childObjects.index(tempX)
            self.parentContainer.reorder(newPosition, source)
        return True

