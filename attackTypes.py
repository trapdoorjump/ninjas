import pyglet
import math
import textures
import abilities

class Slash():
    def __init__(self, batch, player):
        self.batch = batch
        self.player = player
        self.id = 0
        self.name = 'slash'
        self.cooldownTime = 0
        self.cooldown = 0.3
        self.rangeMax = 100
        self.speed = 500
       
        self.sound = pyglet.media.load('sounds/slash.wav', streaming=False) 
        self.texture = pyglet.image.load('sprites/slash.png')
        self.list = []

        
    def cast(self, x, y):
        if (self.cooldownTime >= self.cooldown):
            self.cooldownTime = 0

            sprite = pyglet.sprite.Sprite(self.texture, self.player.x, self.player.y + 20, batch=self.batch)
            
            object = abilities.Missile(self.player, sprite, self.speed)
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
            return False
        else:
            return True
        
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



