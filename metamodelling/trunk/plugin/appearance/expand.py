import gtk

class Expand(gtk.VBox):
    def __init__(self, widget):
        gtk.VBox.__init__(self)
        self.widget = widget
        self.expand = 0

        label = gtk.Label('Expand')
        label.set_alignment(0.01, 0.5)
        self.comboExpand = gtk.combo_box_new_text()
        self.comboExpand.append_text('False')
        self.comboExpand.append_text('True')
        self.comboExpand.set_active(1)
        self.comboExpand.connect('changed', self.expandChanged)
        self.pack_start(label,False)
        self.pack_start(self.comboExpand, False)

    def expandChanged(self, widget):
        self.expand = self.comboExpand.get_active()

    def isTrue(self):
        if self.comboExpand.get_active() == 1:
            return True
        else:
            return False

    def setExpand(self, bool):
        if bool == True:
            self.comboExpand.set_active(1)
            self.expand = 1
        else:
            self.comboExpand.set_active(0)
            self.expand = 0
