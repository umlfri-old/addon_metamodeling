'''
Created on 21.3.2010

@author: Michal Kovacik, Factory method design pattern
'''
import pygtk
pygtk.require('2.0')
from __init__ import *

try:
    import gtk
    import gtk.glade
except:
    sys.exit(1)    

class BaseElement(object):
    '''
    base class for inheritance of visual parts like Rectangle and so on
    @ivar attribs: dict of attributes which in latter phase will be converted into XML tag 
    '''
    def __init__(self):
        self.attribs = dict()
    
    def GetAttributes(self):
        '''
        common method for getting attribs
        @return: attribs dictionary
        @rtype: dict
        '''
        return self.attribs
    
    def GetAttributesKeySet(self):
        '''
        common method for getting list of attributes
        @rtype: list
        '''
        return self.attribs.keys()
    
    def SetAttribute(self,name,value):
        '''
        append an attribute with a name and value into list
        '''
        self.attribs[name]=value
    
    def Identity(self):
        '''
        returns its own identity identifier
        @rtype: str
        '''
        return "BaseElement"    
    
class Align(BaseElement):
    '''
    Align is used to align content to center or sides
    '''
    def __init__(self):
        BaseElement.__init__(self)
        self.attribs["align"]=""
    def Identity(self):
        return "Align"     

class Condition(BaseElement):
    '''
    Condition is used to evaluate an expression, if result is True, subcontent is loader, else not
    '''
    def __init__(self):
        BaseElement.__init__(self)
        self.attribs["condition"]="True"
    def Identity(self):
        return "Condition" 
        
class Default(BaseElement):
    '''
    Default is used to set default textfont or textcolor
    '''
    def __init__(self):
        BaseElement.__init__(self)
        self.attribs["textfont"]=""
        self.attribs["textcolor"]=""
        
    def Identity(self):
        return "Default" 
        
class Diamond(BaseElement):
    '''
    Diamond is visual representation of diamond-like element, which can be filled and bordered
    '''
    def __init__(self):
        BaseElement.__init__(self)
        self.attribs["fill"]=""
        self.attribs["border"]="black"
        
    def Identity(self):
        return "Diamond" 

class Ellipse(BaseElement):
    '''
    Diamond is visual representation of ellipse-like element, which can be filled and bordered
    '''
    def __init__(self):
        BaseElement.__init__(self)
        self.attribs["fill"]=""
        self.attribs["border"]="black" 
        
    def Identity(self):
        return "Ellipse" 
        
class HBox(BaseElement):
    '''
    HBox is a container, which can own multiple visual parts under it. HBox organizes child elements into one column
    '''
    def __init__(self):
        BaseElement.__init__(self)
        self.attribs["expand"]=""
        
    def Identity(self):
        return "HBox" 

class Icon(BaseElement):
    '''
    Icon defines a possible additional icon, see Package.xml file for further example
    '''
    def __init__(self):
        BaseElement.__init__(self)
        self.attribs["filename"]=""
    
    def Identity(self):
        return "Icon" 

class Line(BaseElement):
    '''
    Line defines a line, which type could be for instance horizontal, vertical,..
    '''
    def __init__(self):
        BaseElement.__init__(self)
        self.attribs["type"]="auto"
        self.attribs["color"]="black"  
        
    def Identity(self):
        return "Line"   

class Loop(BaseElement):
    '''
    Loop defines an iterable collection through which we can iterate
    '''
    def __init__(self):
        BaseElement.__init__(self)
        self.attribs["collection"]="None"
    
    def Identity(self):
        return "Loop" 
        
class Padding(BaseElement):
    '''
    Padding defines internal intendation
    '''
    def __init__(self):
        BaseElement.__init__(self)
        self.attribs["padding"]=0
        
    def Identity(self):
        return "Padding" 

class Proportional(BaseElement):
    '''
    Proportional is important when defining circle from ellipse by changing ratio in this element
    '''
    def __init__(self):
        BaseElement.__init__(self)
        self.attribs["ratio"]=""
        self.attribs["align"]=""
        self.attribs["size"]="maximal"
        
    def Identity(self):
        return "Proportional" 

class Rectangle(BaseElement):
    '''
    Rectangle is one of most used elements, by Path definition we are able to change corners or sides
    '''
    def __init__(self):
        BaseElement.__init__(self)
        self.attribs["fill"]=""
        self.attribs["border"]="black"
        self.attribs["lefttop"]=""
        self.attribs["righttop"]=""
        self.attribs["leftbottom"]=""
        self.attribs["rightbottom"]=""
        self.attribs["left"]=""
        self.attribs["right"]=""
        self.attribs["top"]=""
        self.attribs["bottom"]=""
        
    def Identity(self):
        return "Rectangle" 

class Shadow(BaseElement):
    '''
    Shadow is being drawed in south-eastern corner of an element. Distance is defined by padding attribute
    '''
    def __init__(self):
        BaseElement.__init__(self)
        self.attribs["padding"]=5
        self.attribs["color"]="black"
        
    def Identity(self):
        return "Shadow" 

class Sizer(BaseElement):
    '''
    Sizer is especially for defining size constraints or default width and height
    '''
    def __init__(self):
        BaseElement.__init__(self)
        self.attribs["minwidth"]=0
        self.attribs["minheight"]=0
        self.attribs["maxwidth"]=10
        self.attribs["maxheight"]=10
        self.attribs["width"]=5
        self.attribs["height"]=5
        
    def Identity(self):
        return "Sizer" 

class Svg(BaseElement):
    '''
    Svg supports a scalable vector graphics extension
    '''
    def __init__(self):
        BaseElement.__init__(self)
        self.attribs["width"]=0
        self.attribs["height"]=0
        self.attribs["scale"]=""
        
    def Identity(self):
        return "Svg" 

class Switch(BaseElement):
    '''
    by using Switch - Case we can switch between different cases of "value" attribute
    '''
    def __init__(self):
        BaseElement.__init__(self)
        self.attribs["value"]="None"

    def Identity(self):
        return "Switch" 

class TextBox(BaseElement):
    '''
    TextBox is a classic text which appears in canvas. This element is also known as a Label-type one
    '''
    def __init__(self):
        BaseElement.__init__(self)
        self.attribs["text"]="some text"
        self.attribs["color"]="black"
        self.attribs["font"]="Arial 10"
        
    def Identity(self):
        return "TextBox" 

class VBox(BaseElement):
    '''
    VBox organizes child elements like HBox, but in one row
    '''
    def __init__(self):
        BaseElement.__init__(self)
        self.attribs["expand"]=""
        
    def Identity(self):
        return "VBox" 
    
class ConnectionArrow(BaseElement):
    '''
    ConnectionArrow is used in Relationship definition only. index values -1 or 0 determines on which side of connection is arrow drawn
    '''
    def __init__(self):
        BaseElement.__init__(self)
        self.attribs["index"]=-1
        self.attribs["direction"]=""
        self.attribs["style"]="simple_arrow" 
        self.attribs["color"]="black"   
        self.attribs["fill"]=""
        self.attribs["size"]="5"
        
    def Identity(self):
        return "ConnectionArrow"
    
class ConnectionLine(BaseElement):
    '''
    ConnectionLine is also used in relationship definition only like in ConnectionArrow case. Defines a connection line between two Objects
    '''
    def __init__(self):
        BaseElement.__init__(self)
        self.attribs["color"]="black"
        self.attribs["style"]=""
        self.attribs["width"]=""
        
    def Identity(self):
        return "ConnectionLine"  
    
class Label(BaseElement):
    '''
    Label is used in relationship definition only and its position is one of center, source, destination (and +/-, i.e. source+1)
    '''
    def __init__(self):
        BaseElement.__init__(self) 
        self.attribs["position"]="center"
        
    def Identity(self):
        return "Label"   
    
class Case(BaseElement):
    '''
    Case is used with Switch in combination
    '''
    def __init__(self):
        BaseElement.__init__(self)
        self.attribs["type"]="equal"
        self.attribs["negate"]="False"
        self.attribs["condition"]=""  
        
    def Identity(self):
        return "Case"  
    
class G(BaseElement):
    '''
    G is subelement of Svg
    '''
    def __init__(self):
        BaseElement.__init__(self)
        self.attribs["id"]=""
        self.attribs["style"]=""
        self.attribs["transform"]=""  
        
    def Identity(self):
        return "g"     
    
class Path(BaseElement):
    '''
    Path is subelement of Svg
    '''
    def __init__(self):
        BaseElement.__init__(self)
        self.attribs["id"]=""
        self.attribs["d"]=""
        self.attribs["style"]=""
        self.attribs["transform"]=""  
        
    def Identity(self):
        return "path"            

class AppearanceFactory(object):
    '''
    AppearanceFactory is a realization of mechanism described in Factory method desing pattern
    It has only one method which returns instance of object, which depends on input string.
    Input string doesnt necessarily match Identity method, but it is recommended
    '''      
    @staticmethod
    def CreateElement(objectType):
        if (objectType=="Align"):
            return Align()
        elif (objectType=="Condition"):
            return Condition()
        elif (objectType=="Default"):
            return Default()
        elif (objectType=="Diamond"):
            return Diamond()
        elif (objectType=="Ellipse"):
            return Ellipse()
        elif (objectType=="HBox"):
            return HBox()
        elif (objectType=="Icon"):
            return Icon()
        elif (objectType=="Line"):
            return Line()
        elif (objectType=="Loop"):
            return Loop()
        elif (objectType=="Padding"):
            return Padding()
        elif (objectType=="Proportional"):
            return Proportional()
        elif (objectType=="Rectangle"):
            return Rectangle()
        elif (objectType=="Shadow"):
            return Shadow()
        elif (objectType=="Sizer"):
            return Sizer()
        elif (objectType=="Svg"):
            return Svg()
        elif (objectType=="Switch"):
            return Switch()
        elif (objectType=="TextBox"):
            return TextBox()
        elif (objectType=="VBox"):
            return VBox()
        elif (objectType=="ConnectionArrow"):
            return ConnectionArrow()
        elif (objectType=="ConnectionLine"):
            return ConnectionLine()
        elif (objectType=="Label"):
            return Label()
        elif (objectType=="Case"):
            return Case()
        elif (objectType=="G"):
            return G()
        elif (objectType=="Path"):
            return Path()
        
if __name__ == '__main__':
    a = AppearanceFactory()