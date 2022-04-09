import pygame
from metricPrefixes import *
from lib import *

blocksSpawned = 0
class Block:
    # graphic settings
    PADDING = 2

    # координаты в которые движется блок
    destination = None
    speed = 80
    lastJourneySpeed = 20

    # когда True, field проверит окружающие блоки на совпадения и снимет флажок обратно
    checkNeeded = False

    # когда True, после прекращения движения (достижения цели), обьект будет удален
    lastJourney = False

    skipChecking = False
    combiningUpward = False     # True когда блок обьединяется вверх, тогда включается медленная скорость

    def __init__(self, value, blockWidth, x, y, screen, font):
        self.value = value
        self.blockWidth = blockWidth
        self.color = getColorFromValue(value)
        
        global blocksSpawned
        self.id = blocksSpawned
        blocksSpawned += 1

        self.x = x
        self.y = y

        self.screen = screen
        self.font = font
    
    def update(self):
        if self.destination is not None:
            if self.x == self.destination[0] and self.y == self.destination[1]:
                self.arrived()
                return

            # движение блоков к цели
            upward = True if (self.y - self.destination[1]) > 0 else False
            left = True if (self.x - self.destination[0]) > 0 else False

            if self.x != self.destination[0] and self.y == self.destination[1]:
                self.moveHorizontally(left)
            elif self.x == self.destination[0] and self.y != self.destination[1]:
                self.moveVertically(upward)

    def moveHorizontally(self, left):
        deltaX = -1 if left else 1
        speed = self.speed if not self.lastJourney else self.lastJourneySpeed
        for px in range(speed):
            self.x += deltaX
            if self.x == self.destination[0]:
                self.arrived()
                return

    def moveVertically(self, upward):
        deltaY = -1 if upward else 1
        speed = self.speed if not self.lastJourney and not self.combiningUpward else self.lastJourneySpeed
        for px in range(speed):
            self.y += deltaY
            if self.y == self.destination[1]:
                self.arrived()
                return

    def arrived(self):
        self.destination = None
        self.combiningUpward = False
        if not self.lastJourney:
            self.checkNeeded = True

    def getRect(self):
        return pygame.Rect(self.x, self.y, self.blockWidth, self.blockWidth)

    def draw(self):
        rect = pygame.Rect(self.x + self.PADDING, self.y + self.PADDING, self.blockWidth - 2*self.PADDING, self.blockWidth - 2*self.PADDING)
        pygame.draw.rect(self.screen, self.color, rect, border_radius=3)

        renderedText = self.font.render(getShortValueName(self.value), True, (255,255,255))
        textRect = renderedText.get_rect()
        textRect.center = self.getRect().center

        self.screen.blit(renderedText, textRect)

    def setValue(self, value):
        self.value = value
        self.color = getColorFromValue(value)