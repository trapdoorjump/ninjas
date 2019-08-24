import pyglet
from pyglet.window import key
import textures
import abilities
import attackTypes
import math
import collision

class Ninja:
    def __init__(self, mainBatch, positionX, positionY):
        self.texture = textures.texture_load('sprites/ninja-red.png', 1, 2, 100, 100, 0.5, True)
        self.sprite = pyglet.sprite.Sprite(self.texture, x=positionX, y=positionY, batch=mainBatch)
        self.name = 'ninja'

        self.attackSpeed = 0.3
        self.health = 20
        self.energy = 10 
        self.armor = 10
        
        self.angle = 0
        self.moveX = positionX
        self.moveY = positionY
        self.movementSpeed = 200
        self.moving = False

        self.skillQ = abilities.Shuriken(mainBatch, self.sprite)
        self.skillW = None
        self.skillE = None
        self.skillR = None

        self.attack = attackTypes.Slash(mainBatch, self.sprite)  

    def __del__(self):
        self.sprite.delete()

    def on_mouse_press(self, x, y, button, modifiers):
        
        if (button == 4):  
            degress = math.degrees(math.atan2(y - self.sprite.y, x - self.sprite.x))

            if degress < 0:
                degress += 360

            self.angle = degress
            self.moveX = x
            self.moveY = y
            
            self.moving = True

        if (button == 1):  
            self.moving = self.attack.cast(x, y)   
            if (self.moving == False):
                self.moveX = self.sprite.x
                self.moveY = self.sprite.y     

    def on_key_press(self, symbol, modifiers, mouseX, mouseY):
        if symbol == key.Q:
            self.moving = self.skillQ.cast(mouseX, mouseY)
    
    def update(self, dt, units):

        self.skillQ.loop(dt)
        self.attack.loop(dt)

        if self.moving == True:    
            if not (collision.collision(self.sprite, self.angle, units)):
                movementX = self.movementSpeed
                movementY = self.movementSpeed

                diferenceX = self.moveX - self.sprite.x
                diferenceY = self.moveY - self.sprite.y

                if diferenceX < 0:
                    diferenceX = diferenceX * -1
                if diferenceY < 0:
                    diferenceY = diferenceY * -1

                if diferenceX > diferenceY:
                    movementY = movementY * (diferenceY/diferenceX)
                elif diferenceX < diferenceY:
                    movementX = movementX * (diferenceX/diferenceY)

                if self.sprite.x > self.moveX:
                    self.sprite.x -= movementX * dt   
                if self.sprite.x < self.moveX:
                    self.sprite.x += movementX * dt  

                if self.sprite.y > self.moveY:
                    self.sprite.y -= movementY * dt   
                if self.sprite.y < self.moveY:
                    self.sprite.y += movementY * dt 

                if self.sprite.y == self.moveY and self.sprite.x == self.moveX:
                    self.moving = False
            else:
                self.moving = False
    
