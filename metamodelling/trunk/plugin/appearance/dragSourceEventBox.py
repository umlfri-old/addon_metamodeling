import gtk
from baseElement import BaseElement

class DragSourceEventBox(BaseElement):
    def __init__(self, parent):
        BaseElement.__init__(self)
        self.parentWidget = parent

    def getParent(self):
        return self.parentWidget