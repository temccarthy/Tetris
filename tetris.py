"""
TODO
- refactor to OOP
- add score/level/lines
- add next tet
- add save tet
- add gameover

"""

import sys
import pygame
import numpy as np
from Tetromino import Tet

pygame.init()
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
BLACK = 0, 0, 0
WHITE = 255, 255, 255

gridRectSize = 30
gridRect = pygame.Rect(0, 0, gridRectSize, gridRectSize)
gridSize = (20, 10)

grid = np.zeros(gridSize, dtype=int)

colorList = [
    ("red", (255, 0, 0)),
    ("orange", (255, 102, 0)),
    ("yellow", (255, 255, 0)),
    ("green", (0, 255, 0)),
    ("cyan", (0, 255, 255)),
    ("blue", (0, 0, 255)),
    ("purple", (204, 0, 255))
]

movingTet = Tet()
font = pygame.font.SysFont('Arial', 10)

pygame.time.set_timer(pygame.USEREVENT+1, 1000)
collided = False
spaceCollide = False
delList = []

while True:

    # reset grid
    if not collided: 
        for piece in movingTet.pieces:
            newX = movingTet.location[0]+piece[0]
            newY = movingTet.location[1]+piece[1]
            grid.itemset((newY, newX), 0)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.USEREVENT+1:
            collided = movingTet.tryMove(0, 1, grid)
            print("forced down")

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:

                while not spaceCollide:
                    spaceCollide = movingTet.tryMove(0, 1, grid)
                spaceCollide = False
                collided = True

            if event.key == pygame.K_UP:
                movingTet.rotate(grid)
                #0movingTet.tryMove(0,-1,grid)

            # if event.key == pygame.K_DOWN:
            #     movingTet.tryMove(0, 1, grid)
            #     if not collided:
            #         pygame.time.set_timer(pygame.USEREVENT+1, 1000)

            if event.key == pygame.K_LEFT:
                if not spaceCollide:
                    movingTet.tryMove(-1, 0, grid)

            if event.key == pygame.K_RIGHT:
                if not spaceCollide:
                    movingTet.tryMove(1, 0, grid)

    pressed = pygame.key.get_pressed()   
    if pygame.time.get_ticks()%50==0:
        if pressed[pygame.K_DOWN]:
            print("down")
            collided = movingTet.tryMove(0, 1, grid)
            if not collided:
                pygame.time.set_timer(pygame.USEREVENT+1, 1000)

    for piece in movingTet.pieces:
        newX = movingTet.location[0]+piece[0]
        newY = movingTet.location[1]+piece[1]
        grid.itemset((newY, newX), movingTet.col+1)

    screen.fill(WHITE)
    for i in range(gridSize[0]):
        for j in range(gridSize[1]):
            gridRect2 = gridRect.copy()
            gridRect2.x = j*gridRectSize
            gridRect2.y = i*gridRectSize
            gridRect3 = gridRect2.copy()

            pygame.draw.rect(
                screen, colorList[grid[i][j]-1][1] if grid[i][j] > 0 else WHITE, gridRect2, 0)
            pygame.draw.rect(screen, BLACK, gridRect3, 1)
            #screen.blit(font.render(str(j)+","+str(i), True, BLACK),
            #            (gridRect2.x+5, gridRect2.y+5))

    if collided:
        movingTet = Tet()
        pygame.display.flip()
        pygame.time.delay(1000)
        for i in range(gridSize[0]):
            if 0 not in grid[i, :]:
                delList.append(i)

        if len(delList) > 0:
            for line in delList:
                for j in reversed(range(line)):
                    grid[j+1, :] = grid[j, :]
                grid[0, :] = 0
            delList = []
        collided = False
        pygame.time.set_timer(pygame.USEREVENT+1, 1000)

    pygame.display.flip()
