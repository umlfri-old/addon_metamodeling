import gtk
import gtk.glade
from lxml import etree
import os
import constants
from appearance.simpleContent import SimpleContent
from appearance.container import Container
from appearance.textBox import TextBox
from appearance.line import Line
from appearance.icon import Icon
from appearance.padding import Padding
from appearance.sizer import Sizer
from appearance.proportional import Proportional
from appearance.condition import Condition
from appearance.loop import Loop
from appearance.diamond import Diamond
from appearance.rectangle import Rectangle
from appearance.switch import Switch
from appearance.connectionLine import ConnectionLine
from appearance.lineAndArrowVBox import LineAndArrowVBox
from appearance.connectionArrow import ConnectionArrow
from appearance.labelScrolledWindow import LabelScrolledWindow
from appearance.appBuilder import AppBuilder
import constants
from lxml import etree


class AppearanceManager:
    def __init__(self, interface):
        self.i = interface
        self.dic = { "on_button_horizontal_box_clicked" : self.widgetClicked,
                     "on_button_vertical_box_clicked" : self.widgetClicked,
                     "on_appearanceWindow_key_release_event" : self.keyPressed,
                     "on_button_text_box_clicked" : self.widgetClicked,
                     "on_button_line_clicked" : self.widgetClicked,
                     "on_appearanceWindow_check_resize" : self.windowResized,
                     "on_button_icon_clicked" : self.widgetClicked,
                     "on_button_padding_clicked" : self.widgetClicked,
                     "on_button_sizer_clicked" : self.widgetClicked,
                     "on_button_proportional_clicked" : self.widgetClicked,
                     "on_button_condition_clicked" : self.widgetClicked,
                     "on_button_loop_clicked" : self.widgetClicked,
                     "on_button_diamond_clicked" : self.widgetClicked,
                     "on_button_ellipse_clicked" : self.widgetClicked,
                     "on_button_rectangle_clicked" : self.widgetClicked,
                     "on_button_switch_clicked" : self.widgetClicked,
                     "on_button_connection_line_clicked" : self.widgetClicked,
                     "on_button_connection_arrow_clicked" : self.widgetClicked,
                     "on_button_save_clicked" : self.saveApp}
        self.closed = True
        self.widgetSelected = False
        self.selectedButton = None
        self.default_color = None
        self.rootObject = None
        self.selected = None #selected element or connection in meta editor
        self.lastHighligted = None
        self.builder = AppBuilder()

    def close(self, widget):
        self.closed = True
        self.window.hide()
        return gtk.TRUE

    def close2(self, widget, widget2):
        self.closed = True
        self.window.hide()
        return gtk.TRUE

    def show(self):
        selected = []
        for item in self.i.current_diagram.selected:
            selected.append(item)
        if len(selected) != 1:
            md = gtk.MessageDialog(None, gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_ERROR, gtk.BUTTONS_CLOSE, 'Select only one Element or Connection.')
            md.run()
            md.destroy()
            return
        self.selected = selected[0]
        #print self.selected.object.__id__#GetUID()
        #print self.selected.object.values['appearance']
        if self.selected.object.type.name != constants.ELEMENT_OBJECT_NAME:
            if self.selected.object.type.name != constants.CONNECTION_OBJECT_NAME:
                md = gtk.MessageDialog(None, gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_ERROR, gtk.BUTTONS_CLOSE, 'Appearance can be specified only for Elements and Connections.')
                md.run()
                md.destroy()
                return
        if self.closed:
            self.init_Window()
            if self.selected.object.type.name == constants.CONNECTION_OBJECT_NAME:
                self.initConnectionWin()
            self.window.show()
            self.closed = False
        else:
            self.close(self.window)
            self.init_Window()
            self.show()
        self.builder.buildApp(self)

    def initConnectionWin(self):
        self.wTree.get_widget("vbox1").remove(self.wTree.get_widget("scrolledwindow1"))
        self.notebook = gtk.Notebook()

        sw = gtk.ScrolledWindow()
        sw.add_with_viewport(LineAndArrowVBox(gtk.VBox(), self, None))
        self.notebook.append_page(sw, gtk.Label('Line and arrow'))

        #sw = gtk.ScrolledWindow()
        sw = LabelScrolledWindow()
        sw.add_with_viewport(SimpleContent(None,self))
        self.notebook.append_page(sw, gtk.Label('+ Label'))


        sw = gtk.ScrolledWindow()
        sw.add_with_viewport(self.notebook)
        self.wTree.get_widget("vbox1").pack_start(sw, True,True)
        self.wTree.get_widget("vbox1").reorder_child(sw, 1)
        self.wTree.get_widget("vbox1").show_all()
        x,y = self.window.get_size()
        self.hideButtons()
        self.window.resize(x,y)
        self.notebookHandler = self.notebook.connect('switch-page', self.switchPage)

        self.showConnectionButtons()

    def printChild(self,child):
        for c in child:
            print c.tag, c.attrib
            self.printChild(c)

    def init_Window(self):
        self.gladefile = os.path.split(os.path.realpath(__file__))[0] + "/appearance.glade"
        self.wTree = gtk.glade.XML(self.gladefile)
        self.wTree.signal_autoconnect(self.dic)
        self.window = self.wTree.get_widget("appearanceWindow")
        self.window.connect("destroy", self.close)
        self.window.connect("delete_event", self.close2)
        self.window.set_position(gtk.WIN_POS_CENTER)
        self.window.set_keep_above(True)
        self.window.set_title('Appearance '+self.selected.object.name)
        self.widgetSelected = False
        self.selectedButton = None
        self.default_color = None
        self.lastHighligted = None
        vbox = self.wTree.get_widget('vboxContent')
        vbox.pack_start(SimpleContent(None,self))
        vbox.show_all()
        self.rootObject = None

    def widgetClicked(self, widget):
        self.widgetSelected = True
        self.selectedButton = widget
        self.clearProperties()

    def keyPressed(self, widget, key):
        if key.keyval == 65307:
            self.widgetSelected = False
            widget.window.set_cursor(None)

    def buttonAddEnter(self, widget, w):
        if self.widgetSelected == False:
            widget.window.set_cursor(None)
        if self.widgetSelected == True:
            widget.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.PLUS))

    def addContent(self, widget, w):
        if self.widgetSelected:
            self.widgetSelected = False
            widget.window.set_cursor(None)

            widget.remove(widget.get_Label())
            widget.disconnect(widget.enterNotifyHandler)
            widget.disconnect(widget.buttonReleaseHandler)

            content = None
            if self.selectedButton.name == 'button_horizontal_box':
                name = 'Horizontal box'
                content = Container(name, gtk.VBox(), self, widget.parentContainer)
                widget.add_Content(content)
            elif self.selectedButton.name == 'button_vertical_box':
                name = 'Vertical box'
                content = Container(name, gtk.HBox(), self, widget.parentContainer)
                widget.add_Content(content)
            elif self.selectedButton.name == 'button_text_box':
                content = TextBox(self, widget.parentContainer)
                widget.add_Content(content)
            elif self.selectedButton.name == 'button_line':
                content = Line(self, widget.parentContainer)
                widget.add_Content(content)
            elif self.selectedButton.name == 'button_icon':
                content = Icon(self, widget.parentContainer)
                widget.add_Content(content)
            elif self.selectedButton.name == 'button_padding':
                content = Padding('Padding', gtk.VBox(), self, widget.parentContainer)
                widget.add_Content(content)
            elif self.selectedButton.name == 'button_sizer':
                content = Sizer('Sizer', gtk.VBox(), self, widget.parentContainer)
                widget.add_Content(content)
            elif self.selectedButton.name == 'button_proportional':
                content = Proportional('Proportional', gtk.VBox(), self, widget.parentContainer)
                widget.add_Content(content)
            elif self.selectedButton.name == 'button_condition':
                content = Condition('Condition', gtk.VBox(), self, widget.parentContainer)
                widget.add_Content(content)
            elif self.selectedButton.name == 'button_loop':
                content = Loop('Loop', gtk.VBox(), self, widget.parentContainer)
                widget.add_Content(content)
            elif self.selectedButton.name == 'button_diamond':
                content = Diamond('Diamond', gtk.VBox(), self, widget.parentContainer)
                widget.add_Content(content)
            elif self.selectedButton.name == 'button_ellipse':
                content = Diamond('Ellipse', gtk.VBox(), self, widget.parentContainer)
                widget.add_Content(content)
            elif self.selectedButton.name == 'button_rectangle':
                content = Rectangle('Rectangle', gtk.VBox(), self, widget.parentContainer)
                widget.add_Content(content)
            elif self.selectedButton.name == 'button_switch':
                content = Switch('Switch', gtk.VBox(), self, widget.parentContainer)
                widget.add_Content(content)
            elif self.selectedButton.name == 'button_connection_line':
                content = ConnectionLine(self, widget.parentContainer)
                widget.add_Content(content)
            elif self.selectedButton.name == 'button_connection_arrow':
                content = ConnectionArrow(self, widget.parentContainer)
                widget.add_Content(content)
            widget.content.showProperties(None, None)
            if widget.parentContainer:
                if type(widget.parentContainer).__name__ == 'Container':
                    widget.parentContainer.changePacking()

            if self.rootObject == None:
                self.rootObject = content

            widget.show_all()

    def printNode(self, node):
        if node:
            print node.containerName
            for child in node.childObjects:
                self.printNode(child.content)

    def prehliadka(self, widget):
        for x in self.rootObject.childObjects:
            print x.content
        if self.rootObject != None:
            self.printNode(self.rootObject)

    def clearProperties(self):
        if self.lastHighligted:
            self.lastHighligted.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("black"))
        self.wTree.get_widget("label_name").set_text('')
        box = self.wTree.get_widget('vbox_properties')
        for w in box.children():
            box.remove(w)

    def clearAll(self):
        self.rootObject = None
        if self.selected.object.type.name == constants.CONNECTION_OBJECT_NAME:
            sw = self.notebook.get_nth_page(self.notebook.get_current_page())
            sw.remove(sw.get_child())
            sw.add_with_viewport(SimpleContent(None,self))
            sw.show_all()
        else:
            vbox = self.wTree.get_widget('vboxContent')
            for c in vbox.children():
                vbox.remove(c)
            vbox.pack_start(SimpleContent(None,self))
            vbox.show_all()
        self.clearProperties()

    def windowResized(self, widget):
        if self.rootObject:
            self.redraw(self.rootObject)

    def redraw(self, node):
        if node:
            try:
                node.exposeLine(node.drawArea, None)
            except AttributeError:
                pass
            try:
                for child in node.childObjects:
                    self.redraw(child.content)
            except AttributeError:
                pass

    def hideButtons(self):
        self.wTree.get_widget("button_horizontal_box").hide()
        self.wTree.get_widget("button_vertical_box").hide()
        self.wTree.get_widget("button_diamond").hide()
        self.wTree.get_widget("button_ellipse").hide()
        self.wTree.get_widget("button_padding").hide()
        self.wTree.get_widget("button_proportional").hide()
        self.wTree.get_widget("button_rectangle").hide()
        self.wTree.get_widget("button_sizer").hide()
        self.wTree.get_widget("button_icon").hide()
        self.wTree.get_widget("button_line").hide()
        self.wTree.get_widget("button_text_box").hide()

    def hideConnectionButtons(self):
        self.wTree.get_widget("button_connection_line").hide()
        self.wTree.get_widget("button_connection_arrow").hide()

    def showConnectionButtons(self):
        self.wTree.get_widget("button_connection_line").show()
        self.wTree.get_widget("button_connection_arrow").show()

    def showElementButtons(self):
        self.wTree.get_widget("button_horizontal_box").show()
        self.wTree.get_widget("button_vertical_box").show()
        self.wTree.get_widget("button_diamond").show()
        self.wTree.get_widget("button_ellipse").show()
        self.wTree.get_widget("button_padding").show()
        self.wTree.get_widget("button_proportional").show()
        self.wTree.get_widget("button_rectangle").show()
        self.wTree.get_widget("button_sizer").show()
        self.wTree.get_widget("button_icon").show()
        self.wTree.get_widget("button_line").show()
        self.wTree.get_widget("button_text_box").show()
        self.wTree.get_widget("label7").show()

    def switchPage(self, notebook, par1, page_num):
        self.clearProperties()
        label = self.notebook.get_tab_label_text(self.notebook.get_nth_page(page_num))
        if label == '+ Label':
            self.notebook.set_tab_label_text(self.notebook.get_nth_page(page_num),'Label')
            sw = LabelScrolledWindow()
            sw.add_with_viewport(SimpleContent(None,self))
            self.notebook.append_page(sw, gtk.Label('+ Label'))
            self.notebook.show_all()
            self.hideConnectionButtons()
            self.showElementButtons()
            self.showLabelProp(page_num)
        elif label == 'Label':
            self.hideConnectionButtons()
            self.showElementButtons()
            self.showLabelProp(page_num)
        elif label == 'Line and arrow':
            self.hideButtons()
            self.showConnectionButtons()

    def showLabelProp(self, page_num):
        self.clearProperties()
        labelScrolledWindow = self.notebook.get_nth_page(page_num)
        box = self.wTree.get_widget('vbox_properties')
        label = gtk.Label('Position')
        label.set_alignment(0.01, 0.5)
        box.pack_start(label, False)
        box.pack_start(labelScrolledWindow.position, False)
        box.pack_start(gtk.Label(' '),False)
        label = gtk.Label('Shifting')
        label.set_alignment(0.01, 0.5)
        box.pack_start(label, False)
        box.pack_start(labelScrolledWindow.shifting, False)
        box.pack_start(gtk.Label(' '),False)
        button = gtk.Button('Delete label')
        button.connect('clicked', self.deleteLabel)
        box.pack_start(button, False)
        box.show_all()

    def deleteLabel(self, widget):
        dialog = gtk.MessageDialog(None,0,gtk.MESSAGE_QUESTION,gtk.BUTTONS_YES_NO,'Delete label with whole content?')
        response = dialog.run()
        if response == gtk.RESPONSE_YES:
            self.notebook.disconnect(self.notebookHandler)
            self.notebook.remove_page(self.notebook.get_current_page())
            self.notebook.set_current_page(0)
            self.notebookHandler = self.notebook.connect('switch-page', self.switchPage)
            self.clearProperties()
        dialog.destroy()

    def saveApp(self, widget):
        self.app = '<Appearance>'
        if self.selected.object.type.name == constants.ELEMENT_OBJECT_NAME:
            if self.rootObject != None:
                self.app += self.rootObject.getApp()
        if self.selected.object.type.name == constants.CONNECTION_OBJECT_NAME:
            box = self.notebook.get_nth_page(0).get_child().get_child()
            self.app += box.getApp()
            for i in range(1, self.notebook.get_n_pages()-1):
                position = self.notebook.get_nth_page(i).getPosition()#position.get_active_text()
                self.app += '<Label position="' + position + '" >'
                if self.notebook.get_nth_page(i).get_child().get_child().content != None:
                    self.app +=  self.notebook.get_nth_page(i).get_child().get_child().content.getApp()
                self.app += '</Label>'
        self.app += '</Appearance>'
        self.selected.object.values['appearance'] = self.app
        print self.selected.object.values['appearance']
        self.close(None)