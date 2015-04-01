import gtk
import os
from simpleContent import SimpleContent
from dragSourceEventBox import DragSourceEventBox
from expand import Expand
from colorChooserButton import ColorChooserButton
from pythonValue import PythonValue
from elementValue import ElementValue
from shadow import Shadow
from diamond import Diamond
import constants
from rectangleCorner import RectangleCorner
from rectangleSide import RectangleSide

class Rectangle(Diamond):
    def __init__(self, name, box, manager, parent):
        Diamond.__init__(self, name, box, manager, parent)
        self.leftTopCorner = RectangleCorner(self, 'Left top corner')
        self.rightTopCorner = RectangleCorner(self, 'Right top corner')
        self.leftBotCorner = RectangleCorner(self, 'Left bottom corner')
        self.rightBotCorner = RectangleCorner(self, 'Right bottom corner')
        self.leftSide = RectangleSide(self, 'Left side')
        self.topSide = RectangleSide(self, 'Top side')
        self.rightSide = RectangleSide(self, 'Right side')
        self.botSide = RectangleSide(self, 'Bottom side')
        self.propBox = gtk.VBox()
        self.propBox.set_border_width(3)
        self.createProperties()

    def createProperties(self):
        hbox = gtk.HBox()
        label = gtk.Label('Fill color')
        label.set_alignment(0.01, 0.5)
        hbox.pack_start(label,False)
        hbox.pack_end(PythonValue(self,'Fill color'),False)
        hbox.pack_end(ElementValue(self,'Fill color'),False)
        self.propBox.pack_start(hbox,False)
        self.propBox.pack_start(self.fillColorButton, False)

        self.propBox.pack_start(gtk.Label(' '),False)

        hbox = gtk.HBox()
        label = gtk.Label('Border color')
        label.set_alignment(0.01, 0.5)
        hbox.pack_start(label,False)
        hbox.pack_end(PythonValue(self,'Border color'),False)
        hbox.pack_end(ElementValue(self,'Border color'),False)
        self.propBox.pack_start(hbox,False)
        self.propBox.pack_start(self.borderColorButton, False)
        self.propBox.pack_start(gtk.Label(' '),False)

        self.propBox.pack_start(self.leftTopCorner, False)
        self.propBox.pack_start(gtk.Label(' '),False)

        self.propBox.pack_start(self.rightTopCorner, False)
        self.propBox.pack_start(gtk.Label(' '),False)

        self.propBox.pack_start(self.leftBotCorner, False)
        self.propBox.pack_start(gtk.Label(' '),False)

        self.propBox.pack_start(self.rightBotCorner, False)
        self.propBox.pack_start(gtk.Label(' '),False)

        self.propBox.pack_start(self.leftSide, False)
        self.propBox.pack_start(gtk.Label(' '),False)

        self.propBox.pack_start(self.topSide, False)
        self.propBox.pack_start(gtk.Label(' '),False)

        self.propBox.pack_start(self.rightSide, False)
        self.propBox.pack_start(gtk.Label(' '),False)

        self.propBox.pack_start(self.botSide, False)
        self.propBox.pack_start(gtk.Label(' '),False)

        self.propBox.pack_start(self.shadow, False)
        self.propBox.pack_start(gtk.Label(' '),False)
        if self.expand:
            self.propBox.pack_start(self.expand, False)
            self.propBox.pack_start(gtk.Label(' '),False)

        self.scrolWin = gtk.ScrolledWindow()
        self.scrolWin.add_with_viewport(self.propBox)

    def showProperties(self, widget, w):
        if self.manager.lastHighligted:
            self.manager.lastHighligted.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("black"))
        self.manager.lastHighligted = self
        self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("green"))
        box2 = self.manager.wTree.get_widget('vbox_properties')
        for w in box2.children():
            box2.remove(w)

        box2.add(self.scrolWin)
        box2.show_all()

    def setElementValue(self, attrib, value):
        if attrib == 'Fill color':
            self.fillColorButton.color = value
            if value:
                self.fillColorButton.set_label(self.fillColorButton.color)
            else:
                self.fillColorButton.set_label('')
        elif attrib == 'Border color':
            self.borderColorButton.color = value
            if value:
                self.borderColorButton.set_label(self.borderColorButton.color)
            else:
                self.borderColorButton.set_label('')

    def colorChanged(self, newColor, attrib):
        pass

    def getApp(self):
        app = '<Rectangle '
        if self.fillColorButton.color:
            app += 'fill="' + self.fillColorButton.color + '" '
        if self.borderColorButton.color:
            app += 'border="' + self.borderColorButton.color + '" '
        if self.leftTopCorner.checkBox.get_active():
            app += 'lefttop="' + self.leftTopCorner.getXMLFormat() + '" '
        if self.rightTopCorner.checkBox.get_active():
            app += 'righttop="' + self.rightTopCorner.getXMLFormat() + '" '
        if self.leftBotCorner.checkBox.get_active():
            app += 'leftbottom="' + self.leftBotCorner.getXMLFormat() + '" '
        if self.rightBotCorner.checkBox.get_active():
            app += 'rightbottom="' + self.rightBotCorner.getXMLFormat() + '" '
        if self.leftSide.checkBox.get_active():
            app += 'left="' + self.leftSide.getXMLFormat() + '" '
        if self.rightSide.checkBox.get_active():
            app += 'right="' + self.rightSide.getXMLFormat() + '" '
        if self.topSide.checkBox.get_active():
            app += 'top="' + self.topSide.getXMLFormat() + '" '
        if self.botSide.checkBox.get_active():
            app += 'bottom="' + self.botSide.getXMLFormat() + '" '
        app += '>'
        if self.childObjects[0].content != None:
            app += self.childObjects[0].content.getApp()
        app += '</Rectangle>'
        if self.shadow.padding > 0 or self.shadow.buttonColor.color:
            app = '<Shadow ' + self.shadow.getXMLFormat() + '>' + app + '</Shadow>'
        return app