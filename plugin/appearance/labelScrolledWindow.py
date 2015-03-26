import gtk

class LabelScrolledWindow(gtk.ScrolledWindow):
    def __init__(self):
        gtk.ScrolledWindow.__init__(self)
        self.position = gtk.combo_box_new_text()
        self.position.append_text('center')
        self.position.append_text('destination')
        self.position.append_text('source')
        self.shifting = gtk.SpinButton(gtk.Adjustment(0,-10000,10000,1,10,0),0.0,0)
        self.position.set_active(0)
