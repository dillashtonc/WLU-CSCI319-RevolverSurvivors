# based on Kirby. changes explained in comments. ## denotes a to-do

from . import Mobile
## # removed Acceleration, will need to add new FSMs
from FSMs import WalkingFSM, SteadyFSM, AutoWalkFSM
from utils import vec, RESOLUTION, SpriteManager
from . import Drawable, Animated

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

      # Gun attributes
      #self.gun = Drawable(position=self.position, fileName="hat.png")
      self.gun = Animated(position=self.position, fileName="gunsheet.png")
      self.gun_offset_x = 40  # Adjust as needed 55
      self.gun_offset_y = 20  # Adjust as needed 30
      self.current_quadrant = "lower left"
      self.flip = False
      
        
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
      self.steadyFSMX = SteadyFSM(self)
      self.steadyFSMY = SteadyFSM(self, axis = 1)
      self.autowalkFSM = AutoWalkFSM(self)
      self.currentFSMX = self.steadyFSMX
      self.currentFSMY = self.steadyFSMY
      self.auto = False
      
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

         # movement
         # note: removed lines like self.currentFSMY.stop_increase() to prevent halting
         # behavior
         
         # up
         if event.axis == 1 and event.value < -0.1:
            self.currentFSMY.decrease()

         # down
         elif event.axis == 1 and event.value > 0.1:
            self.currentFSMY.increase()

         elif event.axis == 1:
            self.currentFSMY.stop_all()

         # left
         elif event.axis == 0 and event.value < -0.1:
            self.currentFSMX.decrease()

         # right
         elif event.axis == 0 and event.value > 0.1:
            self.currentFSMX.increase()

         elif event.axis == 0:
            self.currentFSMX.stop_all()

      if event.type == JOYBUTTONDOWN:
        # cycle between Steady and AutoWalk FSMs using right shoulder button
        if event.button == 5:
            self.toggleFSM()

      # keyboard controls
      if event.type == KEYDOWN:
         if event.key == K_UP:
            self.currentFSMY.decrease()
             
         elif event.key == K_DOWN:
            self.currentFSMY.increase()
            
         elif event.key == K_LEFT:
            self.currentFSMX.decrease()
            
         elif event.key == K_RIGHT:
            self.currentFSMX.increase()
            
      elif event.type == KEYUP:
         if event.key == K_UP:
            self.currentFSMY.stop_decrease()
             
         elif event.key == K_DOWN:
            self.currentFSMY.stop_increase()
             
            
         elif event.key == K_LEFT:
            self.currentFSMX.stop_decrease()
            
         elif event.key == K_RIGHT:
            self.currentFSMX.stop_increase()

   def toggleFSM(self):
    # switch between Steady and AutoWalk FSMs
      if self.auto == False:
         self.auto = True
         print("switching to auto")
      else:
         self.auto = False
         print("switching to steady")
   
   def update(self, seconds): 
      # get rid of LR and UD
      if self.auto == False:
         self.currentFSMX.update(seconds)
         self.currentFSMY.update(seconds)
      else:
         self.autowalkFSM.update(seconds)
      #self.LR.update(seconds)
      #self.UD.update(seconds)

      super().update(seconds)

      gun_offset = vec(self.gun_offset_x, self.gun_offset_y)
      rotated_offset = self.rotateVector(gun_offset, self.gun.angle)
      self.gun.position = self.position + rotated_offset

      # Determine the quadrant based on gun position
      if self.gun.position[0] < self.position[0]:
         if self.gun.position[1] < self.position[1]:
            quadrant = "upper left"
            self.gun.row = 1
            if self.flip == True:
               self.gun.image = pygame.transform.flip(self.gun.image, True, False)
               self.flip = False
         else:
            quadrant = "lower left"
            self.gun.row = 0
            if self.flip == True:
               self.gun.image = pygame.transform.flip(self.gun.image, True, False)
               self.flip = False
      else:
         if self.gun.position[1] < self.position[1]:
            quadrant = "upper right"
            print("switch row")
            self.gun.row = 1
            if self.flip == False:
               self.gun.image = pygame.transform.flip(self.gun.image, True, False)
               self.flip = True
         else:
            quadrant = "lower right"
            self.gun.row = 0
            if self.flip == False:
               self.gun.image = pygame.transform.flip(self.gun.image, True, False)
               self.flip = True

      # Print a message when the gun enters a new quadrant
      if quadrant != self.current_quadrant:
         print("Gun entered", quadrant, "quadrant")
         self.current_quadrant = quadrant


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
   
   
 



      
