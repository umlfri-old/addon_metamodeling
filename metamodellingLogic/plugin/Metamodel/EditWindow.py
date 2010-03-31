'''
Created on 28.3.2010

@author: Michal Kovacik
'''
import os
from __init__ import *
import pygtk
from symbol import for_stmt
pygtk.require('2.0')

try:
    import gtk
    import gtk.glade
except:
    sys.exit(1)    


class ContextMenu(gtk.Menu):
    def __init__(self, t):
        gtk.Menu.__init__(self)
        self.t = t
        
        self.addmenuitem = gtk.MenuItem("Add")
        
        submenuadd = gtk.Menu()
        for mit in self.__GetSubMenuItems():
            menu_items = gtk.MenuItem(mit)         
            menu_items.connect("activate", self.add, mit)
            menu_items.show()
            submenuadd.append(menu_items)      
        
        self.addmenuitem.set_submenu(submenuadd)
        self.show()
        
        self.addmenuitem.show()
        self.append(self.addmenuitem)
        
        self.removeitem = gtk.MenuItem("Remove")
        self.removeitem.connect("activate", self.menuitem_remove, mit)
        self.removeitem.show()
        self.append(self.removeitem)

    def add(self,widget,string):
        parent = self.t.treestore.append(self.t.treeview.get_selection().get_selected()[1])
        item = AppearanceFactory.CreateElement(string)
        self.t.treestore.set(parent,0,item.Identity(),1,item)
        
    def __GetSubMenuItems(self):
        return ['Align','Condition','Default','Diamond','Ellipse','HBox','Icon','Line','Loop','Padding','Proportional','Rectangle','Shadow','Sizer','Svg','Switch','TextBox','VBox']
    
    def menuitem_remove(self, widget,string):
        item = self.t.treeview.get_selection().get_selected()[1]
        self.t.treestore.remove(item)


class EditWindow(object):
    def __init__(self,selected,project):
        self.TARGETS = [
        ('MY_TREE_MODEL_ROW', gtk.TARGET_SAME_WIDGET, 0),
        ('text/plain', 0, 1),
        ('TEXT', 0, 2),
        ('STRING', 0, 3),
        ]
        self.__ConstructBasicLayout()
        
        self.treestore = gtk.TreeStore(str,object)
        self.tmpModel = gtk.ListStore(str,str)
        
        parent = self.treestore.append(None)
        self.treestore.set(parent,0,"Appearance",1,None)
        quex = self.treestore.append(parent)
        item = AppearanceFactory.CreateElement('Ellipse')
        self.treestore.set(quex,0,item.Identity(),1,item)
        quex1 = self.treestore.append(parent)
        item1 = AppearanceFactory.CreateElement('Rectangle')
        self.treestore.set(quex1,0,item1.Identity(),1,item1)
        
        quex2 = self.treestore.append(quex1)
        item2 = AppearanceFactory.CreateElement('Rectangle')
        self.treestore.set(quex2,0,item2.Identity(),1,item2)


        self.treeview = gtk.TreeView(self.treestore)
        self.treeview.get_selection().set_mode(gtk.SELECTION_SINGLE)
        
        
        self.treeview.enable_model_drag_source( gtk.gdk.BUTTON1_MASK,
                                                self.TARGETS,
                                                gtk.gdk.ACTION_DEFAULT|
                                                gtk.gdk.ACTION_MOVE|
                                                gtk.gdk.ACTION_COPY)
        self.treeview.enable_model_drag_dest(self.TARGETS,
                                             gtk.gdk.ACTION_DEFAULT)

        self.treeview.connect("drag_data_get", self.drag_data_get_data)
        self.treeview.connect("drag_data_received",
                              self.drag_data_received_data)
        #self.treeview.connect("selection")
        self.treeview.connect('cursor-changed', self.on_cursor_changed)
        #self.treeview.connect('cursor-changed', self.on_button_press_event, self.treeview.eventButton)
        self.treeview.connect("button_press_event", self.on_button_press_event)
        #self.treeview.connect("button_press_event", self.test)

        self.tvcolumn = gtk.TreeViewColumn('Structure of layout')
        self.treeview.append_column(self.tvcolumn)
        self.cell = gtk.CellRendererText()
        self.tvcolumn.pack_start(self.cell, True)
        self.tvcolumn.add_attribute(self.cell, "text", 0)
               
        self.hbox.pack_start(self.treeview)
        
        self.canvas = gtk.DrawingArea()
        self.hbox.pack_start(self.canvas)
        
        self.twProperties = gtk.TreeView()
        self.hbox.pack_end(self.twProperties)
        
        
        self.window.show_all()
        gtk.main()
        
    def __ConstructBasicLayout(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title("Metamodel Editor")
        self.window.set_size_request(600,480)
            
        self.hbox = gtk.HBox() 
        self.window.add(self.hbox)     
        
    def on_button_press_event(self, widget, event):
        if (event is None): return
        """
        if event.button == 1 and event.type == gtk.gdk.BUTTON_PRESS:
            ret = self.GetSelectedItem(widget)
            if (ret is not None):
                self.SetPropertiesModel(ret)
        """        
        if event.button == 3 and event.type == gtk.gdk.BUTTON_PRESS:
            print self.GetSelectedItem(widget)
            c = ContextMenu(self)
            c.popup(None, None, None, event.button, event.get_time())
            
    def test(self,widget,event):
        print event.button
        self.eventButton = event.button
        widget.eventButton = event.button
        print 'eB '+str(self.eventButton)
            
    def on_cursor_changed(self, treeview):
        print "Treeview Cursor changed"

        ret = self.GetSelectedItem(treeview)
        if (ret is not None):
            self.SetPropertiesModel(ret)
        
        s = treeview.get_selection()
        (ls, iter) = s.get_selected()
        if iter is None:
            print "nothing selected"
        else:
            data0 = ls.get_value(iter, 0)
            data1 = ls.get_value(iter, 1)
            print "Selected:", data0, data1

    
    def GetSelectedItem(self, widget):
        if (widget is not None):
            test = gtk.TreeView()
            entry1, entry2 = widget.get_selection().get_selected()
            entry = entry1.get_value(entry2, 1)
            print entry
            return entry
     
    def SetPropertiesModel(self, source):
        if (source is not None):
            self.tmpModel.clear()
            attr = source.GetAttributes().items()
            for it in attr:
                print it
                key, val = it
                print key,val
                newitem = self.tmpModel.append(None)
                self.tmpModel.set(newitem,0,key,1,val)
        
        self.twProperties.set_model(self.tmpModel)

        if (self.twProperties.get_columns() is not None):
            for i in self.twProperties.get_columns():
                self.twProperties.remove_column(i)
        
        self.tvcolumnK = gtk.TreeViewColumn('Keys of '+source.Identity())
        self.twProperties.append_column(self.tvcolumnK)
        cell = gtk.CellRendererText()
        self.tvcolumnK.pack_start(cell, True)
        self.tvcolumnK.add_attribute(cell, "text", 0)
        
        self.tvcolumnV = gtk.TreeViewColumn('Values of '+source.Identity())
        self.twProperties.append_column(self.tvcolumnV)
        cell1 = gtk.CellRendererText()
        cell1.set_property('editable',True)
        cell1.connect('edited',self.value_edited,self.twProperties.get_selection().get_selected())
        self.tvcolumnV.pack_start(cell1, True)
        self.tvcolumnV.add_attribute(cell1, "text", 1)
    
    def value_edited(self,cell, path, new_text, user_data): 
        print user_data 
        liststore, column = user_data
        column = 1
        liststore[path][column] = new_text
        
        #teraz setnem hodnotu aj do backend objektu
        self.GetSelectedItem(self.treeview).GetAttributes()[liststore[path][0]]=new_text
        return
    
    def drag_data_get_data(self, treeview, context, selection, target_id,
                           etime):
        treeselection = treeview.get_selection()
        model, iter = treeselection.get_selected()
        data = model.get_value(iter, 0)
        selection.set(selection.target, 8, data)

    def drag_data_received_data(self, treeview, context, x, y, selection,
                                info, etime):
        model = treeview.get_model()
        data = selection.data
        print "Data"
        print data
        drop_info = treeview.get_dest_row_at_pos(x, y)
        if drop_info:
            path, position = drop_info
            iter = model.get_iter(path)
            print "Iter"
            print iter
            if (position == gtk.TREE_VIEW_DROP_BEFORE
                or position == gtk.TREE_VIEW_DROP_INTO_OR_BEFORE):
                model.insert_before(iter, [data])
            else:
                model.insert_after(iter, [data])
        else:
            model.append([data])
        if context.action == gtk.gdk.ACTION_MOVE:
            context.finish(True, True, etime)
        return
     
        
if __name__ == '__main__':
    a=EditWindow('','')