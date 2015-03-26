import gtk
from colors2 import colors

class ColorChooserButton(gtk.Button):
    def __init__(self, widget, selectionLabel):
        gtk.Button.__init__(self)
        self.set_label(' ')
        self.widget = widget
        self.selectionLabel = selectionLabel
        self.set_alignment(0.01, 0.5)
        self.connect('clicked', self.chooseTextColor)
        self.color = None

    def chooseTextColor(self, button):
        cdia = gtk.ColorSelectionDialog(self.selectionLabel)
        if self.color:
            if not self.color.startswith('#'):
                try:
                    cdia.colorsel.set_current_color(gtk.gdk.Color(self.color))
                except ValueError:
                    cdia.colorsel.set_current_color(gtk.gdk.Color('#'+self.color))
        response = cdia.run()

        if response == gtk.RESPONSE_OK:
            colorsel = cdia.colorsel
            color = colorsel.get_current_color()
            floatColors = [color.red_float,color.green_float,color.blue_float]
            colorName = "#" + "".join(["%02x" % (col * 255) for col in floatColors])
            string = colors.get(colorName, colorName)
            self.set_label(string)
            if string.startswith('#'):
                self.color = string[1:]
            else:
                self.color = string
            self.widget.colorChanged(color, self.selectionLabel)
        else:
            pass
        cdia.destroy()