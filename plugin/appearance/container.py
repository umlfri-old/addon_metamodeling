import gtk
import os
from lxml import etree
from simpleContent import SimpleContent
from dragSourceEventBox import DragSourceEventBox
from align import Align
from expand import Expand
from parentButton import ParentButton
from baseElement import BaseElement

class Container(BaseElement):
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

    def deleteChild(self, child):
        for c in self.box.children():
            if c.content == child:
                self.box.remove(c)
                self.childObjects.remove(c)

    def showProperties(self, widget, w):
        if self.manager.lastHighligted:
            self.manager.lastHighligted.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("black"))
        self.manager.lastHighligted = self
        self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("green"))
        box = self.manager.wTree.get_widget('vbox_properties')
        for w in box.children():
            box.remove(w)
        if self.expand:
            box.pack_start(self.expand, False)
            box.pack_start(gtk.Label(' '),False)
        box.pack_start(self.align,False)
        #box.pack_start(gtk.Label(' '),False)
        #box.pack_start(ParentButton(self),False)
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
        self.changePacking()

    def isHBox(self):
        if type(self.box).__name__ == 'HBox':
            return True
        return False

    def changePacking(self):
        tempContainer = []
        for x in self.box.children():
            tempContainer.append(x)
            self.box.remove(x)
        for x in tempContainer:
            if type(x.content).__name__ == 'TextBox':
                self.box.pack_start(x,False)
            elif type(x.content).__name__ == 'Line':
                self.box.pack_start(x,False)
            elif type(x.content).__name__ == 'Icon':
                self.box.pack_start(x,False)
            #elif type(x.content).__name__ == 'Padding':
            #    self.box.pack_start(x,False)
            #elif type(x.content).__name__ == 'Sizer':
            #    self.box.pack_start(x,False)
            #elif type(x.content).__name__ == 'Proportional':
            #    self.box.pack_start(x,False)
            #elif type(x.content).__name__ == 'Condition':
            #    self.box.pack_start(x,False)
            #elif type(x.content).__name__ == 'Loop':
            #    self.box.pack_start(x,False)
            #elif type(x.content).__name__ == 'Container':
            #    if x.content.isHBox():
            #        self.box.pack_start(x,False)
            #    else:
            #        self.box.pack_start(x)
            else:
                self.box.pack_start(x)

    def xChanged(self):
        pass

    def yChanged(self):
        pass

    def getApp(self):
        if self.isHBox():
            app = etree.Element('VBox')
        else:
            app = etree.Element('HBox')
        i = 0
        expand =''
        for child in self.childObjects:
            if child.content:
                if type(child.content).__name__ != 'Line':
                    if child.content.expand.isTrue():
                        if expand != '':
                            expand += ' '
                        expand += str(i)
            i += 1
        if expand != '':
            app.attrib['expand'] = expand
        for child in self.childObjects:
            if child.content:
                app.append(child.content.getApp())
        if self.align.isAlignSet():
            align = self.align.getXMLFormat()
            align.append(app)
            return align
        return app

    @staticmethod
    def validate(element, dataElement):
        childs = []
        for child in element.iter():
            if child != element:
                childs.append(child)
        if len(childs) == 0:
            return False, 'Missing content in '+ element.tag + '. Add some or delete ' + element.tag + '.'
        else:
            return True, None

    '''def addWidget(self, widget):
        sc = self.box.get_children()[0]
        sc.remove(sc.get_Label())
        sc.disconnect(sc.enterNotifyHandler)
        sc.disconnect(sc.buttonReleaseHandler)
        sc.content = widget
        #widget.unparent()
        sc.add(widget)
        #self.childObjects.append(widget)
        self.add_New_Simple_Content()

    def changeParent(self, parentChild, child):
        for i in range(0, len(self.childObjects)):
            print self.childObjects[i].content, child
            if self.childObjects[i].content == child:
                self.childObjects[i].remove(child)
                self.childObjects[i].add(parentChild)
                self.childObjects[i].content == parentChild
                child.parentContainer = parentChild'''
