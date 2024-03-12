import pygame
import random
from pygame.locals import USEREVENT
from . import Drawable, Gunslinger, Enemy
from utils import vec, normalize, RESOLUTION, UPSCALED
from utils.enemyManager import EnemyManager

import numpy as np

class GameEngine(object):
    import pygame

    def __init__(self):       
        self.gunslinger = Gunslinger((0,0))
        self.size = vec(*UPSCALED)
        self.background = Drawable((0,0), "background.png")
        self.enemy_manager = EnemyManager()

        # enemy timer
        self.enemySpawnTimer = pygame.time.set_timer(USEREVENT + 1, 5000)
    
    def draw(self, drawSurface):        
        self.background.draw(drawSurface)
        
        self.gunslinger.draw(drawSurface)

        for enemy in self.enemy_manager.get_enemies():
            enemy.draw(drawSurface)
            
    def handleEvent(self, event):
        self.gunslinger.handleEvent(event)

        if event.type == USEREVENT + 1:
            self.spawnEnemy()
    
    def update(self, seconds):
        self.gunslinger.update(seconds)

        for enemy in self.enemy_manager.get_enemies():
            enemy.update(seconds)
        
        Drawable.updateOffset(self.gunslinger, self.size)

    def spawnEnemy(self):
        gunslingerPos = self.gunslinger.position
        screenWidth = RESOLUTION[0]

        # random angle
        randAngle = np.random.uniform(0, 2 * np.pi)

        # random vector
        randVecX = np.cos(randAngle)
        randVecY = np.sin(randAngle)
        randVec = normalize(vec(randVecX, randVecY))

        # new enemy position
        newPos = gunslingerPos + randVec * screenWidth

        # spawn enemy and add it to list in enemy manager
        newEnemy = Enemy(newPos)
        self.enemy_manager.add_enemy(newEnemy)
        
        

    # old enemy spawning function
##    def spawnEnemy(self):
##        gunslingerPos = self.gunslinger.position
##        screenWidth = RESOLUTION[0]
##
##        # distance function
##        def distance(p1, p2):
##            return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5
##
##        positions = [(x,y) for x in range(int(UPSCALED[0])) for y in range(int(UPSCALED[1])) if distance((x,y), gunslingerPos) > screenWidth]
##
##        enemyPosition = random.choice(positions)
##
##        newEnemy = Enemy(enemyPosition)
##        self.enemy_manager.add_enemy(newEnemy)


        
