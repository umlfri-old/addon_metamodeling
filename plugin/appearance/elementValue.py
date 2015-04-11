import gtk
import os

class ElementValue(gtk.EventBox):
    def __init__(self, widget, attrib):
        gtk.EventBox.__init__(self)
        self.widget = widget
        self.attrib = attrib
        icon = gtk.Image()
        icon.set_from_file(os.path.split(os.path.realpath(__file__))[0]+'/buttonElement.png')
        icon.set_tooltip_text('Element attributes')
        self.add(icon)
        self.connect('button-release-event', self.setValue)

    def setValue(self, widget, w):
        label = gtk.Label('   Choose from '+self.widget.manager.selected.object.name+' attributes   ')
        combo = gtk.combo_box_new_text()
        for x in eval(self.widget.manager.selected.object.values['attributes']):
            combo.append_text(('#self.'+x['attName']).replace(' ',''))
        dialog = gtk.Dialog(self.attrib,
                           None,
                           gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                           (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,
                            gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
        dialog.vbox.pack_start(label)
        dialog.vbox.pack_start(combo,False)
        dialog.vbox.pack_start(gtk.Label(' '))
        dialog.vbox.show_all()
        response = dialog.run()
        if response == gtk.RESPONSE_ACCEPT:
            if combo.get_active_text():
                self.widget.setElementValue(self.attrib,combo.get_active_text())
        dialog.destroy()

