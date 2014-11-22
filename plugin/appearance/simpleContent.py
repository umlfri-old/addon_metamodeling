import gtk

class SimpleContent(gtk.EventBox):
    def __init__(self, parentContainer, manager):
        gtk.EventBox.__init__(self)
        self.parentContainer = parentContainer
        self.manager = manager
        self.label = gtk.Label('Add content')
        self.set_border_width(2)
        self.enterNotifyHandler = self.connect('enter_notify_event', manager.buttonAddEnter)
        self.buttonReleaseHandler = self.connect('button_release_event', manager.addContent)
        self.add(self.label)
        self.content = None
        #self.label.connect('drag_motion', self.motion_cb)
        #self.label.connect('drag_drop', self.drop_cb)
        self.label.drag_dest_set(0,[],0)

    def motion_cb(self, wid, context, x, y, time):
        if self.parentContainer:
            if self.manager.lastHighligted:
                self.manager.lastHighligted.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("black"))
                self.manager.lastHighligted = self.parentContainer
            self.parentContainer.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("red"))
        context.drag_status(gtk.gdk.ACTION_COPY, time)
        return True

    def drop_cb(self, wid, context, x, y, time):
        self.manager.addWidget(self, context.get_source_widget())
        print context.get_source_widget().name
        return True

    def get_Label(self):
        return self.label

    def add_Content(self, container):
        if self.parentContainer:
            self.parentContainer.add_New_Simple_Content()
        self.content = container
        self.add(container)