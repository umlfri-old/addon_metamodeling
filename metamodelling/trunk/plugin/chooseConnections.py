import constants
import gtk
import os

class ChooseConnections:
    def __init__(self, interface):
        self.i = interface
        self.dic = { "on_buttonCancel_clicked" : self.close, "on_buttonSave_clicked" : self.saveConnections }
        gladefile = os.path.split(os.path.realpath(__file__))[0] + "/choose_connections.glade"
        self.closed = True
        self.wTree = gtk.glade.XML(gladefile) 
        self.window = self.wTree.get_widget("dialogChooseConnections")
        self.wTree.signal_autoconnect(self.dic)
        self.window.connect("destroy", self.close)
        self.window.connect("delete_event", self.close2)
        self.vBox = self.wTree.get_widget("vBox")
        self.selected = None
        
    def show(self):
        if self.closed:                    
            selected = []
            for item in self.i.current_diagram.selected:
                selected.append(item)
            if len(selected) != 1:
                md = gtk.MessageDialog(None, gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_ERROR, gtk.BUTTONS_CLOSE, 'Select only one element.')
                md.run()
                md.destroy()
                return
            self.selected = selected[0]
            if self.selected.object.type.domain.name != constants.CONNECTIONS_DOMAIN_NAME:
                md = gtk.MessageDialog(None, gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_ERROR, gtk.BUTTONS_CLOSE, 'Select Connections element in Diagram editor.')
                md.run()
                md.destroy()
                return    
            for child in self.vBox.get_children():
                if child.get_name() == 'GtkCheckButton':
                    self.vBox.remove(child)
            conns = []
            for dia in self.i.project.root.diagrams:
                for conn in dia.connections:
                    if conn.object.type.domain.name == constants.CONNECTION_DOMAIN_NAME:
                        conns.append(conn)
            if len(conns) == 0:
                md = gtk.MessageDialog(None, gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_ERROR, gtk.BUTTONS_CLOSE, 'First create some connections in Elements editor.')
                md.run()
                md.destroy()
                return
            checked = []
            for item in self.selected.object.all_values:
                if 'attributes' in item[0]:
                    checked.append(item[1])
            for conn in conns:
                check = gtk.CheckButton(conn.object.values['name'])
                if conn.object.values['name'] in checked:
                    check.set_active(True)
                else:
                    check.set_active(False)
                self.vBox.pack_start(check, False, True, 0)
            self.window.show_all()
            self.closed = False
        else:
            self.close(self.window)
            self.show()
        
    def saveConnections(self, widget):
        conns = []
        for child in self.vBox.get_children():
                if child.get_name() == 'GtkCheckButton':
                    if child.get_active():
                        conns.append({'value': child.get_label()})
        self.selected.object.values['attributes'] = conns
        self.close(widget)
    
    def close(self, widget):
        self.closed = True
        self.window.hide()
        return gtk.TRUE
        
    def close2(self, widget, widget2):
        self.closed = True
        self.window.hide()
        return gtk.TRUE
        
