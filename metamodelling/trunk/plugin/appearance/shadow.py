import gtk
from lxml import etree
from colors2 import colors
from pythonValue import PythonValue
from elementValue import ElementValue
from colorChooserButton import ColorChooserButton
from valueValidator import ValueValidator

class Shadow(gtk.VBox):
    def __init__(self, widget):
        gtk.VBox.__init__(self)
        self.widget = widget
        self.manager = widget.manager
        self.padding = 0

        labelPad = gtk.Label('Shadow padding')
        labelPad.set_alignment(0.01, 0.5)
        self.spin = gtk.SpinButton(gtk.Adjustment(self.padding,0,10000,1,10,0),0.0,0)
        self.spin.set_value(self.padding)
        self.spin.set_editable(False)
        self.spin.connect('value-changed', self.paddingChanged)

        labelColor = gtk.Label('Shadow color')
        labelColor.set_alignment(0.01, 0.5)
        hBox = gtk.HBox()
        hBox.pack_start(labelColor,False)
        hBox.pack_end(PythonValue(self,'Shadow color'),False)
        hBox.pack_end(ElementValue(self,'Shadow color'),False)

        self.buttonColor = ColorChooserButton(self, 'Select shadow color')

        self.pack_start(labelPad,False)
        self.pack_start(self.spin,False)
        self.pack_start(gtk.Label(' '),False)
        self.pack_start(hBox,False)
        self.pack_start(self.buttonColor,False)

    def paddingChanged(self, widget):
        self.padding = self.spin.get_value()

    def setElementValue(self, attrib, value):
        self.buttonColor.color = value
        if value:
            self.buttonColor.set_label(value)
        else:
            self.buttonColor.set_label('')

    def colorChanged(self, newColor, attrib):
        pass

    def getXMLFormat(self):
        shadow = etree.Element('Shadow')
        shadow.attrib['padding'] = str(int(self.padding))
        if self.buttonColor.color == None:
            color = ''
        else:
            color = self.buttonColor.getColor()
        shadow.attrib['color'] = color
        return shadow

    def setShadow(self, element):
        padding = element.get('padding')
        if padding:
            self.spin.set_value(int(padding))
        color = element.get('color')
        if color:
            self.buttonColor.setColor(color)

    @staticmethod
    def validate(element, dataElement):
        padding = int(element.get('padding'))
        color = element.get('color')
        if color:
            if not ValueValidator.validate(color, dataElement):
                return False, 'Unknown element attribute for shadow color: ' + color
        if padding > 0 and color == '':
            child = None
            for c in element:
                child = c
            return False, 'Missing shadow color in ' + child.tag + '.'
        return True, None