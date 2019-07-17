import pygame
import sys
import numpy as np
from Tetromino import Tet

pygame.init()
width, height = 600, 600
screen = pygame.display.set_mode((width, height))
black = 0, 0, 0
white = 255, 255, 255

gridRectSize = 30
gridRect = pygame.Rect(0, 0, gridRectSize, gridRectSize)
gridSize = (20, 11)

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

while True:

    # reset grid
    for piece in movingTet.pieces:
        newX = movingTet.location[0]+piece[0]
        newY = movingTet.location[1]+piece[1]
        grid.itemset((newY, newX), 0)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.USEREVENT+1:
            collided = movingTet.tryMove(0, 1, grid)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                # print("up")
                movingTet.rotate(1, grid)

            if event.key == pygame.K_DOWN:
                # print("down")
                movingTet.tryMove(0, 1, grid)
                if not collided:
                    pygame.time.set_timer(pygame.USEREVENT+1, 1000)

            if event.key == pygame.K_LEFT:
                # print("left")
                movingTet.tryMove(-1, 0, grid)

            if event.key == pygame.K_RIGHT:
                # print("right")
                movingTet.tryMove(1, 0, grid)

            if event.key == pygame.K_SPACE:
                # print("space")
                spaceCollide = False
                while not spaceCollide:
                    spaceCollide = movingTet.tryMove(0, 1, grid)
                #pygame.time.set_timer(pygame.USEREVENT+1, 1000)

    for piece in movingTet.pieces:
        newX = movingTet.location[0]+piece[0]
        newY = movingTet.location[1]+piece[1]
        grid.itemset((newY, newX), movingTet.col+1)

    

    if collided:
        #print('new tet created')
        movingTet = Tet()
        collided = False

    delList=[]
    for i in range(gridSize[0]):
        #print(grid[i,:])
        if 0 not in grid[i,:]:
            delList.append(i)

    for line in delList:
        for j in reversed(range(line)):
            grid[j+1,:] = grid[j,:]
        grid[0,:]=0
        delList=[]

    screen.fill(white)
    for i in range(gridSize[0]):
        for j in range(gridSize[1]):
            gridRect2 = gridRect.copy()
            gridRect2.x = j*gridRectSize
            gridRect2.y = i*gridRectSize
            gridRect3 = gridRect2.copy()

            pygame.draw.rect(
                screen, colorList[grid[i][j]-1][1] if grid[i][j] > 0 else white, gridRect2, 0)
            pygame.draw.rect(screen, black, gridRect3, 1)
            screen.blit(font.render(str(i)+","+str(j), True, black),
                        (gridRect2.x+5, gridRect2.y+5))

    pygame.display.flip()
