import gtk
import os
from dragSourceEventBox import DragSourceEventBox
from align import Align
from shadow import Shadow
from expand import Expand

class Icon(DragSourceEventBox):
    def __init__(self, manager, parent):
        DragSourceEventBox.__init__(self, self)
        self.manager = manager
        self.parentContainer = parent
        self.box = gtk.HBox()
        self.path = None
        self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("black"))
        self.shadow = Shadow(self)
        self.expand = None
        if type(self.parentContainer).__name__ == 'Container':
            self.expand = Expand(self)
        self.align = Align(self)

        self.eB = gtk.EventBox()
        self.eB.set_border_width(2)
        self.connect('button-press-event', self.showProperties)
        labelIcon = gtk.Label('  Icon  ')

        self.icon = gtk.Image()
        self.icon.set_alignment(0.0,0.5)
        self.icon.set_padding(3,3)
        self.icon.set_from_file(os.path.split(os.path.realpath(__file__))[0]+'/question.png')

        iconEvent = gtk.EventBox()
        iconEvent.set_border_width(2)
        iconEvent.connect('button-release-event', self.deleteClicked)
        iconDel = gtk.Image()
        iconDel.set_from_file(os.path.split(os.path.realpath(__file__))[0]+'/delete.png')
        iconEvent.add(iconDel)

        self.box.pack_start(labelIcon, False)
        self.box.pack_start(self.icon)
        self.box.pack_end(iconEvent, False)

        self.eB.add(self.box)
        self.add(self.eB)

        if type(self.parentContainer).__name__ == 'Container':
            self.drag_source_set(gtk.gdk.BUTTON1_MASK,[],0)
            self.drag_dest_set(0,[],0)
            self.connect('drag_motion', self.motion_cb)
            self.connect('drag_drop', self.drop_cb)

    def showProperties(self, widget, w):
        if self.manager.lastHighligted:
            self.manager.lastHighligted.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("black"))
        self.manager.lastHighligted = self
        self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("green"))
        box = self.manager.wTree.get_widget('vbox_properties')
        for w in box.children():
            box.remove(w)
        buttonChoose = gtk.Button('Choose icon')
        buttonChoose.connect('clicked', self.chooseIcon)
        box.pack_start(buttonChoose, False)
        box.pack_start(gtk.Label(' '), False)
        box.pack_start(self.align, False)
        box.pack_start(gtk.Label(' '), False)
        box.pack_start(self.shadow, False)
        if self.expand:
            box.pack_start(gtk.Label(' '),False)
            box.pack_start(self.expand, False)
        box.show_all()

    def chooseIcon(self, widget):
        chooser = gtk.FileChooserDialog(title='Choose icon',action=gtk.FILE_CHOOSER_ACTION_OPEN,buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK))
        pngFilter = gtk.FileFilter()
        pngFilter.set_name("png files")
        pngFilter.add_pattern("*.png")
        chooser.add_filter(pngFilter)
        response = chooser.run()
        if response == gtk.RESPONSE_OK:
            self.icon.set_from_file(chooser.get_filename())
            self.path = chooser.get_filename()
        elif response == gtk.RESPONSE_CANCEL:
            pass
        chooser.destroy()

    def deleteClicked(self, widget, w):
        dialog = gtk.MessageDialog(None,0,gtk.MESSAGE_QUESTION,gtk.BUTTONS_YES_NO,'Delete icon?')
        response = dialog.run()
        if response == gtk.RESPONSE_YES:
            if self.parentContainer == None:
                self.manager.clearAll()
            else:
                self.parentContainer.deleteChild(self)
                #for c in self.parentContainer.box.children():
                #    if c.content == self:
                #        self.parentContainer.box.remove(c)
                #        self.parentContainer.childObjects.remove(c)
                self.manager.clearProperties()
        dialog.destroy()

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

    def xChanged(self, combo):
        self.align.xAlign = combo.get_active()
        if combo.get_active() == 0:
            self.icon.set_alignment(0.0, self.align.yValue)
            self.align.xValue = 0.0
        elif combo.get_active() == 1:
            self.icon.set_alignment(0.5, self.align.yValue)
            self.align.xValue = 0.5
        elif combo.get_active() == 2:
            self.icon.set_alignment(1.0, self.align.yValue)
            self.align.xValue = 1.0
        elif combo.get_active() ==3:
            self.icon.set_alignment(0.0, self.align.yValue)
            self.align.xValue = 0.0

    def yChanged(self, combo):
        self.align.yAlign = combo.get_active()
        if combo.get_active() == 0:
            self.icon.set_alignment(self.align.xValue, 0.0)
            self.align.yValue = 0.0
        elif combo.get_active() == 1:
            self.icon.set_alignment(self.align.xValue, 0.5)
            self.align.yValue = 0.5
        elif combo.get_active() == 2:
            self.icon.set_alignment(self.align.xValue, 1.0)
            self.align.yValue = 1.0
        elif combo.get_active() == 3:
            self.icon.set_alignment(self.align.xValue, 0.5)
            self.align.yValue = 0.5

    def getApp(self):
        app = '<Icon filename="'+self.path+'" />'
        if self.shadow.padding > 0 and self.shadow.buttonColor.color:
            app = '<Shadow ' + self.shadow.getXMLFormat() + '>' + app + '</Shadow>'
        if self.align.isAlignSet():
            app = '<Align ' + self.align.getXMLFormat() + '>' + app + '</Align>'
        return app