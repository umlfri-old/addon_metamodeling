import gtk
import constants 
import shutil
import os

class IconChooser:
    def __init__(self, interface):
        self.i = interface
        self.selected = None
        
    def show(self):
        selected = []
        for item in self.i.current_diagram.selected:
            selected.append(item)
        if len(selected) != 1:
            md = gtk.MessageDialog(None, gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_ERROR, gtk.BUTTONS_CLOSE, 'Select only one element.')
            md.run()
            md.destroy()
            return
        self.selected = selected[0]
        if self.selected.object.type.domain.name == constants.ENUM_DOMAIN_NAME:
            md = gtk.MessageDialog(None, gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_ERROR, gtk.BUTTONS_CLOSE, 'Can not choose icon for enum.')
            md.run()
            md.destroy()
            return
        chooser = gtk.FileChooserDialog(title='Choose icon',action=gtk.FILE_CHOOSER_ACTION_OPEN,buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK))
        pngFilter = gtk.FileFilter()
        pngFilter.set_name("png files")
        pngFilter.add_pattern("*.png")
        chooser.add_filter(pngFilter)
        response = chooser.run()
        if response == gtk.RESPONSE_OK:
            icon = os.path.split(os.path.realpath(chooser.get_filename()))[1]
            path = os.path.split(os.path.realpath(__file__))[0]
            path = path.replace('plugin', 'metamodel/userIcons/')
            try:
                shutil.copy(chooser.get_filename(), path)
            except shutil.Error: #same file exception
                pass
            self.selected.object.values['icon'] = 'userIcons/'+icon            
        elif response == gtk.RESPONSE_CANCEL:
            pass
        chooser.destroy()
