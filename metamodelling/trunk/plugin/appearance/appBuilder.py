from lxml import etree
import gtk
import constants
from container import Container
from diamond import Diamond
from switch import Switch
from simpleContent import SimpleContent
from condition import Condition
from loop import Loop
from padding import Padding
from proportional import Proportional
from rectangle import Rectangle
from sizer import Sizer
from icon import Icon
from line import Line
from textBox import TextBox
from connectionLine import ConnectionLine
from connectionArrow import ConnectionArrow
from labelScrolledWindow import LabelScrolledWindow
from simpleContent import SimpleContent

class AppBuilder():
    def __init__(self):
        self.elementStore = []  #to store align, shadow and use them later on visual element

    def buildApp(self, manager):
        manager.switchList = []
        try:
            root = etree.fromstring(manager.selected.object.values['appearance'])
            self.manager = manager
            self.elementStore = []
            if self.manager.selected.object.type.name == constants.ELEMENT_OBJECT_NAME:
                for child in root:
                    content = self.elementChooser(child, None)
                    manager.rootObject = content
                    widget = manager.wTree.get_widget('vboxContent').children()[0]
                    self.removeLabelAndSignals(widget)
                    widget.add_Content(content)
                    widget.show_all()
            if self.manager.selected.object.type.name == constants.CONNECTION_OBJECT_NAME:
                self.addLineAndArrowContent(root)
                self.addLabelContent(root)
        except etree.XMLSyntaxError:
            pass

    def elementChooser(self, element, parent):
        if element.tag == 'VBox' or element.tag == 'HBox':
            content = self.containerBuilder(element, parent)
        elif element.tag == 'Diamond' or element.tag == 'Ellipse':
            content = self.diamondBuilder(element, parent)
        elif element.tag == 'Align':
            content = self.alignBuilder(element, parent)
        elif element.tag == 'Diamond' or element.tag == 'Ellipse':
            content = self.diamondBuilder(element, parent)
        elif element.tag == 'Shadow':
            content = self.shadowBuilder(element, parent)
        elif element.tag == 'Switch':
            content = self.switchBuilder(element, parent)
        elif element.tag == 'Condition':
            content = self.conditionBuilder(element, parent)
        elif element.tag == 'Loop':
            content = self.loopBuilder(element, parent)
        elif element.tag == 'Padding':
            content = self.paddingBuilder(element, parent)
        elif element.tag == 'Proportional':
            content = self.proportionalBuilder(element, parent)
        elif element.tag == 'Rectangle':
            content = self.rectangleBuilder(element, parent)
        elif element.tag == 'Sizer':
            content = self.sizerBuilder(element, parent)
        elif element.tag == 'Icon':
            content = self.iconBuilder(element, parent)
        elif element.tag == 'Line':
            content = self.lineBuilder(element, parent)
        elif element.tag == 'TextBox':
            content = self.textBoxBuilder(element, parent)
        elif element.tag == 'ConnectionLine':
            content = self.connectionLineBuilder(element, parent)
        elif element.tag == 'ConnectionArrow':
            content = self.connectionArrowBuilder(element, parent)
        return content

    def containerBuilder(self, element, parent):
        if element.tag == 'HBox':
            name = 'Horizontal box'
            box = gtk.VBox()
        else:
            name = 'Vertical box'
            box = gtk.HBox()
        container = Container(name, box, self.manager, parent)
        for ele in self.elementStore:
            if ele[0] == element and ele[1].tag == 'Align':
                container.align.setAlign(ele[1].get('align'))
        for child in element.iter():
            if child.getparent() == element:
                content = self.elementChooser(child, container)
                widget = container.box.get_children()[-1]
                self.removeLabelAndSignals(widget)
                widget.add_Content(content)
        container.changePacking()
        for child in container.childObjects:
            if child.content:
                try:
                    child.content.expand.setExpand(False)
                except AttributeError: # Line does not have expand
                    pass
        expand = element.get('expand')
        if expand:
            expand = expand.split()
            for number in expand:
                container.childObjects[int(number)].content.expand.setExpand(True)
        return container

    def diamondBuilder(self, element, parent):
        diamond = Diamond(element.tag, gtk.VBox(), self.manager, parent)
        for ele in self.elementStore:
            if ele[0] == element and ele[1].tag == 'Shadow':
                diamond.shadow.setShadow(ele[1])
        border = element.get('border')
        if border:
            diamond.borderColorButton.setColor(border)
        fill = element.get('fill')
        if fill:
            diamond.fillColorButton.setColor(fill)
        for child in element:
            content = self.elementChooser(child, diamond)
            widget = diamond.box.get_children()[-1]
            self.removeLabelAndSignals(widget)
            widget.add_Content(content)
        return diamond

    def switchBuilder(self, element, parent):
        switch = Switch(element.tag, gtk.VBox(), self.manager, parent)
        switchValue = element.get('value')
        if switchValue:
            switch.switchValue.set_text(switchValue)
        switch.notebook.remove_page(0)
        del switch.childObjects[0]
        for child in element.iter():
            if child.getparent() == element:
                sc = SimpleContent(switch, self.manager)
                for caseChild in child:
                    self.removeLabelAndSignals(sc)
                    sc.add_Content(self.elementChooser(caseChild, switch))
                switch.notebook.append_page(sc, gtk.Label(child.get('condition')))
                switch.childObjects.append(sc)
        return switch

    def conditionBuilder(self, element, parent):
        condition = Condition(element.tag, gtk.VBox(), self.manager, parent)
        value = element.get('condition')
        if value:
            condition.condition.set_text(value)
        for child in element:
            content = self.elementChooser(child, condition)
            widget = condition.box.get_children()[-1]
            self.removeLabelAndSignals(widget)
            widget.add_Content(content)
        return condition

    def loopBuilder(self, element, parent):
        loop = Loop(element.tag, gtk.VBox(), self.manager, parent)
        collection = element.get('collection')
        if collection != '':
            loop.selectedLoop = collection
        loop.showProperties(None, None)
        for child in element:
            content = self.elementChooser(child, loop)
            widget = loop.box.get_children()[-1]
            self.removeLabelAndSignals(widget)
            widget.add_Content(content)
        return loop

    def paddingBuilder(self, element, parent):
        padding = Padding(element.tag, gtk.VBox(), self.manager, parent)
        paddingValue = element.get('padding')
        if paddingValue:
            padding.paddingSpin.set_value(int(paddingValue))
        left = element.get('left')
        if left:
            padding.leftSpin.set_value(int(left))
        right = element.get('right')
        if right:
            padding.rightSpin.set_value(int(right))
        top = element.get('top')
        if top:
            padding.topSpin.set_value(int(top))
        bottom = element.get('bottom')
        if bottom:
            padding.bottomSpin.set_value(int(bottom))
        for child in element:
            content = self.elementChooser(child, padding)
            widget = padding.box.get_children()[-1]
            self.removeLabelAndSignals(widget)
            widget.add_Content(content)
        return padding

    def proportionalBuilder(self, element, parent):
        prop = Proportional(element.tag, gtk.VBox(), self.manager, parent)
        ratio = element.get('ratio')
        prop.ratio.set_text(ratio)
        size = element.get('size')
        if size == 'maximal':
            prop.size.set_active(1)
        else:
            prop.size.set_active(0)
        if element.get('align'):
            prop.align.setAlign(element.get('align'))
        for child in element:
            content = self.elementChooser(child, prop)
            widget = prop.box.get_children()[-1]
            self.removeLabelAndSignals(widget)
            widget.add_Content(content)
        return prop

    def rectangleBuilder(self, element, parent):
        rectangle = Rectangle(element.tag, gtk.VBox(), self.manager, parent)
        for ele in self.elementStore:
            if ele[0] == element and ele[1].tag == 'Shadow':
                rectangle.shadow.setShadow(ele[1])
        border = element.get('border')
        if border:
            rectangle.borderColorButton.setColor(border)
        fill = element.get('fill')
        if fill:
            rectangle.fillColorButton.setColor(fill)
        lefttop = element.get('lefttop')
        if lefttop:
            rectangle.leftTopCorner.setCorner(lefttop)
        righttop = element.get('righttop')
        if righttop:
            rectangle.rightTopCorner.setCorner(righttop)
        leftbot = element.get('leftbottom')
        if leftbot:
            rectangle.leftBotCorner.setCorner(leftbot)
        rightbot = element.get('rightbottom')
        if rightbot:
            rectangle.rightBotCorner.setCorner(rightbot)
        left = element.get('left')
        if left:
            rectangle.leftSide.setSide(left)
        right = element.get('right')
        if right:
            rectangle.rightSide.setSide(right)
        top = element.get('top')
        if top:
            rectangle.topSide.setSide(top)
        bot = element.get('bottom')
        if bot:
            rectangle.botSide.setSide(bot)
        for ele in self.elementStore:
            if ele[0] == element and ele[1].tag == 'Shadow':
                rectangle.shadow.setShadow(ele[1])
        for child in element:
            content = self.elementChooser(child, rectangle)
            widget = rectangle.box.get_children()[-1]
            self.removeLabelAndSignals(widget)
            widget.add_Content(content)
        return rectangle

    def sizerBuilder(self, element, parent):
        sizer = Sizer(element.tag, gtk.VBox(), self.manager, parent)
        sizer.setValues(element.get('minwidth'),element.get('minheight'),element.get('maxwidth'),element.get('maxheight'),element.get('width'),element.get('height') )
        for child in element:
            content = self.elementChooser(child, sizer)
            widget = sizer.box.get_children()[-1]
            self.removeLabelAndSignals(widget)
            widget.add_Content(content)
        return sizer

    def iconBuilder(self, element, parent):
        icon = Icon(self.manager, parent)
        filename = element.get('filename')
        if filename != '':
            icon.icon.set_from_file(filename)
            icon.path = filename
        for ele in self.elementStore:
            if ele[0] == element and ele[1].tag == 'Align':
                icon.align.setAlign(ele[1].get('align'))
            if ele[0] == element and ele[1].tag == 'Shadow':
                icon.shadow.setShadow(ele[1])
        return icon

    def lineBuilder(self, element, parent):
        line = Line(self.manager, parent)
        line.setLineType(element.get('type'))
        color = element.get('color')
        if color:
            line.buttonColor.setColor(color)
        for ele in self.elementStore:
            if ele[0] == element and ele[1].tag == 'Shadow':
                line.shadow.setShadow(ele[1])
        return line

    def textBoxBuilder(self, element, parent):
        textBox = TextBox(self.manager, parent)
        textBox.textEntry.set_text(element.get('text'))
        color = element.get('color')
        if color:
            textBox.setTextColor(color)
        textBox.setTextFont(element.get('font'))
        for ele in self.elementStore:
            if ele[0] == element and ele[1].tag == 'Align':
                textBox.align.setAlign(ele[1].get('align'))
            if ele[0] == element and ele[1].tag == 'Shadow':
                textBox.shadow.setShadow(ele[1])
        return textBox

    def alignBuilder(self, element, parent):
        for child in element:
            if child.tag == 'Shadow':
                for c in child:
                    self.elementStore.append([c, element])
                    return self.elementChooser(child, parent)
            else:
                self.elementStore.append([child, element])
                return self.elementChooser(child, parent)

    def shadowBuilder(self, element, parent):
        for child in element:
            self.elementStore.append([child, element])
            return self.elementChooser(child, parent)

    def connectionLineBuilder(self, element, parent):
        line = ConnectionLine(self.manager, parent)
        color = element.get('color')
        if color:
            line.setLineColor(color)
        style = element.get('style')
        if style:
            line.setLineStyle(style)
        width = element.get('width')
        if width:
            line.setLineWidth(width)
        begin = element.get('begin')
        if begin:
            line.setLineBegin(begin)
        end = element.get('end')
        if end:
            line.setLineEnd(end)
        return line

    def connectionArrowBuilder(self, element, parent):
        arrow = ConnectionArrow(self.manager, parent)
        index = element.get('index')
        if index:
            arrow.setIndex(index)
        style = element.get('style')
        if style:
            arrow.setArrowStyle(style)
        color = element.get('color')
        if color:
            arrow.setArrowColor(color)
        fill = element.get('fill')
        if fill:
            arrow.setFillColor(fill)
        return arrow

    def removeLabelAndSignals(self, widget):
        widget.remove(widget.get_Label())
        widget.disconnect(widget.enterNotifyHandler)
        widget.disconnect(widget.buttonReleaseHandler)

    def addLineAndArrowContent(self, root):
        container = self.manager.notebook.get_nth_page(0).get_child().get_child()
        for child in root:
            if child.tag != 'Label':
                content = self.elementChooser(child, container)
                widget = container.box.get_children()[-1]
                self.removeLabelAndSignals(widget)
                widget.add_Content(content)
        container.show_all()

    def addLabelContent(self, root):
        for child in root:
            if child.tag == 'Label':
                sw = LabelScrolledWindow()
                sw.add_with_viewport(SimpleContent(None,self.manager))
                self.manager.notebook.insert_page(sw, gtk.Label('Label'), self.manager.notebook.get_n_pages()-1)
                sw.setPosition(child.get('position'))
                for element in child:
                    content = self.elementChooser(element, None)
                    widget = sw.get_child().get_child()
                    self.removeLabelAndSignals(widget)
                    widget.add_Content(content)
        self.manager.notebook.show_all()