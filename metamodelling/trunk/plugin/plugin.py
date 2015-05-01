#!/usr/bin/python

import os.path
import gtk
import appearance
from export.export import Export
from iconChooser import IconChooser
from appearanceManager import AppearanceManager

from org.umlfri.api.mainLoops import GtkMainLoop

def pluginMain(interface):
    exportWindow = Export(interface)
    iconChooser = IconChooser(interface)
    appMng = AppearanceManager(interface)

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
        lambda *a:appMng.show(),
        -1,
        'Appearance',
        False,
        ''
    )

    def projectOpened():
        if interface.project.metamodel.uri == 'urn:umlfri.org:metamodel:metamodeling':
            for node in interface.project.root.children:
                if node.type.name == 'Element':
                    x = node.values['appearance']
                    #print type(x)

    interface.add_notification('project-opened', projectOpened)

    interface.transaction.autocommit = True
    interface.set_main_loop(GtkMainLoop())


