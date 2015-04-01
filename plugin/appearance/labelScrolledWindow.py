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

    @staticmethod
    def validate(element):
        if element.getchildren() == []:
            return False, 'Missing content for label. Add some or delete label.'
        return True, None

    def setPosition(self, position):
        if '+' in position:
            position, shifting = position.split('+')
            self.shifting.set_value(int(shifting))
        elif '-' in position:
            position, shifting = position.split('-')
            self.shifting.set_value(int(shifting)*-1)
        if position == 'center':
            self.position.set_active(0)
        elif position == 'destination':
            self.position.set_active(1)
        elif position == 'source':
            self.position.set_active(2)

    def getPosition(self):
        position = self.position.get_active_text()
        shifting = int(self.shifting.get_value())
        if shifting > 0:
            return position + '+' + str(shifting)
        elif shifting < 0:
            return position + str(shifting)
        else:
            return position
