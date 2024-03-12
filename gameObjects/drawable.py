from utils import SpriteManager, SCALE, RESOLUTION, vec

import pygame

class Drawable(object):
    
    CAMERA_OFFSET = vec(0,0)
    
    @classmethod
    def updateOffset(cls, trackingObject, worldSize):
        
        objSize = trackingObject.getSize()
        objPos = trackingObject.position
        
        offset = objPos + (objSize // 2) - (RESOLUTION // 2)
        
        for i in range(2):
            offset[i] = int(max(0,
                                min(offset[i],
                                    worldSize[i] - RESOLUTION[i])))
        
        cls.CAMERA_OFFSET = offset
        
        

    @classmethod    
    def translateMousePosition(cls, mousePos):
        newPos = vec(*mousePos)
        newPos /= SCALE
        newPos += cls.CAMERA_OFFSET
        
        return newPos
    
    def __init__(self, position=vec(0,0), fileName="", offset=None):
        if fileName != "":
            self.original = SpriteManager.getInstance().getSprite(fileName, offset)
            self.image = self.original.copy()
        
        self.position  = vec(*position)
        self.imageName = fileName
        self.rotate = False
        self.angle = 0

    def setDrawPosition(self):
        if self.rotate:
            self.image = pygame.transform.rotate(self.original, self.angle)
            center = vec(*self.original.get_rect().center)
            rotatedCenter = vec(*self.image.get_rect().center)
            self.drawPosition = self.position - center - rotatedCenter

        else:
            self.drawPosition = self.position
    
    def draw(self, drawSurface):
        self.setDrawPosition()
        drawSurface.blit(self.image, list(map(int, self.drawPosition)))
            
    def getSize(self):
        return vec(*self.image.get_size())
    
    def handleEvent(self, event):
        pass
    
    def update(self, seconds):
        pass
    
    
    def getCollisionRect(self):
        newRect =  self.image.get_rect()
        newRect.left = int(self.position[0])
        newRect.top = int(self.position[1])
        return newRect
    
    def doesCollide(self, other):
        return self.getCollisionRect().colliderect(other.getCollisionRect())   
    
    def doesCollideList(self, others):
        rects = [r.getCollisionRect() for r in others]
        return self.getCollisionRect().collidelist(rects)   
