import pyglet
from pyglet.window import key
from pyglet.window import FPSDisplay
from pyglet.window import mouse
import textures
import units

def display_window_preload():
    global window
    window = pyglet.window.Window(width=1200, height=800, caption="goeninjas", resizable=False)
    window.set_location(400, 100)

    global main_batch
    main_batch = pyglet.graphics.Batch()

def texture_load_all():
    global texture_block_50x50
    texture_block_50x50 = pyglet.image.load('sprites/block50x50.png')

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

def constants_load():
    global started
    started = False

    global mouseX , mouseY
    mouseX = 0
    mouseY = 0

def overworld_units_spawn():
    global player, main_batch
    player = units.Ninja(main_batch, 200, 200)

def initialization():
    display_window_preload()
    display_fps_show()
    texture_load_all()
    display_hud()
    overworld_map_spawn()
    overworld_units_spawn()
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
    global player, mouseX, mouseY
    player.on_mouse_press(x, y, button, modifiers)   

@window.event
def on_mouse_release(x, y, button, modifiers):
    pass

@window.event
def on_mouse_motion(x, y, dx, dy):
    global mouseX, mouseY
    mouseX = x
    mouseY = y

@window.event
def on_key_press(symbol, modifiers):
    global player, mouseX, mouseY
    player.on_key_press(symbol, modifiers, mouseX, mouseY)  

    global  started
    if symbol == key.SPACE:
        if not started:
            started = True

@window.event
def on_key_release(symbol, modifiers):
    pass

def eventSkills(dt):
    global player, walls
    player.update(dt, walls)    

def update(dt):
    if started:
        eventSkills(dt)
        
##########################################################################

if __name__ == "__main__":
    pyglet.clock.schedule_interval(update, 1.0/60)
    pyglet.app.run()
