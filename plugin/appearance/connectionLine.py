import gtk
import os
from dragSourceEventBox import DragSourceEventBox
from colors2 import colors
from pythonValue import PythonValue
from elementValue import ElementValue
from colorChooserButton import ColorChooserButton

class ConnectionLine(DragSourceEventBox):
    def __init__(self, manager, parent):
        DragSourceEventBox.__init__(self, self)
        self.manager = manager
        self.parentContainer = parent
        self.lineStyle = gtk.combo_box_new_text()

        self.buttonColor = ColorChooserButton(self, 'Select line color')

        self.lineStyle.append_text('solid')
        self.lineStyle.append_text('dot')
        self.lineStyle.set_active(0)
        self.lineStyle.connect('changed', self.styleChanged)

        self.widthSpin = gtk.SpinButton(gtk.Adjustment(1,1,10000,1,10,0),0.0,0)
        self.widthSpin.set_editable(False)
        self.widthSpin.connect('changed', self.widthChanged)

        self.beginSpin = gtk.SpinButton(gtk.Adjustment(0.0,0.0,1.0,0.01,0.1,0),0.01,2)
        self.beginSpin.set_editable(False)
        self.beginSpin.connect('changed', self.longChanged)

        self.endSpin = gtk.SpinButton(gtk.Adjustment(1.0,0.0,1.0,0.01,0.1,0),0.01,2)
        self.endSpin.set_editable(False)
        self.endSpin.connect('changed', self.longChanged)

        self.drawArea = None
        self.box = None
        self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("black"))

        self.eB = gtk.EventBox()
        self.eB.set_border_width(2)

        self.createContent()
        self.connect('button-press-event', self.showProperties)

        self.eB.add(self.box)
        self.add(self.eB)

    def styleChanged(self, w):
        self.exposeLine(self.drawArea, None)
        self.drawArea.queue_draw()

    def widthChanged(self, w):
        self.exposeLine(self.drawArea, None)
        self.drawArea.queue_draw()

    def longChanged(self, w):
        self.exposeLine(self.drawArea, None)
        self.drawArea.queue_draw()

    def createContent(self):
        self.box = gtk.HBox()
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
        gc.set_values(line_width=int(self.widthSpin.get_value()))
        if self.lineStyle.get_active() == 0:
            gc.set_values(line_style=gtk.gdk.LINE_SOLID)
        else:
            gc.set_values(line_style=gtk.gdk.LINE_ON_OFF_DASH)
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
        if x-75 < 40:
            x1 = 40
        else:
            x1 = x-75
        drawArea.set_size_request(x1, 7)
        x, y = drawArea.window.get_size()
        start = int((self.beginSpin.get_value()*x1))
        #end = x1 - int(((1-self.endSpin.get_value())*x1))
        end = int((self.endSpin.get_value()*x1))
        drawArea.window.draw_line(gc, start, y/2, end, y/2)
        gc.foreground = tempColor

    def showProperties(self, widget, w):
        if self.manager.lastHighligted:
            self.manager.lastHighligted.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("black"))
        self.manager.lastHighligted = self
        self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("green"))
        box = self.manager.wTree.get_widget('vbox_properties')
        for w in box.children():
            box.remove(w)
        labelColor = gtk.Label('Line color')
        labelColor.set_alignment(0.01, 0.5)
        hBox = gtk.HBox()
        hBox.pack_start(labelColor,False)
        hBox.pack_end(PythonValue(self,'Line color'),False)
        hBox.pack_end(ElementValue(self,'Line color'),False)
        box.pack_start(hBox, False)
        box.pack_start(self.buttonColor, False)
        box.pack_start(gtk.Label(' '),False)

        labelType = gtk.Label('Line style')
        labelType.set_alignment(0.01, 0.5)
        box.pack_start(labelType, False)
        box.pack_start(self.lineStyle, False)
        box.pack_start(gtk.Label(' '),False)

        labelWidth = gtk.Label('Line width')
        labelWidth.set_alignment(0.01, 0.5)
        box.pack_start(labelWidth, False)
        box.pack_start(self.widthSpin, False)
        box.pack_start(gtk.Label(' '),False)

        labelBegin = gtk.Label('Begin')
        labelBegin.set_alignment(0.01, 0.5)
        box.pack_start(labelBegin, False)
        box.pack_start(self.beginSpin, False)
        box.pack_start(gtk.Label(' '),False)

        labelEnd = gtk.Label('End')
        labelEnd.set_alignment(0.01, 0.5)
        box.pack_start(labelEnd, False)
        box.pack_start(self.endSpin, False)
        box.pack_start(gtk.Label(' '),False)

        box.show_all()

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
        app = '<ConnectionLine '
        if self.buttonColor.color:
            app += 'color="' + self.buttonColor.color + '" '
        app += 'style="' + self.lineStyle.get_active_text() + '" '
        app += 'width="' + str(int(self.widthSpin.get_value())) + '" '
        app += 'begin="' + str(int(self.beginSpin.get_value())) + '" '
        app += 'end="' + str(int(self.endSpin.get_value())) + '" '
        app += '/>'
        return app