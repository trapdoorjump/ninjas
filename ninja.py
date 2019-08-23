import pyglet
from pyglet.window import key
from pyglet.window import FPSDisplay
from pyglet.window import mouse
from random import randint, choice
import math
import textures
import skillsClass
import abilities

def display_window_preload():
    global window
    window = pyglet.window.Window(width=1200, height=800, caption="goeninjas", resizable=False)
    window.set_location(400, 100)

    global main_batch
    main_batch = pyglet.graphics.Batch()

def texture_load_all():
    global texture_block_50x50
    texture_block_50x50 = pyglet.image.load('sprites/block50x50.png')

    global texture_ninja_blue
    texture_ninja_blue = textures.texture_load('sprites/ninja-gray.png', 1, 2, 100, 100, 0.5, True)

    global texture_shuriken
    texture_shuriken = textures.texture_load('sprites/ninja-shuriken-25x.png', 1, 4, 25, 25, 0.02, True)

    global texture_ninja_gray
    texture_ninja_gray = textures.texture_load('sprites/ninja-blue.png', 1, 2, 100, 100, 0.5, True)

    global texture_slash
    texture_slash = pyglet.image.load('sprites/air_slash_64x.png')

def display_fps_show():
    global window
    global display_fps
    display_fps = FPSDisplay(window)
    display_fps.label.font_size = 10

def display_hud():
    text_hp = pyglet.text.Label("HP", x=1000 , y=650, batch=main_batch)
    text_hp.italic = True
    text_hp.bold = True
    text_hp.font_size = 16

    text_player_hp = pyglet.text.Label(str(5), x=1100, y=600, batch=main_batch)
    text_player_hp.color = (0, 100, 50, 255)
    text_player_hp.font_size = 22

    global text_intro
    text_intro = pyglet.text.Label("Press space to start", x=550 , y=400)
    text_intro.anchor_x = "center"
    text_intro.anchor_y = "center"
    text_intro.italic = True
    text_intro.bold = True
    text_intro.font_size = 40

def overworld_map_spawn():
    global walls
    walls = []

    for index in range(11):
        walls.append(pyglet.sprite.Sprite(texture_block_50x50, x=0, y=150 + index * 50, batch=main_batch)) 
        walls.append(pyglet.sprite.Sprite(texture_block_50x50, x=900, y=150 + index * 50, batch=main_batch)) 
        walls.append(pyglet.sprite.Sprite(texture_block_50x50, x=1150, y=150 + index * 50, batch=main_batch)) 
    for index in range(24):
        walls.append(pyglet.sprite.Sprite(texture_block_50x50, x=index*50, y=100, batch=main_batch)) 
        walls.append(pyglet.sprite.Sprite(texture_block_50x50, x=index*50, y=700, batch=main_batch)) 

def overworld_units_spawn():
    global player
    player = pyglet.sprite.Sprite(texture_ninja_blue, x=200, y=200, batch=main_batch)   

def audio_load():
    global sound_shuriken
    sound_shuriken = pyglet.media.load('res/sounds/shuriken.wav', streaming=False)   

    global sound_slash
    sound_slash = pyglet.media.load('sounds/slash.wav', streaming=False)   

def constants_load():
    global started
    started = False

    global moveX, moveY, moving, player_movespeed
    moveX = 0
    moveY = 0
    moving = False
    player_movespeed = 200

    global mouseX , mouseY, anglePlayer
    mouseX = 0
    mouseY = 0
    anglePlayer = 0

    global fireClick, fire2, player_laser2_list, player_fire_rate
    fireClick = False
    fire2 = False
    
    player_laser2_list = []
    player_fire_rate = 0
    

    skills = []
    skills.append(skillsClass.Skills(key.Q, 1, 'shuriken', 2))

    global abilityQCooldown, abilityQCooldownMax, moveShurikenX, moveShurikenY, shurikenRangeMax, shurikenRange
    abilityQCooldown = 0
    abilityQCooldownMax = 2
    moveShurikenX = 0
    moveShurikenY = 0
    shurikenRangeMax = 400
    shurikenRange = 0
    
    global abilityWCooldown, abilityWCooldownMax, moveSlashX, moveSlashY, slashRangeMax, slashRange, player_slash_list
    abilityWCooldown = 0
    abilityWCooldownMax = 0.5
    moveSlashX = 0
    moveSlashY = 0
    slashRangeMax = 100
    slashRange = 0
    player_slash_list = []

    global skillQ, main_batch, player, sound_shuriken, texture_shuriken
    skillQ = abilities.Shuriken(main_batch, key.Q, player)

def initialization():
    display_window_preload()
    display_fps_show()
    texture_load_all()
    display_hud()
    overworld_map_spawn()
    overworld_units_spawn()
    audio_load()
    constants_load()

############## BEFORE EVENTS ####################
initialization()

@window.event
def on_draw():
    window.clear()
    if started:
        main_batch.draw()
    else:
        text_intro.draw()
    display_fps.draw()

@window.event
def on_mouse_press(x, y, button, modifiers):
    global player, anglePlayer, fire2, fireClick
    degress = math.degrees(math.atan2(y-player.y, x-player.x))
    if degress < 0:
        degress += 360
    anglePlayer = degress
    if (button == 4):
        global moving, moveX, moveY
        moveX = x
        moveY = y
        moving = True
    if (button == 1):
        fireClick = True

@window.event
def on_mouse_release(x, y, button, modifiers):
    pass
    #global fireClick
    #if (button == 1):
    #    fireClick = False

@window.event
def on_mouse_motion(x, y, dx, dy):
    global mouseX, mouseY
    mouseX = x
    mouseY = y

@window.event
def on_key_press(symbol, modifiers):
    global  started, skillQ, mouseX, mouseY, moving

    if symbol == key.SPACE:
        if not started:
            started = True
    if symbol == skillQ.key:
        skillQ.cast(mouseX, mouseY, moving)

@window.event
def on_key_release(symbol, modifiers):
    global fire2
    if symbol == key.Q:
        fire2 = False

def angle(x1, x2, y1, y2):
    angleValue = math.degrees(math.atan2(y1-y2, x1-x2))
    if angleValue < 0:
        angleValue += 360
    return angleValue

def player_shoot2(dt):
    global player_fire_rate, abilityQCooldown, abilityQCooldownMax, moveShurikenX, moveShurikenY, mouseX, mouseY, shurikenRange, player_laser2_list, moving

    if (abilityQCooldown >= abilityQCooldownMax):
        player_fire_rate -= dt
        if player_fire_rate <= 0:
            player_laser2_list.append(pyglet.sprite.Sprite(texture_shuriken, player.x + 32, player.y + 32, batch=main_batch))
            player_fire_rate += 0.2
            moveShurikenX = mouseX
            moveShurikenY = mouseY
            abilityQCooldown = 0
            shurikenRange = 0
            sound_shuriken.play()
            moving = False

def slashCast(dt):
    global player_fire_rate, abilityWCooldown, abilityWCooldownMax, moveSlashX, moveSlashY, mouseX, mouseY, slashRange, player_slash_list, moving

    if (abilityWCooldown >= abilityWCooldownMax):
        player_fire_rate -= dt
        if player_fire_rate <= 0:
            missile = pyglet.sprite.Sprite(texture_block_50x50, player.x + 50, player.y + 50, batch=main_batch)
            missile.image.anchor_x = missile.image.width / 2
            missile.image.anchor_y = missile.image.height / 2
            missile.rotation = float(angle(mouseX, player.x, mouseY, player.y)) 
            if (missile.rotation > 70 and missile.rotation < 120) or (missile.rotation > 200 and missile.rotation < 300):
                missile.rotation += 180
            player_slash_list.append(missile)
            player_fire_rate += 0.2
            moveSlashX = mouseX
            moveSlashY = mouseY
            abilityWCooldown = 0
            slashRange = 0
            sound_slash.play()
            moving = False

def eventSkills(dt):
    global skillQ
    skillQ.loop(dt)     

def collision(entity, list):
    global moving

    for item in list:
        
        if item.x < entity.x + entity.width and item.x + item.width > entity.x \
                and item.y < entity.y + entity.height and item.height + item.y > entity.y:

            angleDiference = angle(item.x, entity.x, item.y, entity.y) - anglePlayer
            if angleDiference < 0:
                angleDiference = angleDiference * -1

            if angleDiference <= 45:
                moving = False
                return True 

def update(dt):
    global abilityQCooldown, abilityQCooldownMax, player_movespeed, walls, abilityWCooldown, abilityWCooldownMax
    if started:
        global moving, moveX, moveY
        if moving == True:
            if not (collision(player, walls)):
                msx = player_movespeed
                msy = player_movespeed
                diferenceX = moveX - player.x
                diferenceY = moveY - player.y

                if diferenceX < 0:
                    diferenceX = diferenceX * -1
                if diferenceY < 0:
                    diferenceY = diferenceY * -1

                if diferenceX > diferenceY:
                    msy = msy * (diferenceY/diferenceX)
                elif diferenceX < diferenceY:
                    msx = msx * (diferenceX/diferenceY)

                if player.x > moveX:
                    player.x -= msx * dt   
                if player.x < moveX:
                    player.x += msx * dt  
                if player.y > moveY:
                    player.y -= msy * dt   
                if player.y < moveY:
                    player.y += msy * dt   
                if player.y == moveY and player.x == moveX:
                    moving = False 
        

        abilityQCooldown += dt
        abilityWCooldown += dt
        if abilityQCooldown > abilityQCooldownMax:
            abilityQCooldown = abilityQCooldownMax
        if abilityWCooldown > abilityWCooldownMax:
            abilityWCooldown = abilityWCooldownMax
        if fire2:
            player_shoot2(dt)
        if fireClick:
            slashCast(dt)
        eventSkills(dt)
        

##########################################################################

if __name__ == "__main__":
    pyglet.clock.schedule_interval(update, 1.0/60)
    pyglet.app.run()
