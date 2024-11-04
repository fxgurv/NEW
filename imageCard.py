import random
 
from PIL import Image, ImageDraw, ImageFilter
 
def rndColor():
    return (random.randint(128, 255), random.randint(128, 255), random.randint(128, 255))
 
def leftColor():
    return (220, 220, 220)
 
def rightColor():
    return (170, 170, 170)
 
def singleColor():
    image = Image.new('RGB', (1024,960), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    for x in range(24, 1823):
        for y in range(1920):
            draw.point((x, y), fill=leftColor())
    for x in range(1847, 3647):
        for y in range(1920):
            draw.point((x, y), fill=rightColor())
    image.save('singleColor.png','png')

def mixRowColor():
    image = Image.new('RGB', (1024,960), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    for x in range(24, 1823, 2):
        for y in range(1920):
            draw.point((x, y), fill=leftColor())
            draw.point((x+1, y), fill=rightColor())
    for x in range(1847, 3647, 2):
        for y in range(1920):
            draw.point((x, y), fill=rightColor())
            draw.point((x+1, y), fill=leftColor())
    image.save('mixRowColor.png','png')

    
def mixRowColumnColor():
    image = Image.new('RGB', (1024,960), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    for x in range(24, 1823, 2):
        for y in range(0, 1920, 2):
            draw.point((x, y), fill=leftColor())
    for x in range(24+1, 1823, 2):
        for y in range(0, 1920, 2):
            draw.point((x, y), fill=rightColor())
    for x in range(24, 1823, 2):
        for y in range(1, 1920, 2):
            draw.point((x, y), fill=rightColor())
    for x in range(24+1, 1823, 2):
        for y in range(1, 1920, 2):
            draw.point((x, y), fill=leftColor())
    for x in range(1847, 3647, 2):
        for y in range(0, 1920, 2):
            draw.point((x, y), fill=rightColor())
    for x in range(1847+1, 3647, 2):
        for y in range(0, 1920, 2):
            draw.point((x, y), fill=leftColor())
    for x in range(1847, 3647, 2):
        for y in range(1, 1920, 2):
            draw.point((x, y), fill=leftColor())
    for x in range(1847+1, 3647, 2):
        for y in range(1, 1920, 2):
            draw.point((x, y), fill=rightColor())
    image.save('mixRowColumnColor.png','png')

singleColor()
mixRowColor()
mixRowColumnColor()