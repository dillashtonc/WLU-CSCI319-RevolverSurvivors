from . import AbstractGameFSM
from utils import vec, magnitude, EPSILON, scale, RESOLUTION, UPSCALED
from utils.enemyManager import EnemyManager

from statemachine import State

class MovementFSM(AbstractGameFSM):
    
    def __init__(self, obj):
        super().__init__(obj)
    
    def update(self, seconds):
        super().update(seconds)

class AutoWalkFSM(AbstractGameFSM):
    """AutoWalk FSM makes the gunslinger automatically move away from the nearest enemy."""
    finding_loc = State(initial=True) # new state for finding location
    walking = State()
    stopping = State()

    find_loc = finding_loc.to(walking)
    walk = walking.to.itself() | stopping.to(walking)
    stop = walking.to(stopping) | stopping.to.itself()
    
    def __init__(self, obj):
        super().__init__(obj)
        self.max_distance = 50  # Maximum distance the gunslinger can walk away from enemies
        self.enemy_manager = EnemyManager() # get instance here

    def update(self, seconds):
        super().update(seconds)

        if self == "finding_loc":
            print("finding")
            # get enemy list
            enemies = self.enemy_manager.get_enemies()
    
            # Detect the nearest enemy
            nearest_enemy = self.find_nearest_enemy(enemies)
            print(self.enemy_manager.get_enemies())
            print(nearest_enemy)

            if nearest_enemy is not None:
                # calculate direction away from nearest enemy
                direction_away = self.obj.position - nearest_enemy.position

                # limit movement distance
                if magnitude(direction_away) > self.max_distance:
                    direction_away = scale(direction_away, self.max_distance)

                # update gunslinger's target position
                self.obj.target_position = self.obj.velocity + direction_away

                # transition to walking
                self.transition.to(walking)

        elif self == "walking":
            print("walking")
            # Move towards the target position
            distance = magnitude(self.obj.target_position - self.obj.position)
            if distance > 1:  # Adjust as needed
                # Update gunslinger's velocity to move towards the target position
                direction_to_target = normalize(self.obj.target_position - self.obj.position)
                self.obj.velocity += direction_to_target * self.obj.speed
            else:
                # Arrived at the target position, transition to the stopping state
                self.transition.to(stopping)
                print("stopping")

    def find_nearest_enemy(self, enemies):
        """Find the nearest enemy"""
        nearest_enemy = None
        min_distance = float('inf')

        for enemy in enemies:
            distance = magnitude(enemy.position - self.obj.position)
            if distance < min_distance:
                min_distance = distance
                nearest_enemy = enemy

        return nearest_enemy


class SteadyFSM(MovementFSM):
    """Steady FSM allows the gunslinger to move without gradual stopping."""
    not_moving = State(initial=True)
    negative = State()
    positive = State()
    stalemate = State()
    
    decrease = not_moving.to(negative) | positive.to(stalemate) | negative.to.itself(internal=True) | stalemate.to.itself(internal=True)
    increase = not_moving.to(positive) | negative.to(stalemate) | positive.to.itself(internal=True) | stalemate.to.itself(internal=True)
    stop_decrease = negative.to(not_moving) | positive.to(stalemate) | stalemate.to(positive) | not_moving.to.itself(internal=True)
    stop_increase = negative.to(stalemate) | positive.to(not_moving) | stalemate.to(negative) | not_moving.to.itself(internal=True)
    stop_all = not_moving.to.itself(internal=True) | negative.to(not_moving) | positive.to(not_moving) | stalemate.to(not_moving)
    
    def __init__(self, obj, axis=0):
        self.axis = axis
        self.direction = vec(0, 0)
        self.direction[self.axis] = 1
        
        super().__init__(obj)
    
    def update(self, seconds=0):

        # Boundary checking
        world_size = vec(*UPSCALED)
        if self.obj.position[self.axis] < 0:
            self.stop_decrease()
            self.obj.position[self.axis] = 0
            # add that line below
            self.obj.velocity[self.axis] = max(0, self.obj.velocity[self.axis])
        elif self.obj.position[self.axis] > (world_size[self.axis] - 16):
            self.stop_increase()
            self.obj.velocity[self.axis] = min(0, self.obj.velocity[self.axis])

        if self == "negative":
            self.obj.velocity[self.axis] -= 200 * seconds

            if self.axis == 0:
                self.obj.flipImage[0] = True
            
        elif self == "positive":
            self.obj.velocity[self.axis] += 200 * seconds

            if self.axis == 0:
                self.obj.flipImage[0] = False
            
        elif self == "stalemate":
            self.obj.velocity[self.axis] = 0
        else:
            self.obj.velocity[self.axis] = 0

        super().update(seconds)

class AccelerationFSM(MovementFSM):
    """Axis-based acceleration with gradual stopping."""
    not_moving = State(initial=True)
    
    negative = State()
    positive = State()
    
    stalemate = State()
    
    decrease = not_moving.to(negative) | positive.to(stalemate) | \
                negative.to.itself(internal=True) | stalemate.to.itself(internal=True)
    
    increase = not_moving.to(positive) | negative.to(stalemate) | \
                positive.to.itself(internal=True) | stalemate.to.itself(internal=True)

    stop_decrease = negative.to(not_moving) | positive.to(stalemate) | \
                    stalemate.to(positive) | not_moving.to.itself(internal=True)
    
    stop_increase = negative.to(stalemate) | positive.to(not_moving) | \
                    stalemate.to(negative) | not_moving.to.itself(internal=True)
    
    stop_all      = not_moving.to.itself(internal=True) | negative.to(not_moving) | \
                    positive.to(not_moving) | stalemate.to(not_moving)
    
    def __init__(self, obj, axis=0):
        self.axis      = axis
        self.direction = vec(0,0)
        self.direction[self.axis] = 1
        self.accel = 200
        
        super().__init__(obj)

    def update(self, seconds=0):

        # get the world size from UPSCALED
        worldSize = vec(*UPSCALED)

        # left and up boundaries
        if self.obj.position[self.axis] < 0:
            self.stop_decrease()
            self.obj.velocity[self.axis] = max(0, self.obj.velocity[self.axis])

        # right and down boundaries
        if self.obj.position[self.axis] > (worldSize[self.axis]-16):
            self.stop_increase()
            self.obj.velocity[self.axis] = min(0, self.obj.velocity[self.axis])

        if self == "positive":
            self.obj.velocity += self.direction * self.accel * seconds
        elif self == "negative":
            self.obj.velocity -= self.direction * self.accel * seconds
                
        elif self == "stalemate":
            pass
        else:
            if self.obj.velocity[self.axis] > self.accel * seconds:
                self.obj.velocity[self.axis] -= self.accel * seconds
            elif self.obj.velocity[self.axis] < -self.accel * seconds:
                self.obj.velocity[self.axis] += self.accel * seconds
            else:
                self.obj.velocity[self.axis] = 0
        
        
    
        super().update(seconds)
