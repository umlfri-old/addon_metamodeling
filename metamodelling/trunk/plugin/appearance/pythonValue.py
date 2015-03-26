import gtk
import os

class PythonValue(gtk.EventBox):
    def __init__(self, widget, attrib):
        gtk.EventBox.__init__(self)
        self.widget = widget
        self.attrib = attrib
        icon = gtk.Image()
        icon.set_from_file(os.path.split(os.path.realpath(__file__))[0]+'/buttonPython.png')
        icon.set_tooltip_text('Python expression')
        self.add(icon)
        self.connect('button-release-event', self.setValue)

    def setValue(self, widget, w):
        label = gtk.Label('   Python expression   ')
        entry = gtk.Entry()
        dialog = gtk.Dialog(self.attrib,
                           None,
                           gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                           (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,
                            gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
        dialog.vbox.pack_start(label)
        hbox = gtk.HBox()
        hbox.pack_start(gtk.Label('#'))
        hbox.pack_start(entry,False)
        dialog.vbox.pack_start(hbox)
        dialog.vbox.pack_start(gtk.Label(' '))
        dialog.vbox.show_all()
        response = dialog.run()
        if response == gtk.RESPONSE_ACCEPT:
            #if entry.get_text():
            if entry.get_text() == '':
                self.widget.setElementValue(self.attrib, False)
            else:
                self.widget.setElementValue(self.attrib,'#'+entry.get_text())
        dialog.destroy()


