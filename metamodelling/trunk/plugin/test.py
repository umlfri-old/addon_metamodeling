import gtk
import gtk.glade
from lxml import etree
import os
import constants
from appearance.simpleContent import SimpleContent
from appearance.container import Container
import constants

class Test:
    def __init__(self, interface):
        self.i = interface
        self.dic = { "on_button_horizontal_box_clicked" : self.widgetClicked,
                     "on_button_vertical_box_clicked" : self.widgetClicked,
                     "on_appearanceWindow_key_release_event" : self.keyPressed,
                     "on_button1_clicked" : self.prehliadka }
        self.closed = True
        self.widgetSelected = False
        self.selectedButton = None
        self.default_color = None
        self.rootObject = None
        self.selected = None #selected element or connection in meta editor
        self.lastHighligted = None

    def close(self, widget):
        self.closed = True
        self.window.hide()
        return gtk.TRUE

    def close2(self, widget, widget2):
        self.closed = True
        self.window.hide()
        return gtk.TRUE

    def show(self):
        selected = []
        for item in self.i.current_diagram.selected:
            selected.append(item)
        if len(selected) != 1:
            md = gtk.MessageDialog(None, gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_ERROR, gtk.BUTTONS_CLOSE, 'Select only one Element or Connection.')
            md.run()
            md.destroy()
            return
        self.selected = selected[0]
        if self.selected.object.type.name != constants.ELEMENT_OBJECT_NAME:
            if self.selected.object.type.name != constants.CONNECTION_OBJECT_NAME:
                md = gtk.MessageDialog(None, gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_ERROR, gtk.BUTTONS_CLOSE, 'Appearance can be specified only for Elements and Connections.')
                md.run()
                md.destroy()
            return
        if self.closed:
            self.init_Window()
            self.window.show()
            self.closed = False
        else:
            self.close(self.window)
            self.init_Window()
            self.show()

    def init_Window(self):
        self.gladefile = os.path.split(os.path.realpath(__file__))[0] + "/test.glade"
        self.wTree = gtk.glade.XML(self.gladefile)
        self.wTree.signal_autoconnect(self.dic)
        self.window = self.wTree.get_widget("appearanceWindow")
        self.window.connect("destroy", self.close)
        self.window.connect("delete_event", self.close2)
        self.window.set_position(gtk.WIN_POS_CENTER)
        self.window.set_keep_above(True)
        self.window.set_title('Appearance '+self.selected.object.name)
        self.widgetSelected = False
        self.selectedButton = None
        self.default_color = None
        self.lastHighligted = None
        vbox = self.wTree.get_widget('vboxContent')
        vbox.pack_start(SimpleContent(None,self))
        vbox.show_all()
        self.rootObject = None
        buton = self.wTree.get_widget('button_horizontal_box')
        buton.drag_source_set(gtk.gdk.BUTTON1_MASK,[],0)
        buton.drag_dest_set(0,[],0)
        buton.connect('drag_end', self.dragend)

        buton2 = self.wTree.get_widget('button_vertical_box')
        buton2.drag_dest_set(0,[],0)
        buton2.connect('drag_motion', self.motion_cb)
        buton2.connect('drag_drop', self.drop_cb)
        buton2.connect('drag_data_received', self.got_data_cb)

    def got_data_cb(wid, context, x, y, data, info, time):
        # Got data.
        print 'lol'#l.set_text(data.get_text())
        context.finish(True, False, time)

    def drop_cb(self, wid, context, x, y, time):
        # Some data was dropped, get the data
        #wid.drag_get_data(context, time)
        print wid.name
        print context.get_source_widget().name
        return True

    def motion_cb(self, wid, context, x, y, time):
        #l.set_text('\n'.join([str(t) for t in context.targets]))
        print 'wid:', wid.name
        context.drag_status(gtk.gdk.ACTION_MOVE, time)
        # Returning True which means "I accept this data".
        return True

    def pokus(self):
        print 'som'
        return True

    def dragend(self, drag_context, dat):
        print drag_context.name

    def widgetClicked(self, widget):
        self.widgetSelected = True
        self.selectedButton = widget
        self.clearProperties()

    def keyPressed(self, widget, key):
        if key.keyval == 65307:
            self.widgetSelected = False
            widget.window.set_cursor(None)

    def buttonAddEnter(self, widget, w):
        if self.widgetSelected == False:
            widget.window.set_cursor(None)
        if self.widgetSelected == True:
            widget.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.PLUS))

    def addContent(self, widget, w):
        if self.widgetSelected:
            self.widgetSelected = False
            widget.window.set_cursor(None)

            widget.remove(widget.get_Label())
            widget.disconnect(widget.enterNotifyHandler)
            widget.disconnect(widget.buttonReleaseHandler)

            content = None
            if self.selectedButton.name == 'button_horizontal_box':
                name = 'Horizontal box'
                content = Container(name, gtk.VBox(), self, widget.parentContainer)
                widget.add_Content(content)
            elif self.selectedButton.name == 'button_vertical_box':
                name = 'Vertical box'
                content = Container(name, gtk.HBox(), self, widget.parentContainer)
                widget.add_Content(content)

            if self.rootObject == None:
                self.rootObject = content

            widget.show_all()

    def printNode(self, node):
        if node:
            print node.containerName
            for child in node.childObjects:
                self.printNode(child.content)

    def prehliadka(self, widget):
        for x in self.rootObject.childObjects:
            print x.content
        if self.rootObject != None:
            self.printNode(self.rootObject)

    def clearProperties(self):
        if self.lastHighligted:
            self.lastHighligted.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("black"))
        self.wTree.get_widget("label_name").set_text('')
        box = self.wTree.get_widget('vbox_properties')
        for w in box.children():
            box.remove(w)

    def clearAll(self):
        self.rootObject = None
        self.count = 1
        vbox = self.wTree.get_widget('vboxContent')
        for c in vbox.children():
            vbox.remove(c)
        vbox.pack_start(SimpleContent(None,self))
        vbox.show_all()
        self.clearProperties()

    def addWidget(self, eventBox, widget):
        eventBox.remove(eventBox.get_Label())
        eventBox.disconnect(eventBox.enterNotifyHandler)
        eventBox.disconnect(eventBox.buttonReleaseHandler)
        content = None
        if widget.name == 'button_horizontal_box':
            name = 'Horizontal box'
            content = Container(name, gtk.VBox(), self, eventBox.parentContainer)
            eventBox.add_Content(content)
        elif widget.name == 'button_vertical_box':
            name = 'Vertical box'
            content = Container(name, gtk.HBox(), self, eventBox.parentContainer)
            eventBox.add_Content(content)

        if self.rootObject == None:
            self.rootObject = content

        eventBox.show_all()