class EnemyManager:

# change to singleton, use getInstance
    
    def __init__(self):
        self.enemies = []

    #@staticmethod
    def add_enemy(self, enemy):
        self.enemies.append(enemy)

    #@staticmethod
    def get_enemies(self):
        return self.enemies

# may need to add singleton logic
