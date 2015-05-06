import gtk
from simpleContent import SimpleContent

class BaseElement(gtk.EventBox):
    def __init__(self):
        gtk.EventBox.__init__(self)

    def deleteChild(self, child):
        for c in self.box.children():
            if c.content == child:
                self.box.remove(c)
                self.childObjects.remove(c)
        self.add_New_Simple_Content()

    def add_New_Simple_Content(self):
        if len(self.childObjects) == 0:
            sc = SimpleContent(self,self.manager)
            self.box.pack_start(sc)
            self.childObjects.append(sc)
            self.show_all()

    def motion_cb(self, wid, context, x, y, time):
        context.drag_status(gtk.gdk.ACTION_COPY, time)
        return True

    def drop_cb(self, wid, context, x, y, time):
        tempX = None
        source = context.get_source_widget().getParent()
        for child in self.parentContainer.childObjects:
            if child.content == source:
                for x in self.parentContainer.childObjects:
                    if x.content == self:
                        tempX = x
        if tempX:
            newPosition = self.parentContainer.childObjects.index(tempX)
            self.parentContainer.reorder(newPosition, source)
        return True

