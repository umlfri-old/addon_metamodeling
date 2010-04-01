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
        ('object', gtk.TARGET_SAME_WIDGET, 0),
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
#        item = AppearanceFactory.CreateElement('Ellipse')
#        self.treestore.set(quex,0,item.Identity(),1,item)
#        quex1 = self.treestore.append(parent)
#        item1 = AppearanceFactory.CreateElement('Rectangle')
#        self.treestore.set(quex1,0,item1.Identity(),1,item1)
#        
#        quex2 = self.treestore.append(quex1)
#        item2 = AppearanceFactory.CreateElement('Rectangle')
#        self.treestore.set(quex2,0,item2.Identity(),1,item2)

        self.__ConstructLeftTW()
        
        self.__ConstructCanvas()
         
        self.__ConstructRightTW()
        
        self.window.show_all()
        gtk.main()
        
    def __ConstructBasicLayout(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title("Metamodel Editor")
        self.window.set_size_request(800,600)
            
        self.hbox = gtk.HBox() 
        self.window.add(self.hbox)    
        
    def __ConstructLeftTW(self):
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

        self.treeview.connect('cursor-changed', self.on_cursor_changed)

        self.treeview.connect("button_press_event", self.on_button_press_event)

        self.tvcolumn = gtk.TreeViewColumn('Structure of layout')
        self.treeview.append_column(self.tvcolumn)
        self.cell = gtk.CellRendererText()
        self.tvcolumn.pack_start(self.cell, True)
        self.tvcolumn.add_attribute(self.cell, "text", 0)
               
        self.hbox.pack_start(self.treeview)     
        
    def __ConstructCanvas(self):
        #canvas for previews
        self.canvas = gtk.DrawingArea()
        self.canvas.set_size_request(400,600)
       

        self.hbox.pack_start(self.canvas)
        
    def PaintSelf(self):
        print 'ca'
        print self.canvas
        canvasarea = self.canvas.window
        
        self.gc = canvasarea.new_gc(foreground=None, background=None, font=None, 
                     function=-1, fill=-1, tile=None,
                     stipple=None, clip_mask=None, subwindow_mode=-1,
                     ts_x_origin=-1, ts_y_origin=-1, clip_x_origin=-1,
                     clip_y_origin=-1, graphics_exposures=-1,
                     line_width=-1, line_style=-1, cap_style=-1,
                     join_style=-1)
        
        
#        canvasarea.draw_line(self.gc, 0, 0, 100, 100)
#        canvasarea.draw_rectangle(self.gc, True, 200-50, 300-80, 200+50, 300+80)
        rect = CRectangle()
        rect.Paint(self.gc)
        
    def __ConstructRightTW(self):
        self.twProperties = gtk.TreeView()
        self.hbox.pack_end(self.twProperties)    
        
    def on_button_press_event(self, widget, event):
        if (event is None): return       
        if event.button == 3 and event.type == gtk.gdk.BUTTON_PRESS:
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
        #if (ret is not None):
        self.SetPropertiesModel(ret)  
        
        self.PaintSelf()  
        
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
        self.tmpModel.clear()
        if (source is not None): 
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
    
    def drag_data_get_data(self, treeview, context, selection, target_id,
                           etime):
        treeselection = treeview.get_selection()
        model, iter = treeselection.get_selected()
        data = model.get_value(iter, 0)
        selection.set(selection.target,8,data)
    
    def drag_data_received_data(self, widget, context, x, y, selection, info, etime):
        if widget.get_dest_row_at_pos(x, y) is not None:
            path, pos = widget.get_dest_row_at_pos(x, y)
            model, iter_to_copy = widget.get_selection().get_selected()
            target_iter = model.get_iter(path)
                       
            if self.CheckSanity(model, iter_to_copy, target_iter):
                self.IterCopy(widget, model, iter_to_copy, target_iter, pos)
                context.finish(True, True, etime)
            else:
                context.finish(False, False, etime) 
                
    def CheckSanity(self, model, iter_to_copy, target_iter):
        path_of_iter_to_copy = model.get_path(iter_to_copy)
        path_of_target_iter = model.get_path(target_iter)
        if path_of_target_iter[0:len(path_of_iter_to_copy)] == path_of_iter_to_copy:
            return False
        elif len(path_of_target_iter) < 2:
            return False
        else:
            return True
    
    def IterCopy(self, treeview, model, iter_to_copy, target_iter, pos):
        new_pos_str=(model.get_string_from_iter(target_iter)).split(':')
        old_pos_str=(model.get_string_from_iter(iter_to_copy)).split(':')
        new_el_pos=int(new_pos_str[len(new_pos_str)-1])
        old_el_pos=int(old_pos_str[len(old_pos_str)-1])
        
        node_to_copy = treeview.get_model().get(iter_to_copy,1)[0]
        
        target_node = treeview.get_model().get(target_iter,1)[0]
        
        if (pos == gtk.TREE_VIEW_DROP_INTO_OR_BEFORE) or (pos == gtk.TREE_VIEW_DROP_INTO_OR_AFTER):
            new_iter = model.append(target_iter)
        
        elif pos == gtk.TREE_VIEW_DROP_BEFORE:
            new_iter = model.insert_before(None, target_iter)
        
        elif pos == gtk.TREE_VIEW_DROP_AFTER:
            new_iter = model.insert_after(None, target_iter)
                    
        for i in range(2):
            model.set_value(new_iter, i, model.get_value(iter_to_copy, i))
              
        if model.iter_has_child(iter_to_copy):
            for i in range(0, model.iter_n_children(iter_to_copy)):
                next_iter_to_copy = model.iter_nth_child(iter_to_copy, i)
                self.IterCopy(treeview, model, next_iter_to_copy, new_iter, gtk.TREE_VIEW_DROP_INTO_OR_BEFORE)
     
        model.remove(iter_to_copy)
        
if __name__ == '__main__':
    a=EditWindow('','')