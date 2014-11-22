#!/usr/bin/python

import os.path
import gtk
from export.export import Export
from chooseConnections import ChooseConnections
from iconChooser import IconChooser
from test import Test

from org.umlfri.api.mainLoops import GtkMainLoop

def pluginMain(interface):
    exportWindow = Export(interface)
    iconChooser = IconChooser(interface)
    test = Test(interface)
    
    interface.gui_manager.button_bar.add_button(
        'export_metamodel',
        lambda *a: exportWindow.show(),
        -1,
        'Export metamodel',
        imagefilename = os.path.join('icons', 'export.png')
    )

    interface.gui_manager.draw_menu.add_menu_item(
        'chooseIcon',
        lambda *a:iconChooser.show(),
        -1,
        'Choose icon',
        False,
        ''
    )
    interface.gui_manager.draw_menu.add_menu_item(
        'appearance',
        lambda *a:test.show(),
        -1,
        'Appearance',
        False,
        ''
    )
    
    interface.transaction.autocommit = True
    interface.set_main_loop(GtkMainLoop())
