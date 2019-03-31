from graphics import *
import random

def main():
    win = GraphWin("My Circle", 500, 500)
    boxes = []
    boxesLeft = 64
    boxes.append([])
    for i in range(10):
        boxes[0].append([])
    for i in range(8):
        boxes.append([[]])
        for j in range(8):
            box = Rectangle(Point(i * 50 + 50,j * 50 + 50), Point(i * 50 + 95, j * 50 + 95))
            if random.randint(1, 5) == 1:
                box.isBomb = True
                boxesLeft -= 1
            else:
                box.isBomb = False
            boxes[i + 1].append(box)
            boxes[i + 1][j + 1].draw(win)
        boxes[i].append([])
    for i in range(10):
        boxes[0].append([])

    gameOver = False

    def bombsAround(row, col):
        bombs = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if boxes[row + i ][col + j] and boxes[row + i][col + j].isBomb:
                    bombs += 1
        return bombs

    def revealBombs():
        for i in range(1, 9):
            for j in range(1, 9):
                if boxes[i][j].isBomb:
                    boxes[i][j].setFill("#f45942")

    while not gameOver:
        point = win.getMouse()
        row = int((point.getX() - 50) // 50) + 1
        col = int((point.getY() - 50) // 50) + 1
        box = boxes[row][col]
        if box.contains(point):
            if box.isBomb:
                box.setFill("#f45942")
                gameOver = True
            else:
                box.setFill("#4286f4")
                text = Text(box.getCenter(), str(bombsAround(row, col)))
                text.setTextColor("#302e2e")
                text.setSize(20)
                text.draw(win)

    textDisplay = Text(Point(250, 250), "")
    textDisplay.setSize(30)
    textDisplay.setTextColor("#302e2e")
    if boxesLeft == 0:
        textDisplay.setText("You Won!")
    else:
        revealBombs()
        textDisplay.setText("You Lost :(")
    textDisplay.draw(win)
    win.getMouse()





main()