import gtk
from colorChooserButton import ColorChooserButton

class RectangleCorner(gtk.VBox):
    def __init__(self, widget, cornerName):
        gtk.VBox.__init__(self)
        self.button = gtk.Button()
        self.button.set_label(cornerName)
        self.button.set_sensitive(False)
        self.checkBox = gtk.CheckButton()
        self.checkBox.connect('toggled', self.checked)
        hBox = gtk.HBox()
        hBox.pack_start(self.checkBox,False)
        hBox.pack_start(self.button)
        self.pack_start(hBox)
        self.color = ColorChooserButton(self, cornerName)
        self.combo = gtk.combo_box_new_text()
        self.combo.append_text('Note corner')
        self.combo.append_text('Rounded corner')
        self.combo.set_active(0)
        self.combo.connect('changed', self.cornerTypeChanged)
        self.sizeSpin = gtk.SpinButton(gtk.Adjustment(0,0,10000,1,10,0),0.0,0)
        self.sizeSpin.set_editable(False)
        self.cornerName = cornerName
        self.widget = widget
        self.button.connect('clicked', self.showProperties)

        self.dialog = gtk.Dialog(self.cornerName,
                           None,
                           gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                           (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
        self.dialog.set_size_request(250,220)

        label = gtk.Label('Corner type')
        label.set_alignment(0.01, 0.5)
        self.dialog.vbox.pack_start(label,False)
        self.dialog.vbox.pack_start(self.combo,False)
        self.dialog.vbox.pack_start(gtk.Label(' '),False)

        label = gtk.Label('Corner size')
        label.set_alignment(0.01, 0.5)
        self.dialog.vbox.pack_start(label,False)
        self.dialog.vbox.pack_start(self.sizeSpin,False)
        self.dialog.vbox.pack_start(gtk.Label(' '),False)

        label = gtk.Label('Corner color')
        label.set_alignment(0.01, 0.5)
        self.dialog.vbox.pack_start(label,False)
        self.dialog.vbox.pack_start(self.color,False)
        self.dialog.vbox.pack_start(gtk.Label(' '),False)

        self.detailsVBox = gtk.VBox()
        self.pack_start(self.detailsVBox)

    def showProperties(self, w):
        self.dialog.vbox.show_all()
        self.dialog.run()
        self.dialog.hide()
        self.showDetails()

    def colorChanged(self, color, selectionLabel):
        pass

    def checked(self, w):
        if self.checkBox.get_active():
            self.button.set_sensitive(True)
            self.showDetails()
            if self.cornerName == 'Left top corner':
                self.widget.leftSide.checkBox.set_active(False)
                self.widget.topSide.checkBox.set_active(False)
            elif self.cornerName == 'Right top corner':
                self.widget.topSide.checkBox.set_active(False)
                self.widget.rightSide.checkBox.set_active(False)
            elif self.cornerName == 'Left bottom corner':
                self.widget.botSide.checkBox.set_active(False)
                self.widget.leftSide.checkBox.set_active(False)
            elif self.cornerName == 'Right bottom corner':
                self.widget.rightSide.checkBox.set_active(False)
                self.widget.botSide.checkBox.set_active(False)
        else:
            self.button.set_sensitive(False)
            self.hideDetails()

    def cornerTypeChanged(self, w):
        if self.combo.get_active() == 0:
            self.color.set_sensitive(True)
        else:
            self.color.set_sensitive(False)

    def showDetails(self):
        for w in self.detailsVBox.children():
            self.detailsVBox.remove(w)
        label = gtk.Label('         Type: ' + self.combo.get_active_text())
        label.set_alignment(0.01, 0.5)
        self.detailsVBox.pack_start(label)
        label = gtk.Label('         Size: ' + str(int(self.sizeSpin.get_value())))
        label.set_alignment(0.01, 0.5)
        self.detailsVBox.pack_start(label)
        color = ''
        if self.combo.get_active() == 0:
            if self.color.color:
                color = self.color.color
        label = gtk.Label('         Color: ' + color)
        label.set_alignment(0.01, 0.5)
        self.detailsVBox.pack_start(label)
        self.show_all()

    def hideDetails(self):
        self.detailsVBox.hide()

    def getXMLFormat(self):
        string = str(int(self.sizeSpin.get_value())) +  ' '
        if self.combo.get_active_text() == 'Note corner':
            string += 'note_corner'
        if self.combo.get_active_text() == 'Rounded corner':
            string += 'rounded_corner'
        if self.color.color:
            color = self.color.getColor()
            if color.startswith('##'):
                color = color [2:]
            string += ' ' + color
        return string

    def setCorner(self, string):
        if len(string.split()) > 2:
            size, type, color = string.split()
        else:
            size, type = string.split()
            color = None
        self.sizeSpin.set_value(int(size))
        if type == 'note_corner':
            self.combo.set_active(0)
        elif type == 'rounded_corner':
            self.combo.set_active(1)
        if color:
            self.color.setColor(color)
        self.checkBox.set_active(True)