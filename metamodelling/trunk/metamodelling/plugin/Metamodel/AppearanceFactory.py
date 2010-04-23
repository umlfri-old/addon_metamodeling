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
    def __init__(self):
        self.attribs = dict()
    
    def GetAttributes(self):
        return self.attribs
    
    def GetAttributesKeySet(self):
        return self.attribs.keys()
    
    def SetAttribute(self,name,value):
        self.attribs[name]=value
    
    def Identity(self):
        return "BaseElement"    
    
class Align(BaseElement):
    def __init__(self):
        BaseElement.__init__(self)
        self.attribs["align"]=""
    def Identity(self):
        return "Align"     

class Condition(BaseElement):
    def __init__(self):
        BaseElement.__init__(self)
        self.attribs["condition"]="True"
    def Identity(self):
        return "Condition" 
        
class Default(BaseElement):
    def __init__(self):
        BaseElement.__init__(self)
        self.attribs["textfont"]=""
        self.attribs["textcolor"]=""
        
    def Identity(self):
        return "Default" 
        
class Diamond(BaseElement):
    def __init__(self):
        BaseElement.__init__(self)
        self.attribs["fill"]=""
        self.attribs["border"]="black"
        
    def Identity(self):
        return "Diamond" 

class Ellipse(BaseElement):
    def __init__(self):
        BaseElement.__init__(self)
        self.attribs["fill"]=""
        self.attribs["border"]="black" 
        
    def Identity(self):
        return "Ellipse" 
        
class HBox(BaseElement):
    def __init__(self):
        BaseElement.__init__(self)
        self.attribs["expand"]=""
        
    def Identity(self):
        return "HBox" 

class Icon(BaseElement):
    def __init__(self):
        BaseElement.__init__(self)
        self.attribs["filename"]=""
    
    def Identity(self):
        return "Icon" 

class Line(BaseElement):
    def __init__(self):
        BaseElement.__init__(self)
        self.attribs["type"]="auto"
        self.attribs["color"]="black"  
        
    def Identity(self):
        return "Line"   

class Loop(BaseElement):
    def __init__(self):
        BaseElement.__init__(self)
        self.attribs["collection"]="None"
    
    def Identity(self):
        return "Loop" 
        
class Padding(BaseElement):
    def __init__(self):
        BaseElement.__init__(self)
        self.attribs["padding"]=0
        
    def Identity(self):
        return "Padding" 

class Proportional(BaseElement):
    def __init__(self):
        BaseElement.__init__(self)
        self.attribs["ratio"]=""
        self.attribs["align"]=""
        self.attribs["size"]="maximal"
        
    def Identity(self):
        return "Proportional" 

class Rectangle(BaseElement):
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
    def __init__(self):
        BaseElement.__init__(self)
        self.attribs["padding"]=5
        self.attribs["color"]="black"
        
    def Identity(self):
        return "Shadow" 

class Sizer(BaseElement):
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
    def __init__(self):
        BaseElement.__init__(self)
        self.attribs["width"]=0
        self.attribs["height"]=0
        self.attribs["scale"]=""
        
    def Identity(self):
        return "Svg" 

class Switch(BaseElement):
    def __init__(self):
        BaseElement.__init__(self)
        self.attribs["value"]="None"

    def Identity(self):
        return "Switch" 

class TextBox(BaseElement):
    def __init__(self):
        BaseElement.__init__(self)
        self.attribs["text"]="some text"
        #self.attribs["linestart"]=""
        self.attribs["color"]="black"
        self.attribs["font"]="Arial 10"
        
    def Identity(self):
        return "TextBox" 

class VBox(BaseElement):
    def __init__(self):
        BaseElement.__init__(self)
        self.attribs["expand"]=""
        
    def Identity(self):
        return "VBox" 
    
class ConnectionArrow(BaseElement):
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
    def __init__(self):
        BaseElement.__init__(self)
        self.attribs["color"]="black"
        self.attribs["style"]=""
        self.attribs["width"]=""
        
    def Identity(self):
        return "ConnectionLine"  
    
class Label(BaseElement):
    def __init__(self):
        BaseElement.__init__(self) 
        self.attribs["position"]="center"
        
    def Identity(self):
        return "Label"   
    
class Case(BaseElement):
    def __init__(self):
        BaseElement.__init__(self)
        self.attribs["type"]="equal"
        self.attribs["negate"]="False"
        self.attribs["condition"]=""  
        
    def Identity(self):
        return "Case"  
    
class G(BaseElement):
    def __init__(self):
        BaseElement.__init__(self)
        self.attribs["id"]=""
        self.attribs["style"]=""
        self.attribs["transform"]=""  
        
    def Identity(self):
        return "g"     
    
class Path(BaseElement):
    def __init__(self):
        BaseElement.__init__(self)
        self.attribs["id"]=""
        self.attribs["d"]=""
        self.attribs["style"]=""
        self.attribs["transform"]=""  
        
    def Identity(self):
        return "path"            

class AppearanceFactory(object):
          
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