import pygame
from random import randint
import math

# список будет заполняться при каждом запуске игры случайными цветами для каждой плитки
blockColors = []

def generateBlockColorsList(DIFFERENT_BLOCKS_AMOUNT):
        FROM = 50
        TO = 205
        
        for i in range(DIFFERENT_BLOCKS_AMOUNT):
            blockColors.append((randint(FROM,TO), randint(FROM,TO), randint(FROM,TO)))

def getColorFromValue(value):
    return blockColors[int(math.log(value, 2))] 

colors = {
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "gray": (122, 122, 122),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "milk": (248, 249, 243),
}

def loadImg(filename, width=0, height=0):
    img = pygame.image.load(filename)
    
    if not width:
        width = img.get_width()
    if not height:
        height = img.get_height()
    
    img = pygame.transform.scale(img, (width, height))
    return img