# based on Kirby. changes explained in comments. ## denotes a to-do

from . import Mobile
## # removed Acceleration, will need to add new FSMs
from FSMs import WalkingFSM, SteadyFSM, AutoWalkFSM
from utils import vec, RESOLUTION, SpriteManager
from . import Drawable

from pygame.locals import *

import pygame
import numpy as np

class Gunslinger(Mobile):
   GUN_ROTATION_SPEED_VERTICAL = 10.0
   GUN_ROTATION_SPEED_HORIZONTAL = 10.0

   def __init__(self, position):
##      # change the 8 value below to half the sprite's size to center sprite
      startPos = vec(RESOLUTION[0] / 2 - 15, RESOLUTION[1] / 2 - 19)
      super().__init__(startPos, "Gunslinger3.png")

##      # This code is potetially good reference for the guns
##      self.hatOffset = vec(-3,-6)
##      self.hat = Drawable(position, "hat.png")
##      self.hat.image = pygame.transform.flip(self.hat.image, True, False)

      # Gun attributes
      self.gun = Drawable(position=self.position, fileName="hat.png")
      self.gun_offset_x = 40  # Adjust as needed 55
      self.gun_offset_y = 20  # Adjust as needed 30
      
        
##    # Animation variables specific to Gunslinger
      self.framesPerSecond = 2 
      self.nFrames = 2
      
      self.nFramesList = {
         "moving"   : 4,
         "standing" : 4
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

      if event.type == JOYAXISMOTION:

         # aiming

         if event.axis == 2 or event.axis == 3:  # Vertical or Horizontal movement
            # Calculate the angle between the neutral position and the current position of the analog stick
            vertical_axis_value = pygame.joystick.Joystick(event.joy).get_axis(3)
            horizontal_axis_value = pygame.joystick.Joystick(event.joy).get_axis(2)
            angle = np.arctan2(-vertical_axis_value, horizontal_axis_value)
            self.gun.angle = np.degrees(angle)

         # old aiming code
##         if event.axis == 3:  # Vertical movement
##       # Calculate the angle between the neutral position and the current position of the analog stick
##            vertical_angle = np.arctan2(event.value, 1.0)
##            self.gun.angle = np.degrees(vertical_angle)
##                
##         elif event.axis == 2:  # Horizontal movement
##    # Calculate the angle between the neutral position and the current position of the analog stick
##            horizontal_angle = np.arctan2(event.value, 1.0)
##            self.gun.angle = np.degrees(horizontal_angle)


         
##         if event.axis == 2:  # Vertical movement
##                # Adjust gun angle based on joystick input
##                self.gun.angle += event.value * self.GUN_ROTATION_SPEED_VERTICAL
##                
##         elif event.axis == 3:  # Horizontal movement
##                # Adjust gun angle based on joystick input
##                self.gun.angle += event.value * self.GUN_ROTATION_SPEED_HORIZONTAL

         # movement
         
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

      gun_offset = vec(self.gun_offset_x, self.gun_offset_y)
      rotated_offset = self.rotateVector(gun_offset, self.gun.angle)
      self.gun.position = self.position + rotated_offset

   def draw(self, drawSurface):
      super().draw(drawSurface)
      self.gun.draw(drawSurface)

   # new function for rotation

   def rotateVector(self, vector, angle):
        rad_angle = np.radians(-angle)
        rotation_matrix = np.array([[np.cos(rad_angle), -np.sin(rad_angle)],
                                    [np.sin(rad_angle), np.cos(rad_angle)]])
        return rotation_matrix @ vector   

   def updateMovement(self):
      pass
   
   
 



      
