import gtk
import os
from lxml import etree
from dragSourceEventBox import DragSourceEventBox
from colors2 import colors
from pythonValue import PythonValue
from elementValue import ElementValue
from colorChooserButton import ColorChooserButton
from valueValidator import ValueValidator

class ConnectionArrow(DragSourceEventBox):
    def __init__(self, manager, parent):
        DragSourceEventBox.__init__(self, self)
        self.manager = manager
        self.parentContainer = parent

        self.arrowDirection = gtk.combo_box_new_text()
        self.arrowDirection.append_text('src -> dest')
        self.arrowDirection.append_text('dest -> src')
        self.arrowDirection.set_active(0)

        self.arrowStyle = gtk.combo_box_new_text()
        self.arrowStyle.append_text('simple')
        self.arrowStyle.append_text('triangle')
        self.arrowStyle.append_text('diamond')
        self.arrowStyle.append_text('circle')
        self.arrowStyle.append_text('square')
        self.arrowStyle.set_active(0)
        self.styleDict = {'simple':'simple_arrow', 'triangle':'triangle_arrow', 'diamond':'diamond_arrow', 'circle':'crosscircle_arrow', 'square':'square_arrow' }

        self.arrowColor = ColorChooserButton(self, 'Select arrow color')
        self.fillColor = ColorChooserButton(self, 'Select fill color')

        self.drawArea = None
        self.box = None
        self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("black"))

        self.eB = gtk.EventBox()
        self.eB.set_border_width(2)

        self.createContent()
        self.connect('button-press-event', self.showProperties)

        self.eB.add(self.box)
        self.add(self.eB)

        self.directionHandler = self.arrowDirection.connect('changed', self.directionChanged)
        self.styleHandler = self.arrowStyle.connect('changed', self.styleChanged)

    def directionChanged(self, widget):
        self.exposeLine(self.drawArea, None)
        self.drawArea.queue_draw()

    def styleChanged(self, widget):
        self.exposeLine(self.drawArea, None)
        self.drawArea.queue_draw()
        self.showProperties(None, None)

    def createContent(self):
        self.box = gtk.HBox()
        label = gtk.Label(' \n  Arrow  \n ')
        self.drawArea = gtk.DrawingArea()
        self.drawArea.connect('expose-event',self.exposeLine)
        self.drawArea.set_size_request(100, 30)

        iconEvent = gtk.EventBox()
        iconEvent.set_border_width(2)
        iconEvent.connect('button-release-event', self.deleteClicked)
        icon = gtk.Image()
        icon.set_from_file(os.path.split(os.path.realpath(__file__))[0]+'/delete.png')
        iconEvent.add(icon)

        self.box.pack_start(label,False)
        self.box.pack_start(self.drawArea,True, False,0)
        self.box.pack_end(iconEvent,False,True,2)

    def exposeLine(self, drawArea, data):
        style = drawArea.get_style()
        gc = style.fg_gc[gtk.STATE_NORMAL]
        gc.set_values(line_style=gtk.gdk.LINE_SOLID)
        gc.set_values(line_width=2)
        tempColor = gc.foreground
        if self.arrowColor.color:
            if not self.arrowColor.color.startswith('#'):
                try:
                    gc.foreground = drawArea.get_colormap().alloc(gtk.gdk.Color(self.arrowColor.color))
                except ValueError:
                    gc.foreground = drawArea.get_colormap().alloc(gtk.gdk.Color('#'+self.arrowColor.color))
            else:
                gc.foreground = drawArea.get_colormap().alloc(gtk.gdk.Color("black"))
        else:
            gc.foreground = drawArea.get_colormap().alloc(gtk.gdk.Color("black"))

        fill = None
        if self.fillColor.color:
            if not self.fillColor.color.startswith('#'):
                try:
                    fill = drawArea.get_colormap().alloc(gtk.gdk.Color(self.fillColor.color))
                except ValueError:
                    fill = drawArea.get_colormap().alloc(gtk.gdk.Color('#'+self.fillColor.color))
            else:
                fill = None
        else:
            fill = None

        x, y = drawArea.window.get_size()

        if self.arrowDirection.get_active() == 0:
            if self.arrowStyle.get_active_text() == 'simple':
                drawArea.window.draw_lines(gc,[(10,y/2),(50,y/2),(35,y/2-15)])
                drawArea.window.draw_lines(gc,[(50,y/2),(35,y/2+15)])
            elif self.arrowStyle.get_active_text() == 'triangle':
                drawArea.window.draw_lines(gc,[(10,y/2),(30,y/2)])
                drawArea.window.draw_polygon(gc, False,[(30,y/2-15),(30,y/2+15),(50,y/2)])
                if fill:
                    gc.foreground = fill
                    drawArea.window.draw_polygon(gc, True,[(31,y/2-13),(31,y/2+13),(49,y/2)])
            elif self.arrowStyle.get_active_text() == 'diamond':
                drawArea.window.draw_lines(gc,[(10,y/2),(30,y/2)])
                drawArea.window.draw_polygon(gc, False,[(30,y/2),(55,y/2-15),(80,y/2),(55,y/2+15)])
                if fill:
                    gc.foreground = fill
                    drawArea.window.draw_polygon(gc, True,[(32,y/2),(55,y/2-14),(79,y/2),(55,y/2+14)])
            elif self.arrowStyle.get_active_text() == 'circle':
                drawArea.window.draw_lines(gc,[(10,y/2),(30,y/2)])
                drawArea.window.draw_arc(gc, False, 30, y/2-15, 30, 30, 0, 360*64)
                if fill:
                    gc.foreground = fill
                    drawArea.window.draw_arc(gc, True, 31, y/2-14, 28, 28, 0, 360*64)
            elif self.arrowStyle.get_active_text() == 'square':
                drawArea.window.draw_lines(gc,[(10,y/2),(30,y/2)])
                drawArea.window.draw_polygon(gc, False,[(30,y/2),(45,y/2-15),(60,y/2),(45,y/2+15)])
                if fill:
                    gc.foreground = fill
                    drawArea.window.draw_polygon(gc, True,[(32,y/2),(45,y/2-14),(59,y/2),(45,y/2+14)])
        else:
            if self.arrowStyle.get_active_text() == 'simple':
                drawArea.window.draw_lines(gc,[(10,y/2),(50,y/2)])
                drawArea.window.draw_lines(gc,[(25,y/2-15),(10,y/2),(25,y/2+15)])
            elif self.arrowStyle.get_active_text() == 'triangle':
                drawArea.window.draw_lines(gc,[(30,y/2),(50,y/2)])
                drawArea.window.draw_polygon(gc, False,[(30,y/2-15),(30,y/2+15),(10,y/2)])
                if fill:
                    gc.foreground = fill
                    drawArea.window.draw_polygon(gc, True,[(29,y/2-13),(29,y/2+13),(11,y/2)])
            elif self.arrowStyle.get_active_text() == 'diamond':
                drawArea.window.draw_lines(gc,[(60,y/2),(80,y/2)])
                drawArea.window.draw_polygon(gc, False,[(10,y/2),(35,y/2-15),(60,y/2),(35,y/2+15)])
                if fill:
                    gc.foreground = fill
                    drawArea.window.draw_polygon(gc, True,[(12,y/2),(35,y/2-14),(59,y/2),(35,y/2+14)])
            elif self.arrowStyle.get_active_text() == 'circle':
                drawArea.window.draw_lines(gc,[(40,y/2),(60,y/2)])
                drawArea.window.draw_arc(gc, False, 10, y/2-15, 30, 30, 0, 360*64)
                if fill:
                    gc.foreground = fill
                    drawArea.window.draw_arc(gc, True, 11, y/2-14, 28, 28, 0, 360*64)
            elif self.arrowStyle.get_active_text() == 'square':
                drawArea.window.draw_lines(gc,[(40,y/2),(60,y/2)])
                drawArea.window.draw_polygon(gc, False,[(10,y/2),(25,y/2-15),(40,y/2),(25,y/2+15)])
                if fill:
                    gc.foreground = fill
                    drawArea.window.draw_polygon(gc, True,[(12,y/2),(25,y/2-14),(39,y/2),(25,y/2+14)])

        gc.foreground = tempColor

    def showProperties(self, widget, w):
        if self.manager.lastHighligted:
            self.manager.lastHighligted.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("black"))
        self.manager.lastHighligted = self
        self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("green"))
        box = self.manager.wTree.get_widget('vbox_properties')
        for w in box.children():
            box.remove(w)

        labelIndex = gtk.Label('Index')
        labelIndex.set_alignment(0.01, 0.5)
        box.pack_start(labelIndex, False)
        box.pack_start(self.arrowDirection, False)
        box.pack_start(gtk.Label(' '),False)

        labelStyle = gtk.Label('Arrow style')
        labelStyle.set_alignment(0.01, 0.5)
        box.pack_start(labelStyle, False)
        box.pack_start(self.arrowStyle, False)
        box.pack_start(gtk.Label(' '),False)

        labelColor = gtk.Label('Arrow color')
        labelColor.set_alignment(0.01, 0.5)
        hBox = gtk.HBox()
        hBox.pack_start(labelColor,False)
        hBox.pack_end(PythonValue(self,'Arrow color'),False)
        hBox.pack_end(ElementValue(self,'Arrow color'),False)
        box.pack_start(hBox, False)
        box.pack_start(self.arrowColor, False)
        box.pack_start(gtk.Label(' '),False)

        if self.arrowStyle.get_active_text() != 'simple':
            labelColor = gtk.Label('Fill color')
            labelColor.set_alignment(0.01, 0.5)
            hBox = gtk.HBox()
            hBox.pack_start(labelColor,False)
            hBox.pack_end(PythonValue(self,'Fill color'),False)
            hBox.pack_end(ElementValue(self,'Fill color'),False)
            box.pack_start(hBox, False)
            box.pack_start(self.fillColor, False)
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
        if attrib == 'Arrow color':
            self.arrowColor.color = value
            if value:
                self.arrowColor.set_label(self.arrowColor.color)
            else:
                self.arrowColor.set_label('')
            self.exposeLine(self.drawArea, None)
        if attrib == 'Fill color':
            self.fillColor.color = value
            if value:
                self.fillColor.set_label(self.fillColor.color)
            else:
                self.fillColor.set_label('')
            self.exposeLine(self.drawArea, None)
            self.drawArea.queue_draw()

    def colorChanged(self, newColor, attrib):
        self.exposeLine(self.drawArea, None)

    def getApp(self):
        app = etree.Element('ConnectionArrow')
        if self.arrowDirection.get_active_text() == 'src -> dest':
            index = '-1'
        else:
            index = '0'
        app.attrib['index'] = index
        app.attrib['style'] = self.styleDict[self.arrowStyle.get_active_text()]
        if self.arrowColor.color:
            app.attrib['color'] = self.arrowColor.getColor()
        if self.fillColor.color:
            app.attrib['fill'] = self.fillColor.getColor()
        return app

    def setIndex(self, index):
        self.arrowDirection.disconnect(self.directionHandler)
        if index == '-1':
            self.arrowDirection.set_active(0)
        if index == '0':
            self.arrowDirection.set_active(1)
        self.directionHandler = self.arrowDirection.connect('changed', self.directionChanged)

    def setArrowStyle(self, style):
        self.arrowStyle.disconnect(self.styleHandler)
        if style == 'simple_arrow':
            self.arrowStyle.set_active(0)
        elif style == 'triangle_arrow':
            self.arrowStyle.set_active(1)
        elif style == 'diamond_arrow':
            self.arrowStyle.set_active(2)
        elif style == 'crosscircle_arrow':
            self.arrowStyle.set_active(3)
        elif style == 'square_arrow':
            self.arrowStyle.set_active(4)
        self.styleHandler = self.arrowStyle.connect('changed', self.styleChanged)

    def setArrowColor(self, color):
        self.arrowColor.setColor(color)

    def setFillColor(self, color):
        self.fillColor.setColor(color)

    @staticmethod
    def validate(element, dataElement):
        color = element.get('color')
        if color:
            if not ValueValidator.validate(color, dataElement):
                return False, 'Unknown element attribute for arrow color: ' + color
        fill = element.get('fill')
        if fill:
            if not ValueValidator.validate(fill, dataElement):
                return False, 'Unknown element attribute for arrow fill: ' + fill
        return True, None