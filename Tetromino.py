from random import randrange
import numpy as np

shapeList = [
    ((0, 0), (0, -1), (-1, -1), (1, 0)),   # RED S
    ((0, 0), (-1, 0), (1, 0), (1, -1)),  # ORANGE L
    ((0, 0), (0, -1), (1, 0), (1, -1)),  # YELLOW SQUARE
    ((0, 0), (-1, 0), (0, -1), (1, -1)),  # GREEN S
    ((0, 0), (-1, 0), (1, 0), (2, 0)),  # CYAN BAR
    ((0, 0), (1, 0), (-1, 0), (-1, -1)),  # BLUE L
    ((0, 0), (-1, 0), (0, -1), (1, 0))  # PURPLE T
]


class Tet:

    location = [5, 1]  # x,y
    rotationVal = 0  # use rotation matrix
    pieces = None
    col = 0

    def __init__(self):
        self.location = [5, 1]
        shapeVal = randrange(0, 7)
        self.pieces = shapeList[shapeVal]
        self.col = shapeVal

    def move(self, h, v):
        self.location[0] += h
        self.location[1] += v

    def tryMove(self, h, v, grid):
        collide = False
        for piece in self.pieces:
            newX = self.location[0]+piece[0]+h
            newY = self.location[1]+piece[1]+v

            inBoundsX = newX >= 0 and newX < grid.shape[1]
            inBoundsY = newY >= 0 and newY < grid.shape[0]
            if inBoundsX and inBoundsY:
                collide = collide or grid.item(newY, newX) != 0
            else:
                collide = True

        if not collide:
            self.move(h, v)
        return collide

    def rotate(self, dir, grid):  # only 1 or -1
        assert dir == 1 or dir == -1

        newPieceList = []
        for piece in self.pieces:
            rotM = np.array([[0, -dir],
                             [dir, 0]])
            locM = np.asarray(piece)

            rotated = np.matmul(rotM, locM)
            # print(rotated)
            newPieceList.append(rotated)

        collide = False
        for piece in newPieceList:

            newX = self.location[0]+piece[0]
            newY = self.location[1]+piece[1]
            collide = collide or grid.item(newY, newX) != 0
            #print("checking "+str(newX) + "," + str(newY) + " - grid is "+str(grid.item(newY, newX)))

        if not collide:
            # print("rotated")
            self.pieces = newPieceList
        else:
            pass
            #print("collided, no rotation")
