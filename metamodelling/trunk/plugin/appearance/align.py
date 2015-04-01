import gtk


class Align(gtk.VBox):
    def __init__(self, widget):
        gtk.VBox.__init__(self)
        self.widget = widget

        self.xAlign = 3     # 0=left, 1=center, 2=right, 3=none
        self.yAlign = 3     # 0=top, 1=center, 2=bottom, 3=none
        self.xValue = 0.0
        self.yValue = 0.5

        labelX = gtk.Label('X align')
        labelX.set_alignment(0.01, 0.5)
        self.comboXalign = gtk.combo_box_new_text()
        for value in ['left','center','right','none']:
            self.comboXalign.append_text(value)
        self.comboXalign.set_active(self.xAlign)
        self.comboXalign.connect('changed', self.xChanged)

        labelY = gtk.Label('Y align')
        labelY.set_alignment(0.01, 0.5)
        self.comboYalign = gtk.combo_box_new_text()
        for value in ['top','center','bottom','none']:
            self.comboYalign.append_text(value)
        self.comboYalign.set_active(self.yAlign)
        self.comboYalign.connect('changed', self.yChanged)

        self.pack_start(labelX,False)
        self.pack_start(self.comboXalign,False)
        self.pack_start(gtk.Label(' '),False)
        self.pack_start(labelY,False)
        self.pack_start(self.comboYalign,False)

    def xChanged(self, widget):
        self.xAlign = self.comboXalign.get_active()
        if self.xAlign == 0:
            self.xValue = 0.0
        elif self.xAlign == 1:
            self.xValue = 0.5
        elif self.xAlign == 2:
            self.xValue = 1.0
        elif self.xAlign ==3:
            self.xValue = 0.0
        self.widget.xChanged()

    def yChanged(self, widget):
        self.yAlign = self.comboYalign.get_active()
        if self.yAlign == 0:
            self.yValue = 0.0
        elif self.yAlign == 1:
            self.yValue = 0.5
        elif self.yAlign == 2:
            self.yValue = 1.0
        elif self.yAlign == 3:
            self.yValue = 0.5
        self.widget.yChanged()

    def isAlignSet(self):
        if self.xAlign != 3 or self.yAlign != 3:
            return True
        else:
            return False

    def getXMLFormat(self):
        string = 'align="'
        if self.xAlign == 0:
            string += 'left '
        elif self.xAlign == 1:
            string += 'center '
        elif self.xAlign == 2:
            string += 'right '
        if self.yAlign == 0:
            string += 'top'
        elif self.yAlign == 1:
            string += 'middle'
        elif self.yAlign == 2:
            string += 'bottom'
        string += '" '
        return  string

    def setAlign(self, align):
        align = align.split()
        for value in align:
            if value == 'left':
                self.xAlign == 0
                self.comboXalign.set_active(0)
            elif value == 'center':
                self.xAlign == 1
                self.comboXalign.set_active(1)
            elif value == 'right':
                self.xAlign == 2
                self.comboXalign.set_active(2)
            elif value == 'top':
                self.yAlign = 0
                self.comboYalign.set_active(0)
            elif value == 'middle':
                self.yAlign = 1
                self.comboYalign.set_active(1)
            elif value == 'bottom':
                self.yAlign = 2
                self.comboYalign.set_active(2)






