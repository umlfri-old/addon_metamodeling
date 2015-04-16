import gtk

class ParentButton(gtk.Button):
    def __init__(self, widget):
        gtk.Button.__init__(self)
        self.widget = widget
        self.set_label('Add parent')
        self.connect('clicked', self.clicked)

    def clicked(self, widget):
        label = gtk.Label('   Choose from containers')
        combo = gtk.combo_box_new_text()
        for text in self.widget.manager.getVisibleContainers():
            combo.append_text(text)
        combo.set_active(0)
        dialog = gtk.Dialog('Add parent',
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
            self.widget.manager.addParent(self.widget, combo.get_active_text())
        dialog.destroy()