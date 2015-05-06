import gtk
import os
from lxml import etree
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
                self.manager.clearProperties()
        dialog.destroy()

    def xChanged(self):
        self.icon.set_alignment(self.align.xValue, self.align.yValue)

    def yChanged(self):
        self.icon.set_alignment(self.align.xValue, self.align.yValue)

    def getApp(self):
        filename = self.path
        if filename == None:
            filename = ''
        app = etree.Element('Icon')
        app.attrib['filename'] = filename
        if self.shadow.padding > 0 or self.shadow.buttonColor.color:
            shadow = self.shadow.getXMLFormat()
            shadow.append(app)
            app = shadow
        if self.align.isAlignSet():
            align = self.align.getXMLFormat()
            align.append(app)
            app = align
        return app

    @staticmethod
    def validate(element, dataElement):
        if element.get('filename') == '':
            return False, 'Missing filename for icon. Choose some or delete icon.'
        return True, None