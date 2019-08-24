import pyglet
import math

def angle(x1, x2, y1, y2):
    angleValue = math.degrees(math.atan2(y1-y2, x1-x2))
    if angleValue < 0:
        angleValue += 360
    return angleValue

def collision(entity, angleUnit, list):

    for item in list:
        if item.x < entity.x + entity.width and item.x + item.width > entity.x \
                and item.y < entity.y + entity.height and item.height + item.y > entity.y:

            angleDiference = angle(item.x, entity.x, item.y, entity.y) - angleUnit
            if angleDiference < 0:
                angleDiference = angleDiference * -1

            if angleDiference <= 45:
                return True 