from FSMs import ScreenManagerFSM
from . import TextEntry, EventMenu
from utils import vec, RESOLUTION
from gameObjects.engine import GameEngine

from pygame.locals import *

class ScreenManager(object):
      
    def __init__(self):
        self.game = GameEngine()
        self.state = ScreenManagerFSM(self)
        self.pausedText = TextEntry(vec(0,0),"Paused")
        
        size = self.pausedText.getSize()
        midpoint = RESOLUTION // 2 - size
        self.pausedText.position = vec(*midpoint)
        
        self.mainMenu = EventMenu("background.png", fontName="default8")

        # controller start game
        self.mainMenu.addOption("start", "Press A or 1 to start Game",
                                 RESOLUTION // 2 - vec(0,50),
                                 lambda x: x.type == JOYBUTTONDOWN and x.button == 1,
                                 center="both")

        # keyboard start game
        self.mainMenu.addOption("start", "Press A or 1 to start Game",
                                 RESOLUTION // 2 - vec(0,50),
                                 lambda x: x.type == KEYDOWN and x.key == K_1,
                                 center="both")
        
        self.mainMenu.addOption("exit", "Press 2 to exit Game",
                                 RESOLUTION // 2 + vec(0,50),
                                 lambda x: x.type == KEYDOWN and x.key == K_2,
                                 center="both")
    
    
    def draw(self, drawSurf):
        if self.state.isInGame():
            self.game.draw(drawSurf)
        
            if self.state == "paused":
                self.pausedText.draw(drawSurf)
        
        elif self.state == "mainMenu":
            self.mainMenu.draw(drawSurf)
    
    def handleEvent(self, event):
        if self.state in ["game", "paused"]:
            if event.type == KEYDOWN and event.key == K_m:
                self.state.quitGame()
            elif event.type == KEYDOWN and event.key == K_p:
                self.state.pause()
                
            else:
                self.game.handleEvent(event)
        elif self.state == "mainMenu":
            choice = self.mainMenu.handleEvent(event)
            
            if choice == "start":
                self.state.startGame()
            elif choice == "exit":
                return "exit"
     
    
    def update(self, seconds):      
        if self.state == "game":
            self.game.update(seconds)
        elif self.state == "mainMenu":
            self.mainMenu.update(seconds)
    
