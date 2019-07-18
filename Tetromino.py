from random import randrange
import numpy as np


class Tet:

    location = [0, 0]  # x,y
    pieces = None
    col = 0
    shapeList = [
        ((0, 0), (0, -1), (-1, -1), (1, 0)),   # RED S
        ((0, 0), (-1, 0), (1, 0), (1, -1)),  # ORANGE L
        ((0, 0), (0, -1), (1, 0), (1, -1)),  # YELLOW SQUARE
        ((0, 0), (-1, 0), (0, -1), (1, -1)),  # GREEN S
        ((0, 0), (-1, 0), (1, 0), (2, 0)),  # CYAN BAR
        ((0, 0), (1, 0), (-1, 0), (-1, -1)),  # BLUE L
        ((0, 0), (-1, 0), (0, -1), (1, 0))  # PURPLE T
    ]

    def __init__(self):
        self.location = [4, 1]
        shapeVal = randrange(0, 7)
        self.pieces = self.shapeList[shapeVal]
        self.col = shapeVal

    def move(self, h, v):
        self.location[0] += h
        self.location[1] += v

    def checkIfPiecesCollide(self, location, pieceList, grid):
        collide = False
        canMove = True

        for piece in pieceList:
            newX = location[0]+piece[0]
            newY = location[1]+piece[1]

            if not (newX >= 0 and newX < grid.shape[1]):
                canMove = False
            
            if canMove:
                if newY >= grid.shape[0]:
                    collide = True
                elif grid.item(newY, newX) != 0:
                    collide = True

        if collide:
            canMove = False
        return collide, canMove

    def tryMove(self, h, v, grid):
        newLocation = [x+y for x, y in zip(self.location, [h, v])]
        collide, canMove = self.checkIfPiecesCollide(newLocation, self.pieces, grid)

        if canMove:
            #print("moving right "+str(h)+" down "+str(v))
            self.move(h, v)
        return collide

    def rotate(self, grid):  # only 1 or -1
        newPieceList = []
        for piece in self.pieces:
            rotM = np.array([[0, -1],
                             [1, 0]])
            locM = np.asarray(piece)

            rotated = np.matmul(rotM, locM)

            newPieceList.append(rotated)

        collide, canMove = self.checkIfPiecesCollide(
            self.location, newPieceList, grid)

        if canMove:
            self.pieces = newPieceList
