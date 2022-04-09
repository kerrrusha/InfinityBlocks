from time import sleep
import pygame
from block import *

class Field:
    blocks = []
    blocksSpawned = 0
    
    # временное хранилище к-ства очков, которые должны быть засчитаны игрой
    newScore = 0

    def __init__(self, blockWidth, rows, cols, screen, font):
        self.blockWidth = blockWidth
        self.rows = rows
        self.cols = cols
        self.screen = screen
        self.font = font

        self.width = cols * blockWidth
        self.height = rows * blockWidth

        self.MAX_BLOCKS_AMOUNT = rows * cols

        self.creatingTime = pygame.time.get_ticks()
        self.lifeTime = 0

    def update(self):
        self.lifeTime = pygame.time.get_ticks() - self.creatingTime

        for block in self.blocks:
            if block.lastJourney and block.destination is None:
                self.removeBlock(block.id)
                continue
            block.update()

            blockCurrentValue = block.value
            if block.checkNeeded:
                self.checkForMatches(block)
                if blockCurrentValue != block.value and not block.skipChecking:
                    self.checkForMatches(block)
            block.checkNeeded = False
            block.skipChecking = False

            if block.destination is None:
                self.gravityCheck(block)

            # blocksInCols = []
            # for j in range(self.cols):
            #     blocksInCols.append(self.getBlocksInCol(j))
            # print(blocksInCols)

            # matrice = []
            # for i in range(self.rows):
            #     matrice.append([])
            #     for j in range(self.cols):
            #         matrice[i].append(self.getBlockAmountInCell(i,j))
            #     print(matrice[i])
            # print(self.lifeTime/1000, " seconds since started")

    def gravityCheck(self, block):
        blockAdress = self.getCellAdressByStaticBlock(block)
        if blockAdress is None:
            return

        i = blockAdress[0]
        j = blockAdress[1]

        if self.getBlockAmountInCell(i-1,j) == 0:
            block.destination = (block.x, block.y - self.blockWidth)

    def removeBlock(self, blockId):
        for i in range(len(self.blocks)):
            block = self.blocks[i]
            if block.id == blockId:
                self.blocks.pop(i)
                return

    def checkForMatches(self, testBlock):
        up = None
        right = None
        down = None
        left = None

        for block in self.blocks:
            if block.id == testBlock.id or block.destination is not None:
                continue
            if block.x == testBlock.x:
                if block.y == testBlock.y - self.blockWidth:
                    up = block
                if block.y == testBlock.y + self.blockWidth:
                    down = block
            if block.y == testBlock.y:
                if block.x == testBlock.x - self.blockWidth:
                    left = block
                if block.x == testBlock.x + self.blockWidth:
                    right = block
        
        # удаляем все элементы == None
        possibleBlocks = list(filter(None, [up, right, down, left]))

        approvedBlockIDs = []
        for i in range(len(possibleBlocks)):
            if possibleBlocks[i].value == testBlock.value and not possibleBlocks[i].lastJourney:
                approvedBlockIDs.append(possibleBlocks[i].id)

        if len(approvedBlockIDs) > 0:
            self.combine(testBlock, approvedBlockIDs)

    def combine(self, centralBlock, approvedBlockIDs):
        amount = len(approvedBlockIDs)
        newValue = centralBlock.value * (2**amount)

        for blockID in approvedBlockIDs:
            block = self.getBlockByID(blockID)
            if block.x == centralBlock.x:
                if block.y == centralBlock.y - self.blockWidth:
                    # двигаем вниз
                    # если обьед. один блок, то нижний двигаем вверх
                    if len(approvedBlockIDs) == 1:
                        centralBlock.destination = (block.x, block.y)
                        centralBlock.skipChecking = True
                        centralBlock.combiningUpward = True
                    # если обьед. два/три блока, то верхний сначала двигаем вниз
                    else:
                        block.destination = (block.x, block.y + self.blockWidth)
                elif block.y == centralBlock.y + self.blockWidth:
                    block.destination = (block.x, block.y - self.blockWidth)
            elif block.y == centralBlock.y:
                if block.x == centralBlock.x - self.blockWidth:
                    # двигаем вправо
                    block.destination = (block.x + self.blockWidth, block.y)
                if block.x == centralBlock.x + self.blockWidth:
                    block.destination = (block.x - self.blockWidth, block.y)
            block.lastJourney = True
        centralBlock.setValue(newValue)

        # сохраняем к-ство очков, которые игра должна будет добавить
        self.newScore += newValue

    def spawnBlock(self, col, value):
        if self.calcBlocksInColumn(col) >= self.rows and not self.lastBlockInColumnMatching(col, value):
            return False

        x = self.x + col*self.blockWidth
        y = self.y + self.height - self.blockWidth
        
        self.blocksSpawned += 1
        block = Block(value, self.blockWidth, x, y, self.screen, self.font)
        block.destination = self.getDestination(col)
        self.blocks.append(block)
        return True



    def draw(self):
        for block in self.blocks:
            block.draw()
    def drawBorders(self, extraWidth, height):
        fieldRect = self.getRect()

        topBorderRect = pygame.Rect(fieldRect.left - extraWidth, fieldRect.top - height, fieldRect.width+2*extraWidth, height)
        bottomBorderRect = pygame.Rect(fieldRect.left - extraWidth, fieldRect.bottom, fieldRect.width+2*extraWidth, height)
        
        borderRects = [topBorderRect, bottomBorderRect]
        for borderRect in borderRects:
            pygame.draw.rect(self.screen, (255,255,255), borderRect)

    # возвращает координаты (x,y) первого свободного блока в указанной колонке
    def getDestination(self, col):
        x = self.x + col*self.blockWidth
        y = self.y + self.calcBlocksInColumn(col)*self.blockWidth
        
        return (x,y)
    
    def lastBlockInColumnMatching(self, col, value):
        colX = self.x + col*self.blockWidth
        
        lastBlock = None
        for block in self.blocks:
            if block.x != colX:
                continue
            if lastBlock is None:
                lastBlock = block
            elif block.y > lastBlock.y:
                lastBlock = block

        if lastBlock.value != value:
            return False
        return True

    def getBlockByID(self, blockID):
        for block in self.blocks:
            if block.id == blockID:
                return block

    def getBlockByAdress(self, i, j):
        cellCenter = (self.x + j*self.blockWidth + (self.blockWidth // 2), self.y + i*self.blockWidth + (self.blockWidth // 2))
        for block in self.blocks:
            if block.getRect().collidepoint(cellCenter):
                return block
        return None

    def getBlockAmountInCell(self, i, j):
        if i < 0 or i >= self.rows or j < 0 or j >= self.cols:
            return None

        amount = 0
        cellCenter = (self.x + j*self.blockWidth + (self.blockWidth // 2), self.y + i*self.blockWidth + (self.blockWidth // 2))
        for block in self.blocks:
            if block.getRect().collidepoint(cellCenter):
                amount += 1
        return amount

    def getBlockIndexByID(self, blockID):
        for i in range(len(self.blocks)):
            if self.blocks[i].id == blockID:
                return i

    def getBlocksInCol(self, col):
        padding = 1

        x = self.x + col*self.blockWidth + padding
        y = self.y + padding
        width = self.blockWidth - 2*padding
        height = self.height - 2*padding

        rect = pygame.Rect(x, y, width, height)
        
        amount = 0
        for block in self.blocks:
            if block.getRect().colliderect(rect):
                amount += 1
        return amount

    # вернет номер ряда, на котором находится указанный блок
    def getBlockRow(self, block):
        row = ((block.y - self.y) / self.blockWidth)
        if row - int(row) != 0:
            return int(row) + 1
        return int(row)

    # вернет прямоугольник от ячейки до потолка
    def getRectFromBlockToRoof(self, mainBlock):     
        localX = mainBlock.x - self.x
        col = int(localX // self.blockWidth)

        rectX = self.x + col * self.blockWidth
        rectY = self.y
        
        rectHeight = mainBlock.y - self.y

        return pygame.Rect(rectX, rectY, self.blockWidth, rectHeight) 

    def getCellAdressByStaticBlock(self, block):
        if block is None:
            return 
        if not self.getRect().collidepoint(block.x, block.y):
            return

        return ((block.y - self.y)//self.blockWidth, (block.x - self.x)//self.blockWidth)

    # суть в том чтобы построить прямоугольник от потолка до указанного блока,
    # и посчитать, со сколькими блоками этот прямоугольник пересечется
    def getBlocksUnderBlockAmount(self, mainBlock):
        amount = 0
        
        rectFromBlockToRoof = self.getRectFromBlockToRoof(mainBlock)
        for block in self.blocks:
            if block.id == mainBlock.id:
                continue
            if rectFromBlockToRoof.colliderect(block.getRect()):
                amount += 1

        return amount
    
    def calcBlocksInColumn(self, col):
        x = self.x + self.blockWidth * col
        blocksInColumn = 0
        for block in self.blocks:
            if block.x == x:
                blocksInColumn += 1
        return blocksInColumn

    def locate(self, x, y):
        self.x = x 
        self.y = y

    def getRect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def getCol(self, x, y):
        if (self.y + self.height) < y or y < self.y:
            return
        if (self.x + self.width) < x or x < self.x:
            return

        localX = x - self.x
        return int(localX / self.blockWidth)

    # рядок первой свободной ячейки в выбранной колонке
    def getFreeCellRow(self, col):
        for i in range(self.rows):
            if self.field[i][col] == None:
                return i