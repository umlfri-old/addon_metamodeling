import gtk
import os
from lxml import etree
from simpleContent import SimpleContent
from dragSourceEventBox import DragSourceEventBox
from expand import Expand
from colorChooserButton import ColorChooserButton
from pythonValue import PythonValue
from elementValue import ElementValue
from shadow import Shadow
from valueValidator import ValueValidator
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

        self.buttonDelete = gtk.Button('Delete case')
        self.buttonDelete.connect('clicked', self.deleteCase)
        self.buttonDelete.set_sensitive(False)

        sc = SimpleContent(self,manager)
        self.notebook = gtk.Notebook()
        #self.notebook.connect('switch-page', self.switchPage)
        self.notebook.connect('focus-in-event', self.showProperties)
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
        if self in self.manager.switchList:
            self.manager.wTree.get_widget('button_save').grab_focus()
            self.manager.switchList = []
            return
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
        vbox = gtk.HBox()
        vbox.pack_start(label,False)
        vbox.pack_end(ElementValue(self,'Case value'),False)
        box.pack_start(vbox,False)
        self.conditionValue.set_text(self.notebook.get_tab_label_text(self.notebook.get_nth_page(self.notebook.get_current_page())))
        box.pack_start(self.conditionValue,False)
        box.pack_start(gtk.Label(' '),False)

        button = gtk.Button('Add new case')
        button.connect('clicked', self.addCase)
        box.pack_start(button,False)
        box.pack_start(gtk.Label(' '),False)

        box.pack_start(self.buttonDelete,False)
        if len(self.childObjects) > 1:
            self.buttonDelete.set_sensitive(True)

        box.pack_start(gtk.Label(' '),False)
        if self.expand:
            box.pack_start(self.expand, False)
            box.pack_start(gtk.Label(' '),False)
        box.show_all()
        self.manager.wTree.get_widget('button_save').grab_focus()

    def add_New_Simple_Content(self):
        pass

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

    #def setElementValue(self, attrib, value):
    #    if attrib == 'Fill color':
    #        self.fillColorButton.color = '#'+value
    #        self.fillColorButton.set_label(self.fillColorButton.color)
    #    elif attrib == 'Border color':
    #        self.borderColorButton.color = '#'+value
    #        self.borderColorButton.set_label(self.borderColorButton.color)

    def colorChanged(self, newColor, attrib):
        pass

    def addCase(self, w):
        sc = SimpleContent(self,self.manager)
        self.notebook.append_page(sc, gtk.Label('Case'))
        self.notebook.show_all()
        self.childObjects.append(sc)
        self.buttonDelete.set_sensitive(True)
        self.notebook.set_page(-1)

    def deleteCase(self, w):
        if self.notebook.get_n_pages() > 1:
            dialog = gtk.MessageDialog(None,0,gtk.MESSAGE_QUESTION,gtk.BUTTONS_YES_NO,'Delete case with whole content?')
            response = dialog.run()
            if response == gtk.RESPONSE_YES:
                self.childObjects.remove(self.notebook.get_nth_page(self.notebook.get_current_page()))
                self.notebook.remove_page(self.notebook.get_current_page())
            dialog.destroy()
        if len(self.childObjects) == 1:
            self.buttonDelete.set_sensitive(False)

    def setElementValue(self, attrib, value):
        if attrib == 'Switch value':
            self.switchValue.set_text(value)
        elif attrib == 'Case value':
            self.conditionValue.set_text(value)

    def switchPage(self, notebook, par1, page_num):
        print notebook, par1
        self.conditionValue.disconnect(self.signalHandler)
        self.showProperties(None, None)
        self.conditionValue.set_text(self.notebook.get_tab_label_text(self.notebook.get_nth_page(page_num)))
        self.signalHandler = self.conditionValue.connect('changed', self.conditionChanged)


    def conditionChanged(self, w):
        self.notebook.set_tab_label_text(self.notebook.get_nth_page(self.notebook.get_current_page()),self.conditionValue.get_text())

    def getApp(self):
        app = etree.Element('Switch')
        app.attrib['value'] = self.switchValue.get_text()
        for page in self.notebook:
            case = etree.Element('Case')
            case.attrib['condition'] = self.notebook.get_tab_label_text(page)
            if page.content != None:
                case.append(page.content.getApp())
            app.append(case)
        return app

    @staticmethod
    def validate(element, dataElement):
        value = element.get('value')
        if value == '' or not value.strip():
            return False, 'Missing value in switch.'
        if not ValueValidator.validate(value, dataElement):
            return False, 'Unknown element attribute for switch value: ' + value
        for child in element.iter('Case'):
            if child.getparent() == element:
                caseValue = child.get('condition')
                if not ValueValidator.validate(caseValue, dataElement):
                    return False, 'Unknown element attribute for case value: ' + caseValue
                if caseValue == '' or not caseValue.strip():
                    return False, 'Missing case value in switch.'
                if child.getchildren() == []:
                    return False, 'Missing content for case in switch. Add some or delete case.'
        return True, None