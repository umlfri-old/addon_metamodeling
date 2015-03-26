import gtk
import os
from simpleContent import SimpleContent
from dragSourceEventBox import DragSourceEventBox
from expand import Expand
from colorChooserButton import ColorChooserButton
from pythonValue import PythonValue
from elementValue import ElementValue
from shadow import Shadow
import pango
import constants

class Switch(gtk.EventBox):
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

        self.switchValue = gtk.Entry()
        self.conditionValue = gtk.Entry()
        self.signalHandler = self.conditionValue.connect('changed', self.conditionChanged)

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
        self.notebook = gtk.Notebook()
        self.notebook.connect('switch-page', self.switchPage)
        self.notebook.append_page(sc, gtk.Label('Case'))
        self.box.pack_start(self.notebook)
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

    def deleteChild(self, child):
        for c in self.childObjects:
            if c.content == child:
                self.childObjects.remove(c)
                self.notebook.remove_page(self.notebook.current_page())
        if self.notebook.get_current_page() == -1:
            self.addCase(None)

    def showProperties(self, widget, w):
        if self.manager.lastHighligted:
            self.manager.lastHighligted.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("black"))
        self.manager.lastHighligted = self
        self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("green"))
        box = self.manager.wTree.get_widget('vbox_properties')
        for w in box.children():
            box.remove(w)

        label = gtk.Label('Switch value')
        label.set_alignment(0.01, 0.5)
        vbox = gtk.HBox()
        vbox.pack_start(label,False)
        vbox.pack_end(ElementValue(self,'Switch value'),False)
        box.pack_start(vbox,False)
        box.pack_start(self.switchValue,False)
        box.pack_start(gtk.Label(' '),False)

        label = gtk.Label('Case condition')
        label.set_alignment(0.01, 0.5)

        self.conditionValue.set_text(self.notebook.get_tab_label_text(self.notebook.get_nth_page(self.notebook.get_current_page())))
        box.pack_start(label,False)
        box.pack_start(self.conditionValue,False)
        box.pack_start(gtk.Label(' '),False)

        button = gtk.Button('Add new case')
        button.connect('clicked', self.addCase)
        box.pack_start(button,False)
        box.pack_start(gtk.Label(' '),False)

        button = gtk.Button('Delete case')
        button.connect('clicked', self.deleteCase)
        box.pack_start(button,False)

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

    def setElementValue(self, attrib, value):
        if attrib == 'Fill color':
            self.fillColorButton.color = '#'+value
            self.fillColorButton.set_label(self.fillColorButton.color)
        elif attrib == 'Border color':
            self.borderColorButton.color = '#'+value
            self.borderColorButton.set_label(self.borderColorButton.color)

    def colorChanged(self, newColor, attrib):
        pass

    def addCase(self, w):
        sc = SimpleContent(self,self.manager)
        self.notebook.append_page(sc, gtk.Label('Case'))
        self.notebook.show_all()
        self.childObjects.append(sc)

    def deleteCase(self, w):
        if self.notebook.get_n_pages() > 1:
            dialog = gtk.MessageDialog(None,0,gtk.MESSAGE_QUESTION,gtk.BUTTONS_YES_NO,'Delete case with whole content?')
            response = dialog.run()
            if response == gtk.RESPONSE_YES:
                self.childObjects.remove(self.notebook.get_nth_page(self.notebook.get_current_page()))
                self.notebook.remove_page(self.notebook.get_current_page())
            dialog.destroy()

    def setElementValue(self, attrib, value):
        self.switchValue.set_text(value)

    def switchPage(self, notebook, par1, page_num):
        self.conditionValue.disconnect(self.signalHandler)
        self.conditionValue.set_text(self.notebook.get_tab_label_text(self.notebook.get_nth_page(page_num)))
        self.signalHandler = self.conditionValue.connect('changed', self.conditionChanged)

    def conditionChanged(self, w):
        self.notebook.set_tab_label_text(self.notebook.get_nth_page(self.notebook.get_current_page()),self.conditionValue.get_text())

    def getApp(self):
        if self.switchValue.get_text() == '':
            return ''
        app = '<Switch value="' + self.switchValue.get_text() + '">'
        someContent = False
        for page in self.notebook:
            if page.content != None:
                app += '<Case condition="' + self.notebook.get_tab_label_text(page) + '">'
                app += page.content.getApp()
                app += '</Case>'
                someContent = True
        if not someContent:
            return ''
        app += '</Switch>'
        return app