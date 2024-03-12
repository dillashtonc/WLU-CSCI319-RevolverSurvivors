from . import Mobile
from FSMs import WalkingFSM, AccelerationFSM, SteadyFSM, AutoWalkFSM
from utils import vec, RESOLUTION, SpriteManager, UPSCALED
from . import Drawable

from pygame.locals import *

import pygame
import numpy as np


class Kirby(Mobile):
   def __init__(self, position):
      startPos = vec(UPSCALED[0] / 2 - 8, UPSCALED[1] / 2 - 8)
      super().__init__(startPos, "kirby.png")

      # This code is potentially good reference for the guns
      self.hatOffset = vec(-3,-6)
      self.hat = Drawable(position, "hat.png")
      self.hat.image = pygame.transform.flip(self.hat.image, True, False)
        
      # Animation variables specific to Kirby

      self.framesPerSecond = 2 
      self.nFrames = 2
      
      self.nFramesList = {
         "moving"   : 4,
         "standing" : 2
      }
      
      self.rowList = {
         "moving"   : 1,
         "standing" : 0
      }
      
      self.framesPerSecondList = {
         "moving"   : 8,
         "standing" : 2
      }
            
      self.FSManimated = WalkingFSM(self)
      
      self.LR = SteadyFSM(self, axis=0)
      self.UD = SteadyFSM(self, axis=1)
      self.steadyFSM = SteadyFSM(self)
      self.autowalkFSM = AutoWalkFSM(self)
      self.currentFSM = self.steadyFSM
      
   def handleEvent(self, event):

##      Controller layout
##      Left joystick: UD: Axis 1 LR: Axis 0
##      Right joystick: UD: Axis 2 LR: Axis 3
##      A (interact / pickup): button 1
##      L shoulder: button 4
##      R shoulder: button 5

      # movement
      if event.type == JOYAXISMOTION:
         # up
         if event.axis == 1 and event.value < -0.1:
            self.UD.stop_increase()
            self.UD.decrease()

         # down
         elif event.axis == 1 and event.value > 0.1:
            self.UD.stop_decrease()
            self.UD.increase()

         elif event.axis == 1:
            self.UD.stop_all()

         # left
         elif event.axis == 0 and event.value < -0.1:
            self.LR.stop_increase()
            self.LR.decrease()

         # right
         elif event.axis == 0 and event.value > 0.1:
            self.LR.stop_decrease()
            self.LR.increase()

         elif event.axis == 0:
            self.LR.stop_all()

      if event.type == JOYBUTTONDOWN:
        # cycle between Steady and AutoWalk FSMs using right shoulder button
        if event.button == 5:
            self.toggleFSM()

      # keyboard controls
      if event.type == KEYDOWN:
         if event.key == K_UP:
            self.UD.decrease()
             
         elif event.key == K_DOWN:
            self.UD.increase()
            
         elif event.key == K_LEFT:
            self.LR.decrease()
            
         elif event.key == K_RIGHT:
            self.LR.increase()
            
      elif event.type == KEYUP:
         if event.key == K_UP:
            self.UD.stop_decrease()
             
         elif event.key == K_DOWN:
            self.UD.stop_increase()
             
            
         elif event.key == K_LEFT:
            self.LR.stop_decrease()
            
         elif event.key == K_RIGHT:
            self.LR.stop_increase()

   def toggleFSM(self):
    # switch between Steady and AutoWalk FSMs
      if self.currentFSM == self.steadyFSM:
         self.currentFSM = self.autowalkFSM
         print("switching to auto")
      else:
         self.currentFSM = self.steadyFSM
         print("switching to steady")
   
   def update(self, seconds): 
      self.currentFSM.update(seconds)
      self.LR.update(seconds)
      self.UD.update(seconds)

      super().update(seconds)

      self.hat.position = self.hatOffset + self.position

   def draw(self, drawSurface):
      super().draw(drawSurface)
      self.hat.draw(drawSurface)

   def updateMovement(self):
      pass
   
   
  
