import pygame
from . import Drawable

class Enemy(Drawable):
    def __init__(self, position):
        super().__init__(position, "hat.png")
    
    def handleEvent(self, event):
        pass
    
    def update(self, seconds):
        super().update(seconds)
    
    def draw(self, drawSurface):
        super().draw(drawSurface)
