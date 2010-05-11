'''
Created on 28.3.2010

@author: Michal Kovacik
'''
import os
from __init__ import *

from Util.DomainType import DomainType
from Util.ElementType import ElementType
from Util.ElementObject import ElementObject
from Util.ConnectionObject import ConnectionObject

from const import ELEMENT_HINTS,CONNECTION_HINTS

from AppearanceGenerator import AppearanceGenerator
from Util.Element import Element
from Util.Connection import Connection
from Util.Cairo.CairoCanvas import CairoCanvas
import pygtk
from symbol import for_stmt
pygtk.require('2.0')

VISUAL_IDENTITY = "visual_identity"

try:
    import gtk
    import gtk.glade
except:
    sys.exit(1)    


class ContextMenu(gtk.Menu):
    '''
    main contextmenu. used when generating Objects
    for Relationship modelling use ContextMenuLine instead
    '''
    def __init__(self, t):
        gtk.Menu.__init__(self)
        self.t = t
        
        self.addmenuitem = gtk.MenuItem("Add")
        
        submenuadd = gtk.Menu()
        
        if (self.t.treeview.get_selection().get_selected()[1]==None):
            selection = self.__GetSubMenuItems()
        elif (self.t.treeview.get_model().get_value(self.t.treeview.get_selection().get_selected()[1],0)=="Svg"):
            selection = self.__GetSvgItems()   
        elif (self.t.treeview.get_model().get_value(self.t.treeview.get_selection().get_selected()[1],0)=="g"):
            selection = self.__GetSvgItems()  
        elif (self.t.treeview.get_model().get_value(self.t.treeview.get_selection().get_selected()[1],0)=="path"):
            selection = None  
        else:  selection = self.__GetSubMenuItems()         
        
        if selection is not None:    
            for mit in selection:
                menu_items = gtk.MenuItem(mit)         
                menu_items.connect("activate", self.add, mit)
                menu_items.show()
                submenuadd.append(menu_items)      
        
            self.addmenuitem.set_submenu(submenuadd)
        
            self.addmenuitem.show()
            self.append(self.addmenuitem)
        
        self.removeitem = gtk.MenuItem("Remove")
        self.removeitem.connect("activate", self.menuitem_remove, 'Remove')
        self.removeitem.show()
        self.append(self.removeitem)
        self.show_all()

    def add(self,widget,string):
        '''
        add action is fired when one item from context menu is selected
        '''
        parent = self.t.treestore.append(self.t.treeview.get_selection().get_selected()[1])
        item = AppearanceFactory.CreateElement(string)
        self.t.treestore.set(parent,0,item.Identity(),1,item)
        
    def __GetSubMenuItems(self):
        '''
        list of items to construct submenu
        '''
        return ['Align','Condition','Default','Diamond','Ellipse','HBox','Icon','Line','Loop','Padding','Proportional','Rectangle','Shadow','Sizer','Svg','Switch','TextBox','VBox']
    
    def __GetSvgItems(self):
        '''
        Svg has only option for two subelements, so if Svg is selected, this is the content of its submenu
        '''
        return ['G','Path']
    
    def menuitem_remove(self, widget,string):
        '''
        action fired when clicked on remove option
        '''
        item = self.t.treeview.get_selection().get_selected()[1]
        self.t.treestore.remove(item)

class ContextMenuLine(gtk.Menu):
    '''
    context menu used for relationship modelling
    when modelling objects, use ContextMenu instead
    '''
    def __init__(self, t):
        gtk.Menu.__init__(self)
        self.t = t
        self.addmenuitem = gtk.MenuItem("Add")
        
        submenuadd = gtk.Menu()
        
        #ak sme v roote
        if (self.t.treeview.get_selection().get_selected()[1]==None):
            selection = self.__GetSubMenuItemsRoot()
        elif (self.t.treeview.get_model().get_value(self.t.treeview.get_selection().get_selected()[1],0)=="ConnectionLine"):
            selection = ""
        elif (self.t.treeview.get_model().get_value(self.t.treeview.get_selection().get_selected()[1],0)=="ConnectionArrow"):
            selection = ""  
        elif (self.t.treeview.get_model().get_value(self.t.treeview.get_selection().get_selected()[1],0)=="Condition"):
            selection = self.__GetSubMenuLineSpecial()   
        elif (self.t.treeview.get_model().get_value(self.t.treeview.get_selection().get_selected()[1],0)=="Loop"):
            selection = self.__GetSubMenuLineSpecial()  
        elif (self.t.treeview.get_model().get_value(self.t.treeview.get_selection().get_selected()[1],0)=="Switch"):
            selection = eval("['Case']")     
        elif (self.t.treeview.get_model().get_value(self.t.treeview.get_selection().get_selected()[1],0)=="Case"):
            selection = self.__GetSubMenuLineSpecial()         
        else: selection = self.__GetSubMenuItems()  
                   
        addrootitems = gtk.MenuItem("Add to Root")
        submenuaddroot = gtk.Menu()
        sel_root_items = self.__GetSubMenuItemsRoot()
        for mit in sel_root_items:
            menu_items = gtk.MenuItem(mit)         
            menu_items.connect("activate", self.addRoot, mit)
            menu_items.show()
            submenuaddroot.append(menu_items)      
        
            addrootitems.set_submenu(submenuaddroot)
            addrootitems.show()
            self.append(addrootitems)        
        
        #print self.t.treeview.get_model().get_value(self.t.treeview.get_selection().get_selected()[1],1)
        if selection is not None:
            for mit in selection:
                menu_items = gtk.MenuItem(mit)         
                menu_items.connect("activate", self.add, mit)
                menu_items.show()
                submenuadd.append(menu_items)      
        
                self.addmenuitem.set_submenu(submenuadd)
                self.addmenuitem.show()
                self.append(self.addmenuitem)
        
        
        self.removeitem = gtk.MenuItem("Remove")
        self.removeitem.connect("activate", self.menuitem_remove, 'Remove')
        self.removeitem.show()
        self.append(self.removeitem)
        self.show()

    def add(self,widget,string):
        '''
        add action is fired when one item from context menu is selected
        '''
        parent = self.t.treestore.append(self.t.treeview.get_selection().get_selected()[1])
        item = AppearanceFactory.CreateElement(string)
        self.t.treestore.set(parent,0,item.Identity(),1,item)
    
    def addRoot(self,widget,string):
        '''
        this action adds more items into root. It cannot be done by gtk.TreeView alone, because of lack of its functionality
        '''
        item = AppearanceFactory.CreateElement(string)
        parent = self.t.treestore.append(None)
        self.t.treestore.set(parent,0,item.Identity(),1,item)
        
    def __GetSubMenuItems(self):
        '''
        list of items to construct submenu
        '''
        return ['Align','Condition','Default','Diamond','Ellipse','HBox','Icon','Line','Loop','Padding','Proportional','Rectangle','Shadow','Sizer','Svg','Switch','TextBox','VBox']
    
    def __GetSubMenuItemsRoot(self):
        '''
        submenu items when extending the root
        '''
        return ['Label']+self.__GetSubMenuLineSpecial()
    
    def __GetSubMenuLineSpecial(self):
        '''
        this list is a submenu of Condition, Loop and Case
        '''
        return ['ConnectionArrow','ConnectionLine','Condition','Loop','Shadow','Switch']
    
    def menuitem_remove(self, widget,string):
        '''
        action fired when clicked on remove option
        '''
        item = self.t.treeview.get_selection().get_selected()[1]
        self.t.treestore.remove(item)

class EditWindow(object):
    '''
    EditWindow is a visual part for editing Object and Relationship objects
    '''
    def __init__(self,manager,selected,project,type,treestore=None,visual_identity=None):
        self.manager = manager
        self.selected = selected
        self.project = project
        self.type = type
        self.appearanceGenerator = AppearanceGenerator()
        
        if visual_identity is not None:
            self.visual_identity = visual_identity
        else: self.visual_identity = None
        
        self.TARGETS = [
        ('object', gtk.TARGET_SAME_WIDGET, 0),
        ('text/plain', 0, 1),
        ('TEXT', 0, 2),
        ('STRING', 0, 3),
        ]
        
        self.__ConstructBasicLayout()
         
        if treestore is not None:
            self.treestore = treestore
        else: 
            self.treestore = gtk.TreeStore(str,object)
            if (self.type=="Relationship"):self.__CreateRelationshipBase()
            
        self.tmpModel = gtk.ListStore(str,str)
        self.pathsStore = gtk.ListStore(str,str)
        self.domainsTreeStore = gtk.TreeStore(str,str)

        self.__ConstructLeftTW()
        
        self.__ConstructCanvas()
         
        self.__ConstructRightTW()
        
        self.__ConstructPaths()
        
        self.__ConstructDomains()
        
        self.__ConstructHints()
        
        self.__ConstructButtons()
        
        self.window.show_all()
        gtk.main()
        
    def __ConstructBasicLayout(self):
        '''
        construct the basic layout in which other parts are inserted
        '''
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title("Metamodel Editor for "+str(self.type))
        self.window.set_size_request(800,600)
        self.vbox=gtk.VBox() 
        self.hbox = gtk.HBox()  
        self.vbox.add(self.hbox)  
        self.hboxBottom = gtk.HBox()
        self.hboxBottom.set_size_request(800,300)
        
        self.vbox.add(self.hboxBottom)
        self.window.add(self.vbox)    
        
    def __ConstructLeftTW(self):
        '''
        method used to construct left TreeView
        '''
        leftvbox = gtk.VBox()
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
        cell = gtk.CellRendererText()
        self.tvcolumn.pack_start(cell, True)
        self.tvcolumn.add_attribute(cell, "text", 0)
        
        leftvbox.pack_start(self.treeview)      
        self.hbox.pack_start(leftvbox)       
        
    def __ConstructCanvas(self):
        '''
        canvas for previews
        '''
        self.canvas = gtk.DrawingArea()
        self.canvas.set_size_request(400,600)       
        self.hbox.pack_start(self.canvas)

        
    def PaintSelf(self):
        '''
        method used to repaint the upper middle part (preview)
        '''
        canvasarea = self.canvas.window
        
        if (self.type=="Object"):
            self.appearanceGenerator.SetTreeView(self.treeview.get_model())
            domaintype = DomainType("bulk")
                   
            a = FakeFactory()

            cairo = CairoCanvas(self.canvas)
            cairo.Clear()
            elementtype = ElementType(a)
            elementtype.SetAppearance(self.appearanceGenerator.DummyObjectAppearance(self.__FakeElement()))
            elementtype.SetDomain(domaintype)
        
            elementobject = ElementObject(elementtype)
        
            element = Element(elementobject)
        
            element.Paint(cairo,delta = (50,200))
        
        elif (self.type=="Relationship"):
            self.appearanceGenerator.SetTreeView(self.treeview.get_model())
            domainType = DomainType("bulk")
            domainType2 = DomainType("bulk")
   
            a = FakeFactory()
            elementtype = ElementType(a)
            elementtype.SetAppearance(self.appearanceGenerator.DummyObjectAppearance(self.__FakeElementForRelationship()))
            elementtype.SetDomain(domainType)
            elementtype2 = ElementType(a)
            elementtype2.SetAppearance(self.appearanceGenerator.DummyObjectAppearance(self.__FakeElementForRelationship()))
            elementtype2.SetDomain(domainType)
        
            elementobject = ElementObject(elementtype)
            elementobject2 = ElementObject(elementtype2)
            element = Element(elementobject)
            element2 = Element(elementobject2)
             
            cairo = CairoCanvas(self.canvas)
            cairo.Clear()
             
            connectionType = self.appearanceGenerator.DummyRelationshipProcesser(self.__FakeRelationship(),domainType2,a)
            
            connectionObject = ConnectionObject(connectionType,elementobject,elementobject2)
             

            element.Paint(cairo,delta = (30,100))
            element.SetPosition((30,100))
            element2.Paint(cairo,delta = (300,100))
            element2.SetPosition((300,100))
            connection = Connection(connectionObject,element,element2)
             #points=[(200,100),(30,100)]
            
            connection.Paint(cairo,delta=(0,0))
             
                 
        else: print "uncompatible type"
        
    def __FakeElement(self):
        '''
        creates a fake appearance of element for preview
        '''
        return AppearanceGenerator().GenerateXML()
    
    def __FakeElementForRelationship(self):
        '''
        creates a preview element, which is used twice for relationship preview 
        at both its ends
        '''
        return AppearanceGenerator().GenerateSampleRounded()
    
    def __FakeRelationship(self):
        '''
        creates a preview relationship 
        '''
        return AppearanceGenerator().GenerateRelationshipXML()
        
    def __ConstructRightTW(self):
        '''
        basic structure of Properties part of a window
        '''
        self.twProperties = gtk.TreeView()
        self.hbox.pack_end(self.twProperties)  
        
    def __ConstructPaths(self):
        '''
        Paths are the list from paths.xml representing vector curves
        '''
        myVBox = gtk.VBox()
        scrolled = gtk.ScrolledWindow()
        scrolled.set_policy(gtk.POLICY_AUTOMATIC,gtk.POLICY_AUTOMATIC)
        myVBox.pack_start(scrolled, True, True, 0)
        scrolled.show()
        
        self.paths = gtk.TreeView(self.pathsStore) 
        self.paths.get_selection().set_mode(gtk.SELECTION_SINGLE)
        
        column=gtk.TreeViewColumn("Path id")
        self.paths.append_column(column)
        cell = gtk.CellRendererText()
        cell.set_property('editable',True)
        column.pack_start(cell, True)
        column.add_attribute(cell, "text", 0)
        
        column1=gtk.TreeViewColumn("Value")
        self.paths.append_column(column1)
        cell1 = gtk.CellRendererText()
        column1.pack_start(cell1, True)
        column1.add_attribute(cell1, "text", 1)
        
        a = FakeFactory().GetMetamodel().GetPathFactory()
        for it in a.GetPaths():
            key,value = it
            newitem = self.pathsStore.append(None)
            self.pathsStore.set(newitem,0,key,1,value)
        
        scrolled.add_with_viewport(self.paths)
        myVBox.set_size_request(200,130)
        #myVBox.pack_start(self.paths)
        self.hboxBottom.pack_start(myVBox) 
        
    def __ConstructDomains(self):
        '''
        domains part of the window is in the centre of bottom part of hbox
        '''
        self.domainsTree = gtk.TreeView(self.domainsTreeStore)
        self.domainsTree.get_selection().set_mode(gtk.SELECTION_SINGLE)
        scrolled = gtk.ScrolledWindow()
        scrolled.set_policy(gtk.POLICY_AUTOMATIC,gtk.POLICY_AUTOMATIC)
        scrolled.set_size_request(300,130)
        self.hboxBottom.pack_start(scrolled,True,True,0)
        scrolled.show()
        
        column = gtk.TreeViewColumn("Elements")
        self.domainsTree.append_column(column)
        cell=gtk.CellRendererText()
        cell.set_property('editable',True)
        column.pack_start(cell,True)
        column.add_attribute(cell,"text",0)
        
        column1 = gtk.TreeViewColumn("Values")
        self.domainsTree.append_column(column1)
        cell1=gtk.CellRendererText()
        column1.pack_start(cell1,True)
        column1.add_attribute(cell1,"text",1)
        
        el = self.selected.GetObject().GetSaveInfo().items()
        for it in el:
            key,value = it
            newitem = self.domainsTreeStore.append(None)
            self.domainsTreeStore.set(newitem,0,key,1,value)
        
        scrolled.add_with_viewport(self.domainsTree) 
    
    def __ConstructHints(self):
        '''
        hints are situated in the right end of bottom hbox part
        '''
        self.hboxBottomRight=gtk.VBox()
        scrolled = gtk.ScrolledWindow()
        self.hboxBottomRight.pack_start(scrolled, True, True, 0)
        scrolled.set_policy(gtk.POLICY_AUTOMATIC,gtk.POLICY_AUTOMATIC)
        scrolled.show()
        simpleListStore = gtk.ListStore(str)
        hintsTree = gtk.TreeView(simpleListStore)
        
        column = gtk.TreeViewColumn("Variables")
        hintsTree.append_column(column)
        cell=gtk.CellRendererText()
        cell.set_property('editable',True)
        column.pack_start(cell,True)
        column.add_attribute(cell,"text",0)
        consts = None
        if self.type=="Object":
            consts = ELEMENT_HINTS   
        elif self.type=="Relationship":
            consts = CONNECTION_HINTS
            
        for it in consts:
            newit = simpleListStore.append(None)
            simpleListStore.set(newit,0,it)       
        
        scrolled.add_with_viewport(hintsTree)
        self.hboxBottomRight.show()
        self.hboxBottom.pack_end(self.hboxBottomRight)    
    
    def __ConstructButtons(self):
        '''
        there are currently two buttons created: Close and Save
        '''
        hbutbox = gtk.HButtonBox()

        close = gtk.Button("Close")
        save = gtk.Button("Save")
        close.connect('clicked',self.close)
        save.connect('clicked',self.save)

        hbutbox.add(close)
        hbutbox.add(save)
        self.hboxBottomRight.pack_end(hbutbox)          
    
    def close(self,param):
        '''
        Closes the window and destroys it
        '''
        self.window.destroy()
    
    #self.visual_identity je kvoli tomu, ze ak podhodim zastupcu, tak najdem jeho realny element, ale 
    #ten moze mat inu hodnotu self.visual_identity. avsak domenove informacie sedia    
    def save(self,param):
        '''
        Saves the {visual_identity,representation} pair
        '''
        if self.type == 'Object':
            if self.visual_identity is not None: self.manager.metamodels[self.visual_identity]=self.treestore
            else: self.manager.metamodels[self.selected.GetObject().GetValue(VISUAL_IDENTITY)]=self.treestore
            print self.manager.metamodels
        elif self.type == 'Relationship':
            if self.visual_identity is not None: self.manager.metamodelsRel[self.visual_identity]=self.treestore
            else: self.manager.metamodelsRel[self.selected.GetObject().GetValue(VISUAL_IDENTITY)]=self.treestore    
            print self.manager.metamodelsRel
                
    def on_button_press_event(self, widget, event):
        '''
        catches button_press event of main treeview
        '''
        if (event is None): return       
        if event.button == 3 and event.type == gtk.gdk.BUTTON_PRESS:
            if (self.type=="Object"): c = ContextMenu(self)
            elif (self.type=="Relationship"): c = ContextMenuLine(self)
            c.popup(None, None, None, event.button, event.get_time())           
            
    def on_cursor_changed(self, treeview):
        '''
        fired when a new element in main treeview is selected
        '''
        ret = self.GetSelectedItem(treeview)

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
        '''
        returns selected item from main treeview
        '''
        if (widget is not None):
            test = gtk.TreeView()
            entry1, entry2 = widget.get_selection().get_selected()
            entry = entry1.get_value(entry2, 1)
            return entry
     
    def SetPropertiesModel(self, source):
        '''
        from selected item this method constructs the right table with data
        '''
        self.tmpModel.clear()
        if (source is not None): 
            attr = source.GetAttributes().items()
            for it in attr:
                key, val = it
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
    
    def __CreateRelationshipBase(self):
        '''
        this is base for a relationship (when there is no match in saved)
        '''
        parent = self.treestore.append(None)
        itempar = AppearanceFactory.CreateElement('ConnectionArrow')
        self.treestore.set(parent,0,itempar.Identity(),1,itempar)
        
        quex = self.treestore.append(None)
        item = AppearanceFactory.CreateElement('ConnectionLine')
        self.treestore.set(quex,0,item.Identity(),1,item)
        
        quex5 = self.treestore.append(None)
        item5 = AppearanceFactory.CreateElement('Label')
        self.treestore.set(quex5,0,item5.Identity(),1,item5)
        
        quex6 = self.treestore.append(quex5)
        item6 = AppearanceFactory.CreateElement('TextBox')
        self.treestore.set(quex6,0,item6.Identity(),1,item6)
         
    def value_edited(self,cell, path, new_text, user_data): 
        '''
        when a value from right table is edited, some action is needed to be performed
        (like set the value into appropriate back-end object)
        '''
        liststore, column = user_data
        column = 1
        liststore[path][column] = new_text
        
        #now i am gonna set the value into appropriate backend object
        self.GetSelectedItem(self.treeview).GetAttributes()[liststore[path][0]]=new_text
    
    def drag_data_get_data(self, treeview, context, selection, target_id,
                           etime):
        '''
        Drag n drop: get data from drag source
        '''
        treeselection = treeview.get_selection()
        model, iter = treeselection.get_selected()
        data = model.get_value(iter, 0)
        selection.set(selection.target,8,data)
    
    def drag_data_received_data(self, widget, context, x, y, selection, info, etime):
        '''
        Drag n drop: set data into drag destination
        '''
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
        '''
        validation for drag n drop action
        '''
        path_of_iter_to_copy = model.get_path(iter_to_copy)
        path_of_target_iter = model.get_path(target_iter)
        if path_of_target_iter[0:len(path_of_iter_to_copy)] == path_of_iter_to_copy:
            return False
        elif len(path_of_target_iter) < 2:
            return False
        else:
            return True
    
    def IterCopy(self, treeview, model, iter_to_copy, target_iter, pos):
        '''
        method for copying items in treeview
        '''
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