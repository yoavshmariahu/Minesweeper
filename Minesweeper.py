from graphics import *
import random

def main():
    win = GraphWin("Minesweeper", 500, 500)
    
    # Initialize gird with no bombs
        # pad 8x8 grid with a layer of sentinel indices to simplify bombsAround()
    grid = []
    boxesLeft = 64
    grid.append([])
    for i in range(10):
        grid[0].append([])
    for i in range(8):
        grid.append([[]])
        for j in range(8):
            box = Rectangle(Point(i * 50 + 50,j * 50 + 50), Point(i * 50 + 95, j * 50 + 95))
            box.isBomb = False
            box.isRevealed = False
            grid[i + 1].append(box)
            grid[i + 1][j + 1].draw(win)
        grid[i + 1].append([])
    grid.append([])
    for i in range(10):
        grid[9].append([])

    # add 10 bombs onto grid at random indices
    bombIdx = random.sample(set(range(64)), 11)
    for i in range(10):
        idx = bombIdx.pop()
        grid[idx // 8 + 1][idx % 8 + 1].isBomb = True
        boxesLeft -= 1

    gameOver = False

    def bombsAround(row, col):
        # row - int
        # col - int
        # 
        # Given row and column, return number of bombs adjacent
        bombs = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if grid[row + i][col + j] and grid[row + i][col + j].isBomb:
                    bombs += 1
        return bombs

    def reveal(row, col):
        nonlocal boxesLeft
        b = grid[row][col]
        if b.isRevealed:
            return
        boxesLeft -= 1
        b.isRevealed = True
        if b.isBomb:
            b.setFill("#f45942")
        else:
            b.setFill("#4286f4")
            bombs = bombsAround(row, col)
            if bombs > 0:
                text = Text(b.getCenter(), str(bombs))
                text.setTextColor("#302e2e")
                text.setSize(20)
                text.draw(win)
            else:
                queue = []
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if grid[row + i][col + j] and not grid[row + i][col + j].isBomb:
                            queue.append((row + i, col + j))
                while len(queue) > 0:
                    item = queue.pop()
                    reveal(item[0], item[1])

    def revealBombs():
        # Display all bombs on grid
        for i in range(1, 9):
            for j in range(1, 9):
                if grid[i][j].isBomb:
                    grid[i][j].setFill("#f45942")

    score = Text(Point(350, 470), "Score: " + str(54 - boxesLeft))
    score.setSize(20)
    score.draw(win)

    firstClick = True
    while not gameOver and boxesLeft != 0:
        point = win.getMouse()
        row = int((point.getX() - 50) // 50) + 1
        col = int((point.getY() - 50) // 50) + 1
        box = grid[row][col]
        if box.contains(point) and not box.isRevealed:
            if box.isBomb and not firstClick:
                gameOver = True
            else:
                if firstClick and box.isBomb:
                    # Make first click safe
                    box.isBomb = False
                    altIdx = bombIdx.pop()
                    grid[altIdx // 8 + 1][altIdx % 8 + 1].isBomb = True
                reveal(row, col)
        score.setText("Score: " + str(54 - boxesLeft))
        firstClick = False

    textDisplay = Text(Point(250, 250), "")
    textDisplay.setSize(35)
    textDisplay.setTextColor("#302e2e")
    if boxesLeft == 0:
        textDisplay.setText("You Won!")
    else:
        textDisplay.setText("You Lost :(")
    revealBombs()
    textDisplay.draw(win)
    win.getMouse()


main()