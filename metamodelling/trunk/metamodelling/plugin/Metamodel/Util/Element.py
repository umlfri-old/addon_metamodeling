from lib.config import config
from Connection import Connection
from DrawingContext import DrawingContext
from VisibleObject import VisibleObject
import weakref

class Element(VisibleObject):
    def __init__(self, obj, isLoad = False):
        VisibleObject.__init__(self)
        self.isLoad = isLoad
        self.object = obj
        self.squares = []
    

    def Paint(self, canvas, delta = (0, 0)):
        self.object.Paint(DrawingContext(canvas, self, (self.position[0]+ delta[0], self.position[1]+ delta[1]), self.GetSize(canvas)))

            
    def GetSizeRelative(self):
        return self.deltaSize
        
    def SetSizeRelative(self, relatSize):
        self.deltaSize = relatSize
    
    def GetResizedRect(self, canvas, delta, mult):
        pos = list(self.GetPosition())
        size = list(self.GetSize(canvas))
        minsize = self.GetMinimalSize(canvas)
        
        for i in (0, 1):
            if mult[i] < 0:
                if delta[i] > size[i] - minsize[i]:
                    pos[i] += size[i] - minsize[i]
                    size[i] = minsize[i]
                else:
                    pos[i] += delta[i]
                    size[i] -= delta[i]
            else:
                size[i] = max(minsize[i], size[i] + mult[i] * delta[i])
                
        return pos, size
        
    def CopyFromElement(self, element):
        self.deltaSize = element.deltaSize
        self.position = element.position
    
    def GetObject(self):
        return self.object
