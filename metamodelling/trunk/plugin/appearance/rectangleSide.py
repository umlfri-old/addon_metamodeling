import gtk

class RectangleSide(gtk.VBox):
    def __init__(self, widget, sideName):
        gtk.VBox.__init__(self)
        self.button = gtk.Button()
        self.button.set_label(sideName)
        self.button.set_sensitive(False)
        self.checkBox = gtk.CheckButton()
        self.checkBox.connect("toggled", self.checked)
        hBox = gtk.HBox()
        hBox.pack_start(self.checkBox,False)
        hBox.pack_start(self.button)
        self.pack_start(hBox)
        self.combo = gtk.combo_box_new_text()
        self.combo.append_text('Rounded side')
        self.combo.set_active(0)
        self.sizeSpin = gtk.SpinButton(gtk.Adjustment(0,0,10000,1,10,0),0.0,0)
        self.sizeSpin.set_editable(False)
        self.sideName = sideName
        self.widget = widget
        self.button.connect('clicked', self.showProperties)

        self.dialog = gtk.Dialog(self.sideName,
                           None,
                           gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                           (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
        self.dialog.set_size_request(250,160)

        label = gtk.Label('Side type')
        label.set_alignment(0.01, 0.5)
        self.dialog.vbox.pack_start(label,False)
        self.dialog.vbox.pack_start(self.combo,False)
        self.dialog.vbox.pack_start(gtk.Label(' '),False)

        label = gtk.Label('Size')
        label.set_alignment(0.01, 0.5)
        self.dialog.vbox.pack_start(label,False)
        self.dialog.vbox.pack_start(self.sizeSpin,False)
        self.dialog.vbox.pack_start(gtk.Label(' '),False)

        self.detailsVBox = gtk.VBox()
        self.pack_start(self.detailsVBox)

    def showProperties(self, w):
        self.dialog.vbox.show_all()
        self.dialog.run()
        self.dialog.hide()
        self.showDetails()

    def checked(self, w):
        if self.checkBox.get_active():
            self.button.set_sensitive(True)
            self.showDetails()
            if self.sideName == 'Left side':
                self.widget.leftTopCorner.checkBox.set_active(False)
                self.widget.leftBotCorner.checkBox.set_active(False)
            elif self.sideName == 'Top side':
                self.widget.leftTopCorner.checkBox.set_active(False)
                self.widget.rightTopCorner.checkBox.set_active(False)
            elif self.sideName == 'Right side':
                self.widget.rightTopCorner.checkBox.set_active(False)
                self.widget.rightBotCorner.checkBox.set_active(False)
            elif self.sideName == 'Bottom side':
                self.widget.leftBotCorner.checkBox.set_active(False)
                self.widget.rightBotCorner.checkBox.set_active(False)
        else:
            self.button.set_sensitive(False)
            self.hideDetails()

    def showDetails(self):
        for w in self.detailsVBox.children():
            self.detailsVBox.remove(w)
        label = gtk.Label('         Type: ' + self.combo.get_active_text())
        label.set_alignment(0.01, 0.5)
        self.detailsVBox.pack_start(label)
        label = gtk.Label('         Size: ' + str(int(self.sizeSpin.get_value())))
        label.set_alignment(0.01, 0.5)
        self.detailsVBox.pack_start(label)
        self.show_all()

    def hideDetails(self):
        self.detailsVBox.hide()

    def getXMLFormat(self):
        return str(int(self.sizeSpin.get_value())) + ' ' + 'rounded_side'

    def setSide(self, string):
        size, type = string.split()
        self.sizeSpin.set_value(int(size))
        if type == 'rounded_side':
            self.combo.set_active(0)
        self.checkBox.set_active(True)

