import pyglet
import math
import textures

class ShurikenMissile():
    def __init__(self, player, sprite, speed):
        self.moveX = 0
        self.moveY = 0
        self.range = 0
        self.moveTypeX = 0
        self.moveTypeY = 0
        self.sprite = sprite
        self.player = player
        self.activated = False
        self.speedX = 0
        self.speedY = 0

    def __del__(self):
        self.activated = False
        self.sprite.delete()



class Shuriken():
    def __init__(self, batch, key, player):
        self.batch = batch
        self.key = key
        self.player = player
        self.id = 0
        self.name = 'shuriken'
        self.cooldownTime = 0
        self.cooldown = 0.1
        self.rangeMax = 400
        self.speed = 450
       
        self.sound = pyglet.media.load('res/sounds/shuriken.wav', streaming=False) 
        self.texture = textures.texture_load('sprites/ninja-shuriken-25x.png', 1, 4, 25, 25, 0.02, True)
        self.list = []

        
    def cast(self, x, y, moving):
        if (self.cooldownTime >= self.cooldown):
            self.cooldownTime = 0
            moving = False

            sprite = pyglet.sprite.Sprite(self.texture, self.player.x + 50, self.player.y + 50, batch=self.batch)
            
            object = ShurikenMissile(self.player, sprite, self.speed)
            self.list.append(object)

            object.speedX = self.speed
            object.speedY = self.speed

            diferenceX = x - object.sprite.x
            diferenceY = y - object.sprite.y

            if diferenceX < 0:
                diferenceX = diferenceX * -1
            if diferenceY < 0:
                diferenceY = diferenceY * -1

            if diferenceX > diferenceY:
                object.speedY = object.speedY * (diferenceY/diferenceX)
            elif diferenceX < diferenceY:
                object.speedX = object.speedX * (diferenceX/diferenceY)
            
            if (object.sprite.x < x):
                object.moveTypeX = 0
            if (object.sprite.x > x):
                object.moveTypeX = 1

            if (object.sprite.y < y):
                object.moveTypeY = 0
            if (object.sprite.y > y):
                object.moveTypeY = 1      

            self.sound.play()
            object.activated = True
        
    def loop(self, dt):
        for object in self.list:
            if (object.activated == True):

                if object.moveTypeX == 1:
                    object.sprite.x -= object.speedX * dt      
                else:
                    object.sprite.x += object.speedX * dt  
                
                if object.moveTypeY == 1:
                    object.sprite.y -= object.speedY * dt 
                else:
                    object.sprite.y += object.speedY * dt 

                distanceX = (object.speedX * dt)
                distanceY = (object.speedY * dt)

                object.range += math.sqrt( ( distanceY * distanceY ) + ( distanceX  * distanceX ) )

                if (object.range >= self.rangeMax):
                    self.list.remove(object)
                    del object
            
        self.cooldownTime += dt 





