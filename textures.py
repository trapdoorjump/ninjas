import pyglet

def texture_load(path, sequenceStart, sequenceEnd, width, height, animationInterval, looping):
    image = pyglet.image.load(path)
    sequence = pyglet.image.ImageGrid(image, sequenceStart, sequenceEnd, item_width=width, item_height=height)
    texture = pyglet.image.TextureGrid(sequence)
    sprite = pyglet.image.Animation.from_image_sequence(texture[0:], animationInterval, loop=looping)
    return sprite