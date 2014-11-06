#!/usr/bin/python

import os.path
import gtk
from export.export import Export
from chooseConnections import ChooseConnections
from iconChooser import IconChooser

from org.umlfri.api.mainLoops import GtkMainLoop

def pluginMain(interface):
    print "start----------"
    exportWindow = Export(interface)
    connections = ChooseConnections(interface)
    iconChooser = IconChooser(interface)
    
    interface.gui_manager.button_bar.add_button(
        'export_metamodel',
        #lambda *a: W.show_all(),
        lambda *a: exportWindow.show(),
        -1,
        'Export metamodel',
        imagefilename = os.path.join('icons', 'export.png')
    )
    interface.gui_manager.draw_menu.add_menu_item(
        'chooseConnections',
        lambda *a:connections.show(),
        -1,
        'Add connections',
        False,
        ''
    )
    interface.gui_manager.draw_menu.add_menu_item(
        'chooseIcon',
        lambda *a:iconChooser.show(),
        -1,
        'Choose icon',
        False,
        ''
    )
    
    interface.transaction.autocommit = True
    interface.set_main_loop(GtkMainLoop())
    print "end-------------"
    #dra=DRA(interface)
    #dra.pluginMain()
