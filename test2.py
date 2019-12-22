class EnemyEvent:
    def __init__(self, tick, enemy_class, x, y):
        self.enemy = enemy_class
        self.x = x
        self.y = y

class T:
    def __init__(self):
        print(1)


a=EnemyEvent(0,T,0,0)