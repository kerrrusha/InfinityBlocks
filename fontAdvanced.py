import pygame

class FontAdvanced:
    def __init__(self, fontName, fontSize):
        self.fontName = fontName
        self.fontSize = fontSize
        self.font = pygame.font.SysFont(fontName, fontSize)
    
    def render(self, text, bool, color):
        return self.font.render(text, bool, color)