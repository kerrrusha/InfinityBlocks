from random import randint
from lib import *
import pickle
import math

class GameProgress:
    # к-ство доступных блоков минус один (если мин. блок 2, то доступных пять: 2, 4, 8, 16, 32)
    INDEX_RANGE = 4
    
    def __init__(self):
        # текущий минимальный блок (игра начинается со второго, далее += 1)
        self.minBlockDegree = 1
        
        self.score = 0
        # create if not exists
        try:
            with open("highscore.pkl", "rb") as f:
                self.highScore = pickle.load(f)
        except(OSError, IOError, EOFError) as e:
            with open("highscore.pkl", "wb") as f:
                self.highScore = 0
                pickle.dump(self.highScore, f)
        self.nextBlockValue = self.getRandomBlockValue()

    # значение при получении которого повышается минимальный блок
    def getCheckpointValue(self):
        return 2 ** (self.minBlockDegree + self.INDEX_RANGE + 1)

    def getMinBlockValue(self):
        return 2 ** self.minBlockDegree

    def getRandomBlockValue(self):
        degree = randint(self.minBlockDegree, (self.minBlockDegree + self.INDEX_RANGE))
        return 2 ** degree

    def update(self):
        if self.getMinBlockValue() > self.nextBlockValue:
            self.nextBlockValue = self.getRandomBlockValue()

    def refreshNextBlockValue(self):
        self.nextBlockValue = self.getRandomBlockValue()

    def addScore(self, val):
        self.score += val
        
        checkpointValue = self.getCheckpointValue()
        if val >= checkpointValue:
            self.minBlockDegree += int(math.log(val, 2) - math.log(checkpointValue, 2) + 1)

        if self.score > self.highScore:
            self.highScore = self.score
            with open("highscore.pkl", "wb") as f:
                pickle.dump(self.highScore, f)