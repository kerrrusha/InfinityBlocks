import pygame

from field import *
from fontAdvanced import FontAdvanced
from lib import *
from gameProgress import *
from block import *
from metricPrefixes import *

import math

class InfinityBlocks:
    GAME_NAME = "Infinity Blocks"
    DIFFERENT_BLOCKS_AMOUNT = 50        # макс. блок (2^50 = 1125899906842624)

    # dislpay settings
    WIDTH = 480
    HEIGHT = 660
    FPS = 30

    # field settings
    ROWS = 8
    COLS = 7

    # block settings
    BLOCK_WIDTH = 60

    # design settings
    BORDERS_EXTRA_WIDTH = 10
    BORDERS_HEIGHT = 5

    nextBlock = None

    def __init__(self):
        # Создаем игру и окно
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption(self.GAME_NAME)
        self.clock = pygame.time.Clock()

        generateBlockColorsList(self.DIFFERENT_BLOCKS_AMOUNT)

        self.font = FontAdvanced("bahnschrift", 25)
        self.smallFont = FontAdvanced(None, 20)
        self.bigFont = FontAdvanced("bahnschrift", 30)

        self.gameProgress = GameProgress()
        self.field = Field(self.BLOCK_WIDTH, self.ROWS, self.COLS, self.screen, self.font)
        
        fieldX = (self.WIDTH - self.field.width) // 2
        # fieldY = (self.HEIGHT - self.field.height) // 2
        self.field.locate(fieldX, 70)
    
    def run(self):
        running = True
        while running:                      #основной игровой цикл
            self.clock.tick(self.FPS)       #поддержание одинакового фпс

            for event in pygame.event.get():    # проверка событий
                if event.type == pygame.QUIT:   # обработка закрытия окна
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:    # клики мышкой
                    if event.button != 1:
                        continue
                    mouse = pygame.mouse.get_pos()          # координаты нажатия мышкой
                    
                    colClicked = self.field.getCol(mouse[0], mouse[1])
                    if colClicked != None:
                        val = self.gameProgress.nextBlockValue
                        if self.field.spawnBlock(colClicked, val):
                            self.gameProgress.refreshNextBlockValue()
            
            # логика
            self.field.update()
            self.removeDeprecatedBlocks()
            self.gameProgress.update()

            self.gameProgress.addScore(self.field.newScore)
            self.field.newScore = 0

            # предварительная отрисовка
            self.screen.fill(colors["black"])
            self.field.draw()
            self.field.drawBorders(self.BORDERS_EXTRA_WIDTH, self.BORDERS_HEIGHT)
            self.drawNextBlock()
            self.drawScore((self.WIDTH // 2, (self.field.y - self.BORDERS_HEIGHT) // 2))
            self.drawHighScore(self.field.x + self.field.width + self.BORDERS_EXTRA_WIDTH, (self.field.y - self.BORDERS_HEIGHT) // 2)
            
            # показываем кадр
            pygame.display.flip()       

        pygame.quit()        

    # уберет блоки со значением меньше минимального, что указан в прогрессе
    def removeDeprecatedBlocks(self):
        minValue = self.gameProgress.getMinBlockValue()
        for block in self.field.blocks:
            if block.value < minValue:
                self.field.removeBlock(block.id)

    def drawHighScore(self, rectRight, y):
        renderedText = self.smallFont.render("Hi: "+getMiddleValueName(self.gameProgress.highScore), True, colors["white"])
        textRect = pygame.Rect(0, y, renderedText.get_width(), renderedText.get_height())
        textRect.right = rectRight

        self.screen.blit(renderedText, textRect)

    def drawScore(self, center):
        renderedText = self.bigFont.render(getMiddleValueName(self.gameProgress.score), True, colors["white"])
        textRect = pygame.Rect(0, 0, renderedText.get_width(), renderedText.get_height())
        textRect.center = center

        self.screen.blit(renderedText, textRect)

    def nextBlockUpdate(self, x, y):
        updateNeeded = False
        if self.nextBlock is None:
            updateNeeded = True
        elif self.nextBlock.value != self.gameProgress.nextBlockValue:
            updateNeeded = True

        if updateNeeded:
            self.nextBlock = Block(self.gameProgress.nextBlockValue, self.BLOCK_WIDTH, x, y, self.screen, self.font)

    def drawNextBlock(self):
        blockX = self.field.x + self.field.width // 2 - self.BLOCK_WIDTH // 2
        blockY = self.field.y + self.field.height + 10

        self.nextBlockUpdate(blockX, blockY)
        self.nextBlock.draw()
        
        borderMargin = 3
        pygame.draw.rect(self.screen, colors["white"], (blockX-borderMargin, blockY-borderMargin, self.BLOCK_WIDTH+2*borderMargin, self.BLOCK_WIDTH+2*borderMargin), 1, 5)