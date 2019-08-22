import pyglet

class Unit:
    def __init__(self, sprite, name, x, y, angle):
        self.model = sprite
        self.name = name
        self.model.x = x
        self.model.y = y
        self.angle = angle