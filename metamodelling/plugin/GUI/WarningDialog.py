'''
Created on 23.3.2010

@author: Michal Kovacik
'''
import sys
import pygtk
pygtk.require('2.0')

try:
    import gtk
    import gtk.glade
except:
    sys.exit(1)    

class WarningDialog(gtk.Dialog):
    def __init__(self,message): 
        super(WarningDialog, self).__init__("UML .FRI Warning")
        self.set_size_request(350,130)
        self.connect("delete_event", lambda w,e: self.hide())
        
        label = gtk.Label(message)
        self.vbox.pack_start(label,True,True,0)
        label.show()
        
        button = gtk.Button(stock=gtk.STOCK_CLOSE)
        button.connect("clicked", lambda w: self.hide())
        self.vbox.pack_start(button, True, True, 0)
        button.show()
        
        self.show()
        gtk.main() 
   
        