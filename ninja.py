import pyglet
from pyglet.window import key
from pyglet.window import FPSDisplay
from pyglet.window import mouse
from random import randint, choice
import math


def display_window_preload():
    global window
    window = pyglet.window.Window(width=1200, height=800, caption="goeninjas", resizable=False)
    window.set_location(400, 100)

    global main_batch
    main_batch = pyglet.graphics.Batch()

def texture_load(path, sequenceStart, sequenceEnd, width, height, animationInterval, looping):
    image = pyglet.image.load(path)
    sequence = pyglet.image.ImageGrid(image, sequenceStart, sequenceEnd, item_width=width, item_height=height)
    texture = pyglet.image.TextureGrid(sequence)
    sprite = pyglet.image.Animation.from_image_sequence(texture[0:], animationInterval, loop=looping)
    return sprite

def texture_load_all():
    global texture_block_50x50
    texture_block_50x50 = pyglet.image.load('sprites/block50x50.png')

    global texture_ninja_blue
    texture_ninja_blue = texture_load('sprites/ninja-blue.png', 1, 2, 100, 100, 0.5, True)

    global texture_shuriken
    texture_shuriken = texture_load('sprites/ninja-shuriken-25x.png', 1, 4, 25, 25, 0.02, True)

    global texture_ninja_gray
    texture_ninja_gray = texture_load('sprites/ninja-blue.png', 1, 2, 100, 100, 0.5, True)

def display_fps_show():
    global window
    global display_fps
    display_fps = FPSDisplay(window)
    display_fps.label.font_size = 10


#init

display_window_preload()

display_fps_show()

texture_load_all()

text3 = pyglet.text.Label("HP", x=1000 , y=650, batch=main_batch)
text3.italic = True
text3.bold = True
text3.font_size = 16

numb_player_health = pyglet.text.Label(str(5), x=1100, y=600, batch=main_batch)
numb_player_health.color = (0, 100, 50, 255)
numb_player_health.font_size = 22

intro_text = pyglet.text.Label("Press space to start", x=550 , y=400)
intro_text.anchor_x = "center"
intro_text.anchor_y = "center"
intro_text.italic = True
intro_text.bold = True
intro_text.font_size = 40

player = pyglet.sprite.Sprite(texture_ninja_blue, x=200, y=200, batch=main_batch)

walls = []

for index in range(11):
    walls.append(pyglet.sprite.Sprite(texture_block_50x50, x=0, y=150 + index * 50, batch=main_batch)) 
    walls.append(pyglet.sprite.Sprite(texture_block_50x50, x=900, y=150 + index * 50, batch=main_batch)) 
    walls.append(pyglet.sprite.Sprite(texture_block_50x50, x=1150, y=150 + index * 50, batch=main_batch)) 
for index in range(24):
    walls.append(pyglet.sprite.Sprite(texture_block_50x50, x=index*50, y=100, batch=main_batch)) 
    walls.append(pyglet.sprite.Sprite(texture_block_50x50, x=index*50, y=700, batch=main_batch)) 
    

# explosion sound
explosion = pyglet.media.load('res/sounds/exp_01.wav', streaming=False)
player_gun_sound = pyglet.media.load('res/sounds/shuriken.wav', streaming=False)

player_laser_list = []
player_laser2_list = []
player_laser2b_list = []
enemy_laser_list = []
enemy_list = []
bg_list = []
explosion_list = []

# when creating a new enemy, it will choose a random direction from the list below
directions = [1, -1]

player_speed = 200
left = False
right = False
up = False
down = False
destroyed_enemies = 0 # this for only stats
next_wave = 0
fire = False
fire2 = False
player_fire_rate = 0
enemy_fire_rate = 0
ufo_head_spawner = 0
enemy_ship_spawner = 0
ufo_head_spawner_count = 1
enemy_ship_spawner_count = 5
preloaded =  False
player_health = 5
player_is_alive = True
explode_time = 2
enemy_explode = False
shake_time = 0
game = False
flash_time = 1
player_flash = False
abilityQCooldown = 0
abilityQCooldownMax = 0.5
moveX = 0
moveY = 0
moving = False
moveShurikenX = 0
moveShurikenY = 0
moveShuriken = False
mouseX = 0
mouseY = 0
shurikenTime = 2
shurikenRangeMax = 400
shurikenRange = 0
anglePlayer = 0



@window.event
def on_draw():
    window.clear()
    if not preloaded:
        preload()
    for bg in bg_list:
        bg.draw()
    if game:
        main_batch.draw()
    else:
        intro_text.draw()
    if not player_is_alive:
        game_over_text.draw()
    display_fps.draw()

@window.event
def on_mouse_press(x, y, button, modifiers):
    global player, anglePlayer
    degress = math.degrees(math.atan2(y-player.y, x-player.x))
    if degress < 0:
        degress += 360
    anglePlayer = degress
    if (button == 4):
        global moving, moveX, moveY
        moveX = x
        moveY = y
        moving = True

@window.event
def on_mouse_motion(x, y, dx, dy):
    global mouseX, mouseY
    mouseX = x
    mouseY = y

@window.event
def on_key_press(symbol, modifiers):
    global  right, left, up, down, fire, fire2, game
    if symbol == key.RIGHT:
        right = True
    if symbol == key.LEFT:
        left = True
    if symbol == key.UP:
        up = True
    if symbol == key.DOWN:
        down = True
    if symbol == key.SPACE:
        fire = True
        if not game:
            game = True
            fire = False
    if symbol == key.Q:
        fire2 = True

@window.event
def on_key_release(symbol, modifiers):
    global right, left, up, down, fire, fire2
    if symbol == key.RIGHT:
        right = False
    if symbol == key.LEFT:
        left = False
    if symbol == key.UP:
        up = False
    if symbol == key.DOWN:
        down = False
    if symbol == key.SPACE:
        fire = False
    if symbol == key.Q:
        fire2 = False

def angle(x1, x2, y1, y2):
    angleValue = math.degrees(math.atan2(y1-y2, x1-x2))
    if angleValue < 0:
        angleValue += 360
    return angleValue

def player_move(entity, dt):
    if right and entity.x < 800:
        entity.x += player_speed * dt
    if left and entity.x > 100:
        entity.x -= player_speed * dt
    if up and entity.y < 680:
        entity.y += player_speed * dt
    if down and entity.y > 35:
        entity.y -= player_speed * dt   

def preload():
    global preloaded
    preloaded = True

def player_shoot(dt):
    global player_fire_rate
    player_fire_rate -= dt
    if player_fire_rate <= 0:
        player_laser_list.append(pyglet.sprite.Sprite(texture_shuriken, player.x + 32, player.y + 32, batch=main_batch))
        player_fire_rate += 0.2
        if player_is_alive:
            player_gun_sound.play()

def player_shoot2(dt):
    global player_fire_rate, abilityQCooldown, moveShurikenX, moveShurikenY, mouseX, mouseY, moveShuriken, shurikenRange

    if (abilityQCooldown >= abilityQCooldownMax):
        player_fire_rate -= dt
        if player_fire_rate <= 0:
            player_laser2_list.append(pyglet.sprite.Sprite(texture_shuriken, player.x + 32, player.y + 32, batch=main_batch))
            player_laser2b_list.append(0)
            player_fire_rate += 0.2
            if player_is_alive:
                moveShurikenX = mouseX
                moveShurikenY = mouseY
                moveShuriken = True
                abilityQCooldown = 0
                shurikenRange = 0
                player_gun_sound.play()


def update_player_shoot(dt):
    global moveShurikenX, moveShurikenY, moveShuriken, shurikenTime, shurikenRange, shurikenRangeMax
    for lsr in player_laser_list:
        lsr.y += 300 * dt
        if lsr.y > 700: 
            player_laser_list.remove(lsr)
            lsr.delete()
    for lsr in player_laser2_list:
        msx = 450
        msy = 450
        diferenceX = moveShurikenX - lsr.x
        diferenceY = moveShurikenY - lsr.y

        if diferenceX < 0:
            diferenceX = diferenceX * -1
        if diferenceY < 0:
            diferenceY = diferenceY * -1

        if diferenceX > diferenceY:
            msy = msy * (diferenceY/diferenceX)
        elif diferenceX < diferenceY:
            msx = msx * (diferenceX/diferenceY)

        if (lsr.x < moveShurikenX):
            lsr.x += msx * dt  
        if (lsr.y < moveShurikenY):
            lsr.y += msy * dt 
        if (lsr.x > moveShurikenX):
            lsr.x -= msx * dt  
        if (lsr.y > moveShurikenY):
            lsr.y -= msy * dt 

        msy = (msy * dt)
        msx = (msx * dt)

        shurikenRange += math.sqrt( ( msy * msy ) + (msx  * msx ) )

        if (shurikenRange > shurikenRangeMax):
            player_laser2_list.remove(lsr)
            lsr.delete()    

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
    global abilityQCooldown, abilityQCooldownMax, player_speed, walls
    if game:
        global moving, moveX, moveY
        if moving == True:
            if not (collision(player, walls)):
                msx = player_speed
                msy = player_speed
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
        if abilityQCooldown > abilityQCooldownMax:
            abilityQCooldown = abilityQCooldownMax
        player_move(player, dt)
        if fire:
            player_shoot(dt)
        if fire2:
            player_shoot2(dt)
        update_player_shoot(dt)

if __name__ == "__main__":
    pyglet.clock.schedule_interval(update, 1.0/60)
    pyglet.app.run()
