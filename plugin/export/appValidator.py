from lxml import etree
from appearance.container import Container
from appearance.line import Line
from appearance.padding import Padding
from appearance.switch import Switch
from appearance.condition import Condition
from appearance.loop import Loop
from appearance.padding import Padding
from appearance.proportional import Proportional
from appearance.sizer import Sizer
from appearance.icon import Icon
from appearance.labelScrolledWindow import LabelScrolledWindow
from appearance.shadow import Shadow
from appearance.diamond import Diamond
from appearance.rectangle import Rectangle
from appearance.line import Line
from appearance.textBox import TextBox
from appearance.connectionLine import ConnectionLine
from appearance.connectionArrow import ConnectionArrow
import constants

class AppValidator:

    @staticmethod
    def validate(dataElement):
        doNotCheck = ['Appearance', 'Case', 'Align']
        try:
            app = etree.fromstring(dataElement.values['appearance'])
        except Exception:
            return False, 'Appearance is missing for ' + dataElement.name + '.'
        if dataElement.type.name == constants.CONNECTION_OBJECT_NAME:
            hasLineEle = False
            for xmlEle in app.iter('ConnectionLine'):
                hasLineEle = True
            if not hasLineEle:
                return False, dataElement.name + ': Missing line element. Add connection line to appearance.'

        for xmlEle in app.iter():
            if xmlEle.tag not in doNotCheck:
                if xmlEle.tag == 'HBox' or xmlEle.tag == 'VBox':
                    result,msg = globals()['Container'].validate(xmlEle, dataElement)
                elif xmlEle.tag == 'Label':
                    result, msg = globals()['LabelScrolledWindow'].validate(xmlEle, dataElement)
                elif xmlEle.tag == 'Ellipse':
                    result, msg = globals()['Diamond'].validate(xmlEle, dataElement)
                else:
                    result, msg = globals()[xmlEle.tag].validate(xmlEle, dataElement)
                if not result:
                        return False, dataElement.name + ': ' + msg
        return True, None