import gtk
import os
import pango
from dragSourceEventBox import DragSourceEventBox
from align import Align
from shadow import Shadow
from elementValue import ElementValue
from pythonValue import PythonValue
from expand import Expand
from colorChooserButton import ColorChooserButton

class TextBox(DragSourceEventBox):
    def __init__(self, manager, parent):
        DragSourceEventBox.__init__(self, self)
        self.manager = manager
        self.parentContainer = parent
        #self.color = None
        self.font = gtk.FontSelection()
        #self.font.set_font_name('sans 12')
        #self.font.set_font_name('Serif Bold Italic 12 ')
        self.shadow = Shadow(self)
        self.expand = None
        if type(self.parentContainer).__name__ == 'Container':
            self.expand = Expand(self)
        self.align = Align(self)

        self.buttonTextColor = ColorChooserButton(self, 'Select text color')
        #self.buttonTextColor = gtk.Button(' ')
        #self.buttonTextColor.set_alignment(0.01, 0.5)
        #self.buttonTextColor.connect('clicked', self.chooseTextColor)

        self.textEntry = gtk.Entry()
        self.textEntry.connect('changed', self.textEdited)

        self.buttonFont = gtk.Button()
        self.buttonFont.set_label(self.font.get_font_name())
        self.buttonFont.set_alignment(0.01, 0.5)
        self.buttonFont.connect('clicked', self.changeFont)

        self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("black"))
        eB = gtk.EventBox()
        eB.set_border_width(2)
        hBox = gtk.HBox()
        label = gtk.Label('  Text:  ')
        self.textEvent = gtk.EventBox()
        self.textAlign = gtk.Alignment(self.align.xValue, 0.5, 1.0, 1.0)
        self.text = gtk.Label('')
        self.text.set_alignment(0.01, 0.5)
        self.textAlign.add(self.text)
        self.textEvent.add(self.textAlign)
        self.text.connect('button-press-event', self.showProperties)

        iconEvent = gtk.EventBox()
        iconEvent.set_border_width(2)
        iconEvent.connect('button-release-event', self.deleteClicked)
        icon = gtk.Image()
        icon.set_from_file(os.path.split(os.path.realpath(__file__))[0]+'/delete.png')
        iconEvent.add(icon)

        self.connect('button-press-event', self.showProperties)

        hBox.pack_start(label,False)
        hBox.pack_start(self.textEvent,True,True)
        hBox.pack_start(iconEvent,False,True,2)

        eB.add(hBox)
        self.add(eB)

        if type(self.parentContainer).__name__ == 'Container':
            self.drag_source_set(gtk.gdk.BUTTON1_MASK,[],0)
            self.drag_dest_set(0,[],0)
            self.connect('drag_motion', self.motion_cb)
            self.connect('drag_drop', self.drop_cb)
            self.text.drag_dest_set(0,[],0)
            self.text.connect('drag_motion', self.motion_cb)
            self.text.connect('drag_drop', self.drop_cb)

    def textEdited(self, entry):
        self.text.set_text(self.textEntry.get_text())

    def deleteClicked(self, widget, w):
        dialog = gtk.MessageDialog(None,0,gtk.MESSAGE_QUESTION,gtk.BUTTONS_YES_NO,'Delete text box?')
        response = dialog.run()
        if response == gtk.RESPONSE_YES:
            if self.parentContainer == None:
                self.manager.clearAll()
            else:
                self.parentContainer.deleteChild(self)
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

    def showProperties(self, widget, w):
        if self.manager.lastHighligted:
            self.manager.lastHighligted.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("black"))
        self.manager.lastHighligted = self
        self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("green"))
        box = self.manager.wTree.get_widget('vbox_properties')
        for w in box.children():
            box.remove(w)
        labelText = gtk.Label('Text')
        labelText.set_alignment(0.01, 0.5)
        textHbox = gtk.HBox()
        textHbox.pack_start(labelText,False)
        textHbox.pack_end(PythonValue(self,'Text'),False)
        textHbox.pack_end(ElementValue(self,'Text'),False)
        box.pack_start(textHbox,False)

        self.textEntry.set_text(self.text.get_text())
        labelColor = gtk.Label('Text color')
        labelColor.set_alignment(0.01, 0.5)

        labelFont = gtk.Label('Text font')
        labelFont.set_alignment(0.01, 0.5)
        fontHbox = gtk.HBox()
        fontHbox.pack_start(labelFont,False)
        fontHbox.pack_end(PythonValue(self,'Text font'),False)
        fontHbox.pack_end(ElementValue(self,'Text font'),False)

        box.pack_start(self.textEntry,False)
        box.pack_start(gtk.Label(' '),False)

        hbox = gtk.HBox()
        hbox.pack_start(labelColor,False)
        hbox.pack_end(PythonValue(self,'Text color'),False)
        hbox.pack_end(ElementValue(self,'Text color'),False)
        box.pack_start(hbox,False)

        box.pack_start(self.buttonTextColor,False)
        box.pack_start(gtk.Label(' '),False)
        box.pack_start(fontHbox, False)
        box.pack_start(self.buttonFont,False)
        box.pack_start(gtk.Label(' '),False)
        box.pack_start(self.align, False)
        box.pack_start(gtk.Label(' '),False)
        box.pack_start(self.shadow, False)
        if self.expand:
            box.pack_start(gtk.Label(' '),False)
            box.pack_start(self.expand, False)
        box.pack_start(gtk.Label(' '),False)
        box.show_all()

    def changeFont(self, button):
        dialog = gtk.FontSelectionDialog('Text font')
        if self.font:
            dialog.set_font_name(self.font.get_font_name())
        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            self.font = dialog.get_font_selection()
            self.text.modify_font(pango.FontDescription(self.font.get_font_name()))
            button.set_label(self.font.get_font_name())
        dialog.destroy()

    def xChanged(self):
        self.text.set_alignment(self.align.xValue, 0.5)

    def yChanged(self):
        self.textAlign.set(self.align.xValue, self.align.yValue, 1.0, 0.0)

    def setElementValue(self, attrib, value):
        if attrib == 'Text color':
            self.buttonTextColor.color = value
            if value:
                self.buttonTextColor.set_label(self.buttonTextColor.color)
            else:
                self.buttonTextColor.set_label('')
            self.text.modify_fg(gtk.STATE_NORMAL, gtk.gdk.Color('black'))
        elif attrib == 'Text':
            if value:
                self.textEntry.set_text(value)
            else:
                self.textEntry.set_text('')
            self.textEdited(None)
        elif attrib == 'Text font':
            if value:
                self.buttonFont.set_label(value)
            else:
                self.buttonFont.set_label('')
            self.font = None

    def colorChanged(self, newColor, attrib):
        if attrib == 'Select text color':
            self.text.modify_fg(gtk.STATE_NORMAL, newColor)

    def getApp(self):
        app = '<TextBox '
        app += 'text="' + self.textEntry.get_text() + '" '
        if self.buttonTextColor.color:
            app += 'color="' + self.buttonTextColor.color + '" '
        if self.buttonFont.get_label() != '':
            app += 'font="' + self.buttonFont.get_label() + '" '
        app += '/>'
        if self.shadow.padding > 0 or self.shadow.buttonColor.color:
            app = '<Shadow ' + self.shadow.getXMLFormat() + '>' + app + '</Shadow>'
        if self.align.isAlignSet():
            app = '<Align ' + self.align.getXMLFormat() + '>' + app + '</Align>'
        return app

    def setTextFont(self, font):
        self.font.set_font_name(font)
        self.text.modify_font(pango.FontDescription(font))
        self.buttonFont.set_label(font)

    def setTextColor(self, color):
        self.buttonTextColor.setColor(color)
        if not color.startswith('#'):
            try:
                self.text.modify_fg(gtk.STATE_NORMAL, gtk.gdk.Color(color))
            except ValueError:
                self.text.modify_fg(gtk.STATE_NORMAL, gtk.gdk.Color('#'+color))
        else:
            self.text.modify_fg(gtk.STATE_NORMAL, gtk.gdk.Color('black'))
