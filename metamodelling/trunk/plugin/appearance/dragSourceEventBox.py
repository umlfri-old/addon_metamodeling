import gtk

class DragSourceEventBox(gtk.EventBox):
    def __init__(self, parent):
        gtk.EventBox.__init__(self)
        self.parentWidget = parent

    def getParent(self):
        return self.parentWidget