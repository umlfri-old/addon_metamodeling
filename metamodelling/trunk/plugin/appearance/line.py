import gtk
import os
from dragSourceEventBox import DragSourceEventBox
from colors2 import colors
from shadow import Shadow
from pythonValue import PythonValue
from elementValue import ElementValue
from expand import Expand
from colorChooserButton import ColorChooserButton

class Line(DragSourceEventBox):
    def __init__(self, manager, parent):
        DragSourceEventBox.__init__(self, self)
        self.manager = manager
        self.parentContainer = parent
        self.lineType = ''
        self.customLine = False #false=can not change hor/ver, True = user can change hor/ver
        tempParent = parent
        while tempParent:
            if type(tempParent).__name__ == 'Container':
                if tempParent.isHBox():
                    self.lineType = 'vertical'
                else:
                    self.lineType = 'horizontal'
                break
            else:
                tempParent = tempParent.parent
        if self.lineType == '':
            self.lineType = 'horizontal'
            self.customLine = True

        self.comboType = gtk.combo_box_new_text()
        self.comboType.append_text('horizontal')
        self.comboType.append_text('vertical')

        self.drawArea = None
        self.box = None
        self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("black"))
        self.shadow = Shadow(self)

        self.eB = gtk.EventBox()
        self.eB.set_border_width(2)

        self.createContent()
        self.connect('button-press-event', self.showProperties)

        self.eB.add(self.box)
        self.add(self.eB)

        if type(self.parentContainer).__name__ == 'Container':
            self.drag_source_set(gtk.gdk.BUTTON1_MASK,[],0)
            self.drag_dest_set(0,[],0)
            self.connect('drag_motion', self.motion_cb)
            self.connect('drag_drop', self.drop_cb)

        self.buttonColor = ColorChooserButton(self, 'Select line color')

    def createContent(self):
        if self.lineType == 'horizontal':
            self.box = gtk.HBox()
        else:
            self.box = gtk.VBox()
        label = gtk.Label('  Line  ')
        self.drawArea = gtk.DrawingArea()
        self.drawArea.connect('expose-event',self.exposeLine)

        iconEvent = gtk.EventBox()
        iconEvent.set_border_width(2)
        iconEvent.connect('button-release-event', self.deleteClicked)
        icon = gtk.Image()
        icon.set_from_file(os.path.split(os.path.realpath(__file__))[0]+'/delete.png')
        iconEvent.add(icon)

        self.box.pack_start(label,False)
        self.box.pack_start(self.drawArea,False)
        self.box.pack_end(iconEvent,False,True,2)

    def exposeLine(self, drawArea, data):
        style = drawArea.get_style()
        gc = style.fg_gc[gtk.STATE_NORMAL]
        gc.set_values(line_style=gtk.gdk.LINE_SOLID)
        gc.set_values(line_width=1)
        tempColor = gc.foreground
        if self.buttonColor.color:
            if not self.buttonColor.color.startswith('#'):
                try:
                    gc.foreground = drawArea.get_colormap().alloc(gtk.gdk.Color(self.buttonColor.color))
                except ValueError:
                    gc.foreground = drawArea.get_colormap().alloc(gtk.gdk.Color('#'+self.buttonColor.color))
            else:
                gc.foreground = drawArea.get_colormap().alloc(gtk.gdk.Color("black"))
        else:
            gc.foreground = drawArea.get_colormap().alloc(gtk.gdk.Color("black"))
        x, y = self.window.get_size()
        if self.lineType == 'horizontal':
            if x-75 < 40:
                x1 = 40
            else:
                x1 = x-75
            drawArea.set_size_request(x1, 7)
            x, y = drawArea.window.get_size()
            drawArea.window.draw_line(gc, 0, y/2, x1, y/2)
        else:
            if y-50 < 40:
                y1 = 40
            else:
                y1 = y-50
            drawArea.set_size_request(20, y1)
            x, y = drawArea.window.get_size()
            drawArea.window.draw_line(gc, x/2, 0, x/2, y1)
        gc.foreground = tempColor

    def showProperties(self, widget, w):
        if self.manager.lastHighligted:
            self.manager.lastHighligted.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("black"))
        self.manager.lastHighligted = self
        self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("green"))
        box = self.manager.wTree.get_widget('vbox_properties')
        for w in box.children():
            box.remove(w)
        labelType = gtk.Label('Type')
        labelType.set_alignment(0.01, 0.5)
        if self.lineType == 'horizontal':
            self.comboType.set_active(0)
        else:
            self.comboType.set_active(1)
        self.comboType.connect('changed', self.changeLineType)

        labelColor = gtk.Label('Line color')
        labelColor.set_alignment(0.01, 0.5)
        hBox = gtk.HBox()
        hBox.pack_start(labelColor,False)
        hBox.pack_end(PythonValue(self,'Line color'),False)
        hBox.pack_end(ElementValue(self,'Line color'),False)

        if self.customLine:
            box.pack_start(labelType, False)
            box.pack_start(self.comboType, False)
            box.pack_start(gtk.Label(' '),False)
        box.pack_start(hBox, False)
        box.pack_start(self.buttonColor, False)
        box.pack_start(gtk.Label(' '),False)
        box.pack_start(self.shadow,False)
        box.show_all()

    def changeLineType(self, combo):
        self.lineType = combo.get_active_text()
        self.eB.remove(self.box)
        self.createContent()
        self.eB.add(self.box)
        self.show_all()

    def deleteClicked(self, widget, w):
        dialog = gtk.MessageDialog(None,0,gtk.MESSAGE_QUESTION,gtk.BUTTONS_YES_NO,'Delete line?')
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

    def setElementValue(self, attrib, value):
        self.buttonColor.color = value
        if value:
            self.buttonColor.set_label(self.buttonColor.color)
        else:
            self.buttonColor.set_label('')
        self.exposeLine(self.drawArea, None)

    def colorChanged(self, newColor, attrib):
        if attrib == 'Select line color':
            self.exposeLine(self.drawArea, None)

    def getApp(self):
        app = '<Line '
        if self.lineType != '':
            app += 'type="' + self.lineType + '" '
        if self.buttonColor.color:
            app += 'color="' + self.buttonColor.color + '" '
        app += '/>'
        if self.shadow.padding > 0 or self.shadow.buttonColor.color:
            app = '<Shadow ' + self.shadow.getXMLFormat() + '>' + app + '</Shadow>'
        return app

    def setLineType(self, type):
        self.lineType = type
        if type == 'horizontal':
            self.comboType.set_active(0)
        if type == 'vertical':
            self.comboType.set_active(1)
        self.changeLineType(self.comboType)
