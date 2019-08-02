"""
TODO
- fix rotating at edges ----
- add next tet ----
- add gameover
- update screen less often (only on frames w/ movement) ----
"""

import sys
import pygame
import numpy as np
from Tetromino import Tet


class Game(object):

    WIDTH, HEIGHT = 600, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    BLACK = 0, 0, 0
    WHITE = 255, 255, 255

    gridRectSize = 30
    gridRect = pygame.Rect(0, 0, gridRectSize, gridRectSize)
    gridSize = (20, 10)
    grid = np.zeros(gridSize, dtype=int)

    collided = False
    spaceCollide = False

    level = 0
    lines = 0
    score = 0

    levelTime = 1000

    gameOver = False

    scoreList = [40, 100, 300, 1200]

    colorList = [
        ("red", (255, 0, 0)),
        ("orange", (255, 102, 0)),
        ("yellow", (255, 255, 0)),
        ("green", (0, 255, 0)),
        ("cyan", (0, 255, 255)),
        ("blue", (0, 0, 255)),
        ("purple", (204, 0, 255))
    ]

    font = None

    pygame.time.set_timer(pygame.USEREVENT+1, levelTime)

    delLineList = []

    movingTet = Tet()
    nextTet = Tet()
    # savedTet = Tet()?

    def __init__(self):
        pygame.init()
        self.font = pygame.font.SysFont('Arial', 20)

    def main(self):

        while not self.gameOver:

            # resets grid
            if not self.collided:
                for piece in self.movingTet.pieces:
                    newX = self.movingTet.location[0]+piece[0]
                    newY = self.movingTet.location[1]+piece[1]
                    self.grid.itemset((newY, newX), 0)

            # gets keyboard presses
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                # if timer runs out try moving piece down
                if event.type == pygame.USEREVENT+1:
                    self.collided = self.movingTet.tryMove(0, 1, self.grid)

                if event.type == pygame.KEYDOWN:

                    # if space hard drop
                    if event.key == pygame.K_SPACE:

                        while not self.spaceCollide:
                            self.spaceCollide = self.movingTet.tryMove(
                                0, 1, self.grid)
                        self.spaceCollide = False
                        self.collided = True

                    # if up rotate clockwise
                    if event.key == pygame.K_UP:
                        if self.movingTet.col != 2:
                            self.movingTet.rotate(self.grid)
                        # movingTet.tryMove(0,-1,grid)

                    # if left move left
                    if event.key == pygame.K_LEFT:
                        if not self.spaceCollide:
                            self.movingTet.tryMove(-1, 0, self.grid)

                    # if right move right
                    if event.key == pygame.K_RIGHT:
                        if not self.spaceCollide:
                            self.movingTet.tryMove(1, 0, self.grid)

            # if down is held, soft drop
            pressed = pygame.key.get_pressed()
            if pygame.time.get_ticks() % 50 == 0:
                if pressed[pygame.K_DOWN]:
                    self.collided = self.movingTet.tryMove(0, 1, self.grid)
                    if not self.collided:
                        pygame.time.set_timer(pygame.USEREVENT+1, self.levelTime)

            # update grid for coloring
            for piece in self.movingTet.pieces:
                newX = self.movingTet.location[0]+piece[0]
                newY = self.movingTet.location[1]+piece[1]                   
                self.grid.itemset((newY, newX), self.movingTet.col+1)

            # update screen
            self.updateScreen()

            # if collided, replaces movingTet with nextTet, gen
            if self.collided:
                self.movingTet.set(self.nextTet)
                self.nextTet = Tet()

                # check for gameover
                for piece in self.movingTet.pieces:
                    newX = self.movingTet.location[0]+piece[0]
                    newY = self.movingTet.location[1]+piece[1]
                    
                    if self.grid[newY][newX]!=0:
                        self.gameOver = True
                        print("gameover")
                        break

                pygame.display.flip()
                pygame.time.delay(self.levelTime)

                # checks for lines
                for i in range(self.gridSize[0]):
                    if 0 not in self.grid[i, :]:
                        self.delLineList.append(i)

                # deletes lines if there are any
                if len(self.delLineList) > 0:
                    for line in self.delLineList:
                        for j in reversed(range(line)):
                            self.grid[j+1, :] = self.grid[j, :]
                        self.grid[0, :] = 0

                    # updates statistics
                    self.lines += len(self.delLineList)
                    self.score += (self.level+1) * \
                        self.scoreList[len(self.delLineList)-1]

                    # speeds up game
                    if self.lines != 0 and self.lines % 10 == 0:
                        self.level += 1
                        if self.level < 16:
                            self.levelTime -= 50
                        elif self.level >= 16 and self.level < 40:
                            self.levelTime -= 10
                        else:
                            pass  # ?

                    self.delLineList = []

                self.collided = False
                #pygame.time.set_timer(pygame.USEREVENT+1, self.levelTime)

            pygame.display.flip()
        
        # at gameover screen
        self.screen.blit(self.font.render("Game Over", True, (127,127,127)), (300,300))
        pygame.display.flip()
        pygame.time.delay(10000)

    def updateScreen(self):
        self.screen.fill(self.WHITE)

        # draws grid w/ colors
        for i in range(self.gridSize[0]):
            for j in range(self.gridSize[1]):
                gridRect2 = self.gridRect.copy()
                gridRect2.x = j*self.gridRectSize
                gridRect2.y = i*self.gridRectSize
                gridRect3 = gridRect2.copy()
                pygame.draw.rect(
                    self.screen, self.colorList[self.grid[i][j]-1][1] if self.grid[i][j] > 0 else self.WHITE, gridRect2, 0)
                pygame.draw.rect(self.screen, self.BLACK, gridRect3, 1)
                # screen.blit(font.render(str(j)+","+str(i), True, BLACK),
                #            (gridRect2.x+5, gridRect2.y+5))

        # draws NEXT and nextTet
        self.screen.blit(self.font.render("NEXT", True, self.BLACK), (362, 10))
        for piece in self.nextTet.pieces:
            gridRect4 = self.gridRect.copy()
            gridRect4.x = 375 + piece[0]*self.gridRectSize
            gridRect4.y = 75 + piece[1]*self.gridRectSize
            gridRect5 = gridRect4.copy()
            pygame.draw.rect(
                self.screen, self.colorList[self.nextTet.col][1], gridRect4, 0)
            pygame.draw.rect(self.screen, self.BLACK, gridRect5, 1)
        
        # draws statistics
        self.screen.blit(self.font.render(
            "LEVEL: " + str(self.level), True, self.BLACK), (350, 400))
        self.screen.blit(self.font.render(
            "LINES: " + str(self.lines), True, self.BLACK), (350, 425))
        self.screen.blit(self.font.render(
            "SCORE: " + str(self.score), True, self.BLACK), (350, 450))


if __name__ == "__main__":
    buttons = [0,0,0,0,0] # UP, DOWN, LEFT, RIGHT, SPACE
    
    game = Game()
    game.main()
